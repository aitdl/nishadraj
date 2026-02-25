"""
Project: NishadRaj OS
Organization: AITDL | NISHADRAJ
Organization: AITDL
License: AGPL-3.0 + Governance Protection Terms
Copyright © AITDL | NISHADRAJ
"""

from datetime import datetime, timedelta
from typing import Any, Union
from jose import jwt
from passlib.context import CryptContext
from app.core.config import settings
import pyotp
import qrcode
import base64
from io import BytesIO

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def create_access_token(subject: Union[str, Any], expires_delta: timedelta = None) -> str:
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode = {"exp": expire, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

def decode_token(token: str) -> dict:
    try:
        decoded_token = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return decoded_token if decoded_token["exp"] >= datetime.utcnow().timestamp() else None
    except Exception:
        return None

def generate_totp_secret() -> str:
    """Generate a random TOTP secret."""
    return pyotp.random_base32()

def generate_totp_uri(email: str, secret: str) -> str:
    """Generate TOTP provisioning URI."""
    return pyotp.totp.TOTP(secret).provisioning_uri(
        name=email,
        issuer_name="NishadRaj OS"
    )

def verify_totp(secret: str, token: str) -> bool:
    """Verify a TOTP token."""
    totp = pyotp.TOTP(secret)
    return totp.verify(token)

def generate_qr_code(uri: str) -> str:
    """Generate a base64 encoded QR code image."""
    img = qrcode.make(uri)
    buffered = BytesIO()
    img.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode()

