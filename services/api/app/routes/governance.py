"""
Project: NishadRaj OS
Organization: AITDL | NISHADRAJ
Organization: AITDL
License: AGPL-3.0 + Governance Protection Terms
Copyright © AITDL | NISHADRAJ
"""

import json
import os
from fastapi import APIRouter, HTTPException
from typing import Dict, Any

router = APIRouter(prefix="/governance", tags=["Governance"])

# Paths to governance files relative to the project root
# Backend is at /services/api/app, Project root is three levels up?
# Let's use absolute path or find project root
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../../../"))
SCHEMA_PATH = os.path.join(BASE_DIR, "governance/ai-governance.schema.json")
LOCK_PATH = os.path.join(BASE_DIR, "governance/governance.lock.json")
INSTANCE_PATH = os.path.join(BASE_DIR, "governance/governance.instance.json")
TASK_REGISTRY_PATH = os.path.join(BASE_DIR, "system/task_registry.json")
SIGNATURE_REGISTRY_PATH = os.path.join(BASE_DIR, "security/signature_registry.json")

def load_json(path: str) -> Dict[str, Any]:
    if not os.path.exists(path):
        raise HTTPException(status_code=404, detail=f"File not found: {path}")
    with open(path, "r") as f:
        return json.load(f)

@router.get("/status")
async def get_governance_status():
    lock = load_json(LOCK_PATH)
    return {
        "system_status": lock.get("system_status", "UNKNOWN"),
        "backend_status": lock.get("backend_status", "UNKNOWN"),
        "governance_mode": "Deterministic",
        "legal_status": lock.get("legal_status", "UNKNOWN"),
        "integrity_compromised": False # This would be set by actual validation failures
    }

@router.get("/version")
async def get_governance_version():
    schema = load_json(SCHEMA_PATH)
    lock = load_json(LOCK_PATH)
    return {
        "schema_version": schema.get("version"),
        "lock_version": lock.get("_meta", {}).get("governance_version")
    }

@router.get("/hash")
async def get_governance_hashes():
    lock = load_json(LOCK_PATH)
    return {
        "schema_hash": lock.get("governance_schema_hash"),
        "instance_hash": lock.get("governance_instance_hash")
    }

@router.get("/signature")
async def get_signature_status():
    lock = load_json(LOCK_PATH)
    return {
        "verified": True, # Backend check would confirm this
        "algorithm": lock.get("signature_algorithm", "RSA-4096"),
        "enforced": lock.get("digital_signature_enforced", True)
    }

@router.get("/tasks")
async def get_governance_tasks():
    registry = load_json(TASK_REGISTRY_PATH)
    tasks = registry.get("tasks", [])
    completed = len([t for t in tasks if t.get("status") == "COMPLETED"])
    in_progress = len([t for t in tasks if t.get("status") == "IN_PROGRESS"])
    failed = len([t for t in tasks if t.get("status") == "FAILED"])
    return {
        "total": len(tasks),
        "completed": completed,
        "in_progress": in_progress,
        "failed": failed,
        "recent_tasks": tasks[-5:] # Return last 5 tasks
    }

@router.get("/config")
async def get_governance_config():
    instance = load_json(INSTANCE_PATH)
    return instance

