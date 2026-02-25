"""
Project: NishadRaj OS
Organization: AITDL | NISHADRAJ
Organization: AITDL
License: AGPL-3.0 + Governance Protection Terms
Copyright © AITDL | NISHADRAJ
"""

import json
import hashlib
import os
from jsonschema import Draft7Validator
from jsonschema.exceptions import ValidationError
from datetime import datetime
import uuid

try:
    from system.documentation_engine import log_error
except ImportError:
    from documentation_engine import log_error

# Correct path for local imports if needed, but here we assume security is a package or in PYTHONPATH
try:
    from security.signature_manager import verify_all_governance_files
except ImportError:
    import sys
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
    from system.signature_manager import verify_all_governance_files

# Robust project root calculation
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SCHEMA_PATH = os.path.join(PROJECT_ROOT, "governance/ai-governance.schema.json")
LOCK_PATH = os.path.join(PROJECT_ROOT, "governance/governance.lock.json")
INSTANCE_PATH = os.path.join(PROJECT_ROOT, "governance/governance.instance.json")

def compute_sha256(filepath: str) -> str:
    with open(filepath, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest().upper()

def validate_schema_structure():
    if not os.path.exists(SCHEMA_PATH):
        raise FileNotFoundError(f"Schema file missing: {SCHEMA_PATH}")
        
    with open(SCHEMA_PATH) as f:
        schema = json.load(f)

    # Deterministic Draft 7 structural verification
    try:
        Draft7Validator.check_schema(schema)
    except ValidationError as e:
        raise Exception(f"Schema structural validation failed: {e.message}")

    return True

def validate_instance():
    if not os.path.exists(INSTANCE_PATH):
        raise FileNotFoundError(f"Instance file missing: {INSTANCE_PATH}")

    with open(SCHEMA_PATH) as s:
        schema = json.load(s)

    with open(INSTANCE_PATH) as i:
        instance = json.load(i)

    # Use Draft7Validator for instance validation
    validator = Draft7Validator(schema)
    errors = sorted(validator.iter_errors(instance), key=lambda e: e.path)

    if errors:
        raise Exception(f"Governance instance validation failed: {errors}")

    return True

def validate_schema_hash():
    if not os.path.exists(LOCK_PATH):
        raise FileNotFoundError(f"Lock file missing: {LOCK_PATH}")

    with open(LOCK_PATH) as f:
        lock_data = json.load(f)

    expected_hash = lock_data.get("governance_schema_hash")
    actual_hash = compute_sha256(SCHEMA_PATH)

    if expected_hash != actual_hash:
        raise Exception(f"Governance schema hash mismatch detected.\nExpected: {expected_hash}\nActual:   {actual_hash}")

    return True

def validate_instance_hash():
    if not os.path.exists(LOCK_PATH):
        raise FileNotFoundError(f"Lock file missing: {LOCK_PATH}")

    with open(LOCK_PATH) as f:
        lock_data = json.load(f)

    expected_hash = lock_data.get("governance_instance_hash")
    if not expected_hash:
        raise Exception("governance_instance_hash missing in lock file.")

    actual_hash = compute_sha256(INSTANCE_PATH)

    if expected_hash != actual_hash:
        raise Exception(f"Governance instance hash mismatch detected.\nExpected: {expected_hash}\nActual:   {actual_hash}")

    return True

def validate_signature_integrity():
    # Calling the verified existence in signature_manager
    if not verify_all_governance_files():
        raise Exception("Digital signature verification failed for one or more governance files.")
    return True

def full_check():
    validate_schema_structure()
    validate_instance()
    validate_schema_hash()
    validate_instance_hash()
    validate_signature_integrity()
    return True

if __name__ == "__main__":
    try:
        full_check()
        print("Governance validation PASSED (Deterministic Mode).")
    except Exception as e:
        error_id = f"ERR-{datetime.now().strftime('%Y%m%d')}-{str(uuid.uuid4())[:8].upper()}"
        log_error(
            module="GOVERNANCE",
            error_id=error_id,
            description=str(e),
            root_cause="Validation failure",
            solution="Review schema or instance"
        )
        print(f"Governance validation FAILED: {e}")
        import sys
        sys.exit(1)

