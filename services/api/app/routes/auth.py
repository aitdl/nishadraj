"""
Project: NishadRaj OS
Author: Jawahar R Mallah
Organization: AITDL
License: AGPL-3.0 + Governance Protection Terms
Copyright © Jawahar R Mallah | AITDL
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database.session import get_db
import uuid
from typing import Optional
from app.schemas.user import UserCreate, UserOut, Token, UserUpdate, UserRegistrationOut, TOTPVerify
from app.core.security import (
    get_password_hash, verify_password, create_access_token,
    generate_totp_secret, generate_totp_uri, generate_qr_code, verify_totp
)
from app.core.governance_hook import enforce_governance
from app.models.user import UserRole, User
from app.models.audit_log import AuditLog
from fastapi.security import OAuth2PasswordRequestForm
from datetime import datetime
from system.documentation_engine import log_task_event, log_error, log_change
from app.core.dependencies import get_current_user, require_role

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/register", response_model=UserRegistrationOut)
async def register(user_in: UserCreate, db: Session = Depends(get_db)):
    """
    Register a new user. Enforces governance preflight.
    Generates TOTP secret for 2FA enrollment.
    """
    # Phase 7: Governance Enforcement
    enforce_governance("AUTH_002")
    
    user = db.query(User).filter(User.email == user_in.email).first()
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exists"
        )
    
    totp_secret = generate_totp_secret()
    new_user = User(
        email=user_in.email,
        hashed_password=get_password_hash(user_in.password),
        role=user_in.role,
        is_active=user_in.is_active,
        totp_secret=totp_secret,
        is_2fa_enabled=False
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    # Generate QR Code for enrollment
    totp_uri = generate_totp_uri(new_user.email, totp_secret)
    qr_code = generate_qr_code(totp_uri)
    
    # Audit Log
    db.add(AuditLog(
        user_id=new_user.id,
        event_type="USER_REGISTER",
        module="AUTH",
        description=f"User registered: {new_user.email}",
        status="SUCCESS",
        details={"email": new_user.email}
    ))
    db.commit()

    # Phase 4: Documentation Engine log
    log_change(
        module="AUTH",
        change_id=f"REG_{new_user.id}",
        impact=f"New user registered: {new_user.email}",
        risk_level="LOW"
    )
    
    return {"user": new_user, "qr_code_base64": qr_code, "totp_secret": totp_secret}

@router.post("/enable-2fa", response_model=UserOut)
async def enable_2fa(verify_in: TOTPVerify, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """
    Enable 2FA for the current user. Requires password and TOTP token.
    """
    # Phase 7: Governance Enforcement
    enforce_governance("AUTH_002")
    
    if not verify_password(verify_in.password, current_user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid password")
    
    if not verify_totp(current_user.totp_secret, verify_in.token):
        raise HTTPException(status_code=400, detail="Invalid TOTP token")
    
    current_user.is_2fa_enabled = True
    db.commit()
    db.refresh(current_user)
    
    # Audit Log
    db.add(AuditLog(
        user_id=current_user.id,
        event_type="2FA_ENABLE",
        module="AUTH",
        description="2FA enabled for user",
        status="SUCCESS"
    ))
    db.commit()

    # Phase 4: Documentation Engine log
    log_change(
        module="AUTH",
        change_id=f"2FA_EN_{current_user.id}",
        impact="2FA protection activated",
        risk_level="LOW"
    )
    
    return current_user

@router.post("/login", response_model=Token)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(), 
    totp_token: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """
    OAuth2 compatible token login. Supports TOTP and Login Lockout.
    """
    user = db.query(User).filter(User.email == form_data.username).first()
    
    # Phase 6: Login Lockout
    if user and (user.failed_login_attempts >= 5 or user.account_locked):
        user.account_locked = True
        # Audit Log
        db.add(AuditLog(
            user_id=user.id,
            event_type="ACCOUNT_LOCK",
            module="AUTH",
            description="Account locked due to excessive failures",
            status="FAILURE",
            details={"reason": "Excessive failed attempts"}
        ))
        db.commit()
        
        # Documentation Engine log
        log_error(
            module="AUTH",
            error_id=f"LOCK_{user.id}",
            description="Account locked",
            root_cause="Brute force protection",
            solution="Admin intervention required"
        )
        
        raise HTTPException(status_code=403, detail="Account locked due to too many failed attempts")

    if not user or not verify_password(form_data.password, user.hashed_password):
        if user:
            user.failed_login_attempts += 1
            if user.failed_login_attempts >= 5:
                user.account_locked = True
            db.commit()
            
            # Audit Log
            db.add(AuditLog(
                user_id=user.id,
                event_type="LOGIN_FAILED",
                module="AUTH",
                description="Invalid credentials login attempt",
                status="FAILURE",
                details={"reason": "Invalid credentials"}
            ))
            db.commit()

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")

    # Phase 4: TOTP Verification
    if user.is_2fa_enabled:
        if not totp_token:
            raise HTTPException(status_code=400, detail="TOTP token required")
        if not verify_totp(user.totp_secret, totp_token):
            # Failed 2FA counts towards lockout
            user.failed_login_attempts += 1
            if user.failed_login_attempts >= 5:
                user.account_locked = True
            db.commit()
            
            # Audit Log
            db.add(AuditLog(
                user_id=user.id,
                event_type="LOGIN_FAILED_2FA",
                module="AUTH",
                description="Invalid TOTP token attempt",
                status="FAILURE"
            ))
            db.commit()
            raise HTTPException(status_code=401, detail="Invalid TOTP token")

    # Success: Reset failed attempts and update last_login_at
    user.failed_login_attempts = 0
    user.account_locked = False
    user.last_login_at = datetime.utcnow()
    db.commit()
    
    # Audit Log
    db.add(AuditLog(
        user_id=user.id,
        event_type="LOGIN_SUCCESS",
        module="AUTH",
        description="User logged in successfully",
        status="SUCCESS"
    ))
    db.commit()

    # Documentation Engine log
    log_task_event(
        module="AUTH",
        task_id=f"LOGIN_{user.id}",
        status="SUCCESS",
        notes=f"User {user.email} logged in"
    )
    
    access_token = create_access_token(subject=user.id)
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me", response_model=UserOut)
async def get_me(current_user: User = Depends(get_current_user)):
    """
    Get current user profile.
    """
    return current_user

@router.put("/users/{user_id}/role", response_model=UserOut)
async def change_role(
    user_id: uuid.UUID, 
    role_update: UserUpdate, 
    db: Session = Depends(get_db),
    admin_user: User = Depends(require_role(UserRole.ADMIN))
):
    """
    Change user role. Governance enforced.
    """
    # Phase 8: Governance Enforcement
    enforce_governance("AUTH_002")
    
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    user.role = role_update.role
    db.commit()
    db.refresh(user)
    return user

@router.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user_id: uuid.UUID, 
    db: Session = Depends(get_db),
    admin_user: User = Depends(require_role(UserRole.ADMIN))
):
    """
    Delete user. Governance enforced.
    """
    # Phase 8: Governance Enforcement
    enforce_governance("AUTH_002")
    
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    db.delete(user)
    db.commit()
    return None
