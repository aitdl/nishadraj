"""
Project: NishadRaj OS
Organization: AITDL | NISHADRAJ
Organization: AITDL
License: AGPL-3.0 + Governance Protection Terms
Copyright © AITDL | NISHADRAJ
"""

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.models.user import User, UserRole
from app.core.config import settings
from app.schemas.user import TokenPayload

reuseable_oauth = OAuth2PasswordBearer(
    tokenUrl="/api/auth/login"
)

async def get_current_user(
    db: Session = Depends(get_db),
    token: str = Depends(reuseable_oauth)
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
        token_data = TokenPayload(sub=user_id)
    except JWTError:
        raise credentials_exception
        
    user = db.query(User).filter(User.id == token_data.sub).first()
    if user is None:
        raise credentials_exception
    return user

def require_role(required_role: UserRole):
    def role_checker(user: User = Depends(get_current_user)):
        # Higher roles bypass lower role requirements (logic can be adjusted)
        # ADMIN > EDITOR > AUDITOR
        hierarchy = {
            UserRole.ADMIN: 3,
            UserRole.EDITOR: 2,
            UserRole.AUDITOR: 1
        }
        
        if hierarchy.get(user.role, 0) < hierarchy.get(required_role, 0):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Operation requires {required_role} privileges"
            )
        return user
    return role_checker

async def rate_limiter():
    """
    STUB: Rate limiting logic.
    In production, this would use Redis to track requests per IP/User.
    """
    # Placeholder for rate limiting logic
    pass

async def check_login_lockout(email: str):
    """
    STUB: Invalid login lockout counter.
    In production, this would check a cache for failed attempts.
    """
    # Placeholder for lockout logic
    pass

