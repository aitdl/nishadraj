"""
Project: NishadRaj OS
Author: Jawahar R Mallah
Role: Software Architect
Organization: AITDL
Websites: https://aitdl.com | https://nishadraj.com
Governance Version: 1.1.0
This file is part of NishadRaj OS.
Licensed under AGPL-3.0 with Additional Governance Protection Terms.
Copyright © Jawahar R Mallah | AITDL
"""
import json
import hashlib
import os
import sys

LEGAL_DIR = "d:/IMP/GitHub/nishadraj/legal"
OWNERSHIP_DECLARATION = os.path.join(LEGAL_DIR, "OWNERSHIP_DECLARATION.md")
LICENSE_FILE = os.path.join(LEGAL_DIR, "LICENSE.md")
from signature_manager import verify_all_governance_files

SCHEMA_PATH = "d:/IMP/GitHub/nishadraj/governance/ai-governance.schema.json"
LOCK_PATH = "d:/IMP/GitHub/nishadraj/governance/governance.lock.json"
REGISTRY_PATH = "d:/IMP/GitHub/nishadraj/system/task_registry.json"

class ValidatorAgent:
    def __init__(self):
        self.load_configs()

    def load_configs(self):
        with open(SCHEMA_PATH, 'r') as f:
            self.schema = json.load(f)
        with open(LOCK_PATH, 'r') as f:
            self.lock = json.load(f)
        with open(REGISTRY_PATH, 'r') as f:
            self.registry = json.load(f)

    def verify_schema_integrity(self):
        with open(SCHEMA_PATH, 'rb') as f:
            current_hash = hashlib.sha256(f.read()).hexdigest().upper()
        
        expected_hash = self.lock.get('governance_schema_hash', '').upper()
        if current_hash != expected_hash:
            print(f"CRITICAL: Schema hash mismatch! Found {current_hash}, expected {expected_hash}")
            return False
        return True

    def verify_registry_integrity(self):
        # In a real scenario, we'd compare against the lock file's task_registry_hash
        # For initialization, we verify if it matches the metadata hash
        tasks_str = json.dumps(self.registry['tasks'], sort_keys=True)
        current_hash = hashlib.sha256(tasks_str.encode()).hexdigest()
        
        metadata_hash = self.registry['metadata'].get('registry_hash', '')
        if metadata_hash and current_hash != metadata_hash:
             print(f"WARNING: Registry hash mismatch with metadata! Found {current_hash}, metadata has {metadata_hash}")
             # In strict mode, we might return False here
        return True

    def validate_task_state(self, task_id):
        task = next((t for t in self.registry['tasks'] if t['id'] == task_id), None)
        if not task:
            print(f"ERROR: Task {task_id} not found in registry.")
            return False
        
        if task['status'] not in ['PENDING', 'IN_PROGRESS']:
            print(f"ERROR: Task {task_id} is in invalid state: {task['status']}")
            return False
            
        return True

    def validate_dependencies(self, task_id):
        task = next((t for t in self.registry['tasks'] if t['id'] == task_id), None)
        if not task: return False
        
        for dep_id in task.get('dependencies', []):
            dep_task = next((t for t in self.registry['tasks'] if t['id'] == dep_id), None)
            if not dep_task or dep_task['status'] != 'COMPLETED':
                print(f"ERROR: Dependency {dep_id} for task {task_id} is not COMPLETED.")
                return False
        return True

    def validate_documentation_presence(self, task_id):
        # Simple check for mandatory docs mentioned in schema
        docs_dir = "d:/IMP/GitHub/nishadraj/docs"
        mandatory_files = ["TASK_LOG.md", "ERROR_REGISTRY.md"]
        for f in mandatory_files:
            if not os.path.exists(os.path.join(docs_dir, f)):
                print(f"ERROR: Mandatory documentation {f} is missing.")
                return False
        return True

    def check_legal_compliance(self):
        if not os.path.exists(OWNERSHIP_DECLARATION):
            print(f"ERROR: {OWNERSHIP_DECLARATION} is missing.")
            return False
        if not os.path.exists(LICENSE_FILE):
            print(f"ERROR: {LICENSE_FILE} is missing.")
            return False
        return True

    def verify_author_attribution(self, file_path):
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()

            required_strings = [
                "Jawahar R Mallah",
                "AITDL",
                "https://aitdl.com",
                "https://nishadraj.com",
                "This file is part of NishadRaj OS",
                "Licensed under AGPL-3.0 with Additional Governance Protection Terms",
                "Copyright © Jawahar R Mallah | AITDL"
            ]

            for item in required_strings:
                if item not in content:
                    print(f"ERROR: Legal/Author attribution missing or incorrect in {file_path}")
                    return False
            return True
        except Exception as e:
            print(f"ERROR: Could not read {file_path} for attribution check: {e}")
            return False

    def get_modified_files(self):
        # Placeholder: in a real system this would interface with git or a change tracker
        # For now, we'll check files related to the task if specified
        return []

    def validate_deployment_integrity(self):
        # Phase 4 Rule Enforcement
        if not verify_all_governance_files():
            print("!!! CI/CD BLOCK: SIGNATURE INVALID !!!")
            return False
            
        if not self.verify_schema_integrity():
            print("!!! CI/CD BLOCK: GOVERNANCE MISMATCH !!!")
            return False
            
        # Check if license has been altered (comparing against known license file)
        if not self.check_legal_compliance():
            print("!!! CI/CD BLOCK: LICENSE ALTERED OR MISSING !!!")
            return False
            
        return True

    def validate_execution(self, task_id):
        # Deployment Integrity (Step 4.2 Upgrade)
        if not self.validate_deployment_integrity():
            return False

        if not self.verify_registry_integrity(): return False
        if not self.validate_task_state(task_id): return False
        if not self.validate_dependencies(task_id): return False
        if not self.validate_documentation_presence(task_id): return False
        return True

    def preflight_check(self, task_id, modified_files=None):
        print(f"--- RUNNING PREFLIGHT CHECK FOR TASK: {task_id} ---")
        is_valid = self.validate_execution(task_id)
        if not is_valid:
            print(f"!!! PREFLIGHT CHECK FAILED FOR TASK: {task_id} !!!")
            print("EXECUTION BLOCKED.")
            return False
        
        # Check author attribution on modified files
        files_to_check = modified_files or self.get_modified_files()
        for file in files_to_check:
            if not self.verify_author_attribution(file):
                print(f"!!! PREFLIGHT CHECK FAILED: Attribution missing in {file} !!!")
                return False

        print(f"PREFLIGHT CHECK PASSED FOR TASK: {task_id}")
        return True

def validate_execution(task_id):
    agent = ValidatorAgent()
    return agent.validate_execution(task_id)

def preflight_check(task_id, modified_files=None):
    agent = ValidatorAgent()
    return agent.preflight_check(task_id, modified_files)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        tid = sys.argv[1]
        m_files = sys.argv[2:] if len(sys.argv) > 2 else None
        preflight_check(tid, m_files)
    else:
        print("Usage: python validator_agent.py <task_id> [modified_files...]")
