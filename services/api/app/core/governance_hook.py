"""
Project: NishadRaj OS
Organization: AITDL | NISHADRAJ
Organization: AITDL
License: AGPL-3.0 + Governance Protection Terms
Copyright © AITDL | NISHADRAJ
"""

import sys
import os

# Ensure root is in path for imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../")))

from system.validator_agent import full_check

def enforce_governance(task_id: str):
    """
    Enforces governance by running a full check using the system validator.
    """
    return full_check()

