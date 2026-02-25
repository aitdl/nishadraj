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
import sys
import argparse
import shutil
from datetime import datetime

# Local imports
try:
    from validator_agent import full_check, compute_sha256, SCHEMA_PATH, LOCK_PATH
    from signature_manager import sign_governance_files
except ImportError:
    # If run from root
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
    from system.validator_agent import full_check, compute_sha256, SCHEMA_PATH, LOCK_PATH
    from system.signature_manager import sign_governance_files

IMPACT_LOG_PATH = "docs/CHANGE_IMPACT_LOG.md"

def parse_version(v_str):
    return list(map(int, v_str.split('.')))

def format_version(v_list):
    return ".".join(map(str, v_list))

def increment_version(current_version, mode):
    v = parse_version(current_version)
    if mode == 'major':
        v[0] += 1
        v[1] = 0
        v[2] = 0
    elif mode == 'minor':
        v[1] += 1
        v[2] = 0
    elif mode == 'patch':
        v[2] += 1
    return format_version(v)

def backup_files():
    backups = {}
    for path in [SCHEMA_PATH, LOCK_PATH, IMPACT_LOG_PATH]:
        if os.path.exists(path):
            backup_path = path + ".bak"
            shutil.copy2(path, backup_path)
            backups[path] = backup_path
    return backups

def restore_backups(backups):
    for original, backup in backups.items():
        if os.path.exists(backup):
            shutil.move(backup, original)
            print(f"Restored backup for {original}")

def cleanup_backups(backups):
    for backup in backups.values():
        if os.path.exists(backup):
            os.remove(backup)

def log_upgrade(new_version):
    entry = f"| GOV_UPGRADE_{new_version} | Governance Level | Upgraded governance to v{new_version}. | Automatic bump via governance_upgrade.py |"
    # Note: The above is a simplified log entry for the table in CHANGE_IMPACT_LOG.md
    # We'll use a more generic format that matches the existing table structure
    now = datetime.now().strftime("%Y-%m-%d")
    log_line = f"| GOV_UPGRADE_{new_version} | /governance/* | Upgraded governance to v{new_version}. | Version: {new_version}, Status: SUCCESS, Time: {now}. |\n"
    
    with open(IMPACT_LOG_PATH, "a") as f:
        f.write(log_line)

def run_upgrade():
    parser = argparse.ArgumentParser(description="NishadRaj OS Governance Upgrade Tool")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--major", action="store_true")
    group.add_argument("--minor", action="store_true")
    group.add_argument("--patch", action="store_true")
    
    args = parser.parse_args()
    
    if args.major: mode = 'major'
    elif args.minor: mode = 'minor'
    else: mode = 'patch'
    
    backups = backup_files()
    
    try:
        # 1. Load current version from schema
        with open(SCHEMA_PATH, 'r') as f:
            schema = json.load(f)
        
        current_version = schema.get('version', '0.0.0')
        new_version = increment_version(current_version, mode)
        
        print(f"Upgrading governance from v{current_version} to v{new_version}...")
        
        # 2. Update Schema
        schema['version'] = new_version
        if '_meta' in schema:
            schema['_meta']['governance_version'] = new_version
            
        with open(SCHEMA_PATH, 'w') as f:
            json.dump(schema, f, indent=4)
        
        # 3. Update Lock File
        with open(LOCK_PATH, 'r') as f:
            lock_data = json.load(f)
        
        if '_meta' in lock_data:
            lock_data['_meta']['governance_version'] = new_version
            
        # Recompute hash of schema
        schema_hash = compute_sha256(SCHEMA_PATH)
        lock_data['governance_schema_hash'] = schema_hash
        
        with open(LOCK_PATH, 'w') as f:
            json.dump(lock_data, f, indent=4)
            
        # 4. Re-sign governance files
        print("Re-signing governance files...")
        sign_governance_files()
        
        # 5. Run full validation
        print("Running integrity validation...")
        if not full_check():
            raise Exception("Validator agent check failed post-upgrade.")
            
        # 6. Log event
        log_upgrade(new_version)
        
        cleanup_backups(backups)
        print(f"Governance upgraded successfully to v{new_version}")
        
    except Exception as e:
        print(f"ERROR: Upgrade failed: {e}")
        restore_backups(backups)
        sys.exit(1)

if __name__ == "__main__":
    run_upgrade()

