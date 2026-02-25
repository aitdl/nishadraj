"""
Project: NishadRaj OS
Organization: AITDL | NISHADRAJ
Organization: AITDL
License: AGPL-3.0 + Governance Protection Terms
Copyright © AITDL | NISHADRAJ
"""

from sqlalchemy import String, DateTime, JSON, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from app.database.session import Base
from datetime import datetime, UTC
import uuid
from sqlalchemy.dialects.postgresql import UUID
from typing import Optional

class AuditLog(Base):
    __tablename__ = "audit_logs"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id: Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    event_type: Mapped[str] = mapped_column(String(100), nullable=False) # e.g., "LOGIN_SUCCESS", "LOGIN_FAILED", "ROLE_CHANGE"
    resource: Mapped[str] = mapped_column(String(255), nullable=False) # e.g., "/api/auth/login"
    status: Mapped[str] = mapped_column(String(50), nullable=False) # e.g., "SUCCESS", "FAILURE"
    ip_address: Mapped[Optional[str]] = mapped_column(String(45), nullable=True)
    details: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(UTC))

