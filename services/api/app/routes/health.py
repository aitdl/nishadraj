"""
Project: NishadRaj OS
Organization: AITDL | NISHADRAJ
Organization: AITDL
License: AGPL-3.0 + Governance Protection Terms
Copyright © AITDL | NISHADRAJ
"""

from fastapi import APIRouter

router = APIRouter()

@router.get("/health", tags=["System"])
async def health_check():
    """
    Returns the system health and governance status.
    """
    return {
        "status": "ok",
        "project": "NishadRaj OS",
        "governance": "hard_enforced"
    }

