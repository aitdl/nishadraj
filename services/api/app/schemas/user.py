"""
Project: NishadRaj OS
Organization: AITDL | NISHADRAJ
Organization: AITDL
License: AGPL-3.0 + Governance Protection Terms
Copyright © AITDL | NISHADRAJ
"""

from pydantic import BaseModel, EmailStr, Field, validator
from typing import Optional
from app.models.user import UserRole
import uuid
from datetime import datetime

class UserBase(BaseModel):
    email: EmailStr
    is_active: Optional[bool] = True
    role: Optional[UserRole] = UserRole.AUDITOR

class UserCreate(UserBase):
    password: str = Field(..., min_length=10)

    @validator('password')
    def password_strength(cls, v):
        if len(v) < 10:
            raise ValueError('Password must be at least 10 characters long')
        return v

class UserUpdate(UserBase):
    password: Optional[str] = None

class UserOut(UserBase):
    id: uuid.UUID
    is_2fa_enabled: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenPayload(BaseModel):
    sub: Optional[str] = None

class UserRegistrationOut(BaseModel):
    user: UserOut
    qr_code_base64: Optional[str] = None
    totp_secret: Optional[str] = None

class TOTPVerify(BaseModel):
    token: str
    password: str

