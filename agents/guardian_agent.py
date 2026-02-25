"""
Project: NishadRaj OS
Organization: AITDL | NISHADRAJ
Role: Software Architect
Organization: AITDL
Websites: https://aitdl.com | https://nishadraj.com
Governance Version: 1.1.0
This file is part of NishadRaj OS.
Licensed under AGPL-3.0 with Additional Governance Protection Terms.
Copyright © AITDL | NISHADRAJ

Module: Guardian Agent
Objective: Final authority for system state changes and merges.
"""

import sys
sys.path.append("system")
from signature_manager import verify_signature

class GuardianAgent:
    def authorize_merge(self, files):
        print("GUARDIAN: Performing final audit before merge...")
        for f in files:
            if not verify_signature(f):
                print(f"GUARDIAN BLOCK: Unauthorized modification in {f}")
                return False
        print("GUARDIAN: Authorization GRANTED.")
        return True

if __name__ == "__main__":
    guardian = GuardianAgent()
    print("Guardian Agent initialized. Final Authority ACTIVE.")

