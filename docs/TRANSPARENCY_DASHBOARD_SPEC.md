Project: NishadRaj OS
Organization: AITDL | NISHADRAJ
Role: Software Architect
Organization: AITDL
Websites: https://aitdl.com | https://nishadraj.com
Governance Version: 1.1.0
This file is part of NishadRaj OS.
Licensed under AGPL-3.0 with Additional Governance Protection Terms.
Copyright © AITDL | NISHADRAJ
---
# Transparency Dashboard Specification

The NishadRaj OS Transparency Dashboard provides real-time public access to the system's governance and security metrics.

## Key Metrics Exposed

- **Governance Version**: The active version of the AI governance layer.
- **Schema Hash**: SHA-256 fingerprint of the mandatory governance rules.
- **Signature Status**: Deterministic verification of system cryptographic integrity.
- **Task Completion %**: Progress of registered autonomous tasks from `task_registry.json`.
- **System Mode**: Current operational state (`ACTIVE` or `PROTECTED`).
- **Security Audit Status**: Detailed logs of last preflight checks and validation results.
- **Contributor Stats**: Anonymous totals of active builders and planners.

## Data Access Policy
- **Read-Only**: All transparency endpoints are strictly read-only. No external write operations are permitted.
- **Frequency**: Metrics are cached and updated every 10 minutes or upon significant governance events.
- **Integrity**: Each metric is cryptographically signed at the source.

