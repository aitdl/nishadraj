"""
Project: NishadRaj OS
Organization: AITDL | NISHADRAJ
Organization: AITDL
License: AGPL-3.0 + Governance Protection Terms
Copyright © AITDL | NISHADRAJ
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import health, governance, auth
import logging

# Setup Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("nishadraj.backend")

app = FastAPI(
    title="NishadRaj OS Governed Backend",
    version="1.1.0",
    description="Enterprise API Core for NishadRaj OS"
)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Routers
app.include_router(health.router)
app.include_router(governance.router, prefix="/api")
app.include_router(auth.router, prefix="/api")

@app.on_event("startup")
async def startup_event():
    logger.info("NishadRaj OS Governed Backend Starting Up...")
    logger.info("Governance Mode: HARD_ENFORCEMENT")
    logger.info("Auth Status: ACTIVE")
    logger.info("RBAC: ENABLED")
    logger.info("JWT: ENABLED")

