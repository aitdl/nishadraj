"""
Project: NishadRaj OS
Organization: AITDL | NISHADRAJ
Organization: AITDL
License: AGPL-3.0 + Governance Protection Terms
Copyright © AITDL | NISHADRAJ
"""

from enum import Enum

class UserRole(str, Enum):
    GOVERNOR = "governor"      # Chief Architect / Founder
    VALIDATOR = "validator"    # System validation agents
    COORDINATOR = "coordinator" # Regional Node managers
    FELLOW = "fellow"          # Academic researchers
    CONTRIBUTOR = "contributor" # Open source developers
    USER = "user"              # Standard platform users

