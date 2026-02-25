"""
Project: NishadRaj OS
Organization: AITDL | NISHADRAJ
Organization: AITDL
License: AGPL-3.0 + Governance Protection Terms
Copyright © AITDL | NISHADRAJ
"""

import os
import json
from datetime import datetime

# Absolute paths for documentation files
DOCS_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "docs"))
MODULE_DOCS_DIR = os.path.join(DOCS_DIR, "modules")
TASK_LOG_PATH = os.path.join(DOCS_DIR, "TASK_LOG.md")
ERROR_REGISTRY_PATH = os.path.join(DOCS_DIR, "ERROR_REGISTRY.md")
CHANGE_LOG_PATH = os.path.join(DOCS_DIR, "CHANGE_IMPACT_LOG.md")
LEDGER_PATH = os.path.join(DOCS_DIR, "MODULE_STATUS_LEDGER.json")

def _ensure_module_file(module):
    """Ensure module-specific log file exists."""
    if not os.path.exists(MODULE_DOCS_DIR):
        os.makedirs(MODULE_DOCS_DIR)
    
    module_file = os.path.join(MODULE_DOCS_DIR, f"{module}.md")
    if not os.path.exists(module_file):
        with open(module_file, "w") as f:
            f.write(f"# {module} Module Logs\n\nRegistry of all module-specific events.\n")
    return module_file

def _append_to_file(filepath, content):
    """Append content to file with hard error handling."""
    try:
        with open(filepath, "a") as f:
            f.write(content)
        return True
    except Exception as e:
        print(f"CRITICAL: Failed to write to {filepath}: {e}")
        return False

def log_task_event(module, task_id, status, notes=""):
    """Append to TASK_LOG.md and module-specific file in card format."""
    timestamp = datetime.now().isoformat()
    entry = f"""
--------------------------------
TASK_ID: {task_id}
MODULE: {module}
STATUS: {status}
NOTES: {notes}
TIMESTAMP: {timestamp}
--------------------------------
"""
    # 1. Append to Central Docs
    success1 = _append_to_file(TASK_LOG_PATH, entry)
    
    # 2. Append to Module Docs
    module_file = _ensure_module_file(module)
    success2 = _append_to_file(module_file, entry)
    
    if not (success1 and success2):
        raise RuntimeError(f"Logging failed for task {task_id}")
    return True

def log_error(module, error_id, description, root_cause, solution):
    """Append to ERROR_REGISTRY.md and module-specific file."""
    timestamp = datetime.now().isoformat()
    entry = f"""
--------------------------------
ERROR_ID: {error_id}
MODULE: {module}
DESCRIPTION: {description}
ROOT_CAUSE: {root_cause}
SOLUTION: {solution}
STATUS: OPEN
TIMESTAMP: {timestamp}
--------------------------------
"""
    # 1. Append to Central Docs
    success1 = _append_to_file(ERROR_REGISTRY_PATH, entry)
    
    # 2. Append to Module Docs
    module_file = _ensure_module_file(module)
    success2 = _append_to_file(module_file, entry)
    
    if not (success1 and success2):
        raise RuntimeError(f"Error logging failed for {error_id}")
    return True

def log_change(module, change_id, impact, risk_level):
    """Append to CHANGE_IMPACT_LOG.md and module-specific file."""
    timestamp = datetime.now().isoformat()
    entry = f"""
--------------------------------
CHANGE_ID: {change_id}
MODULE: {module}
IMPACT: {impact}
RISK_LEVEL: {risk_level}
TIMESTAMP: {timestamp}
--------------------------------
"""
    # 1. Append to Central Docs
    success1 = _append_to_file(CHANGE_LOG_PATH, entry)
    
    # 2. Append to Module Docs
    module_file = _ensure_module_file(module)
    success2 = _append_to_file(module_file, entry)
    
    if not (success1 and success2):
        raise RuntimeError(f"Change logging failed for {change_id}")
    return True

def update_module_status(module, status):
    """Update MODULE_STATUS_LEDGER.json."""
    try:
        with open(LEDGER_PATH, "r") as f:
            ledger = json.load(f)
        
        # Simple Key-Value for this phase
        if "modules" not in ledger:
            ledger["modules"] = {}
        
        # If it's a list (old format), convert it or handle it
        if isinstance(ledger["modules"], list):
            new_modules = {}
            for m in ledger["modules"]:
                new_modules[m["name"]] = m["status"]
            ledger["modules"] = new_modules

        ledger["modules"][module] = status
        ledger["last_audit"] = datetime.now().strftime("%Y-%m-%d")
        
        with open(LEDGER_PATH, "w") as f:
            json.dump(ledger, f, indent=4)
        return True
    except Exception as e:
        print(f"CRITICAL: Failed to update MODULE_STATUS_LEDGER.json: {e}")
        return False

