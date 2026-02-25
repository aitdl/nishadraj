# GOVERNANCE UPGRADE PROTOCOL â€” NishadRaj OS

> Project: NishadRaj OS
> Organization: AITDL | NISHADRAJ
> Organization: AITDL
> License: AGPL-3.0 + Governance Protection Terms
> Copyright © AITDL | NISHADRAJ

## 1. Purpose
- **Prevent unauthorized governance drift**: Ensure all changes to the governance layer are intentional, documented, and authorized.
- **Ensure deterministic enforcement continuity**: Guarantee that system behavior remains predictable and governed across version transitions.

## 2. Upgrade Eligibility Conditions
- **Version increment mandatory**: Any change to the governance schema or instance must be accompanied by a version bump.
- **Change justification required**: Documentation must clearly explain the rationale and impact of the upgrade.
- **Advisory review required**: If the institutional layer is active, upgrades must undergo advisory review.

## 3. Mandatory Upgrade Steps

### STEP 1 â€” Create Upgrade Proposal
- Document proposed changes in detail.
- Perform a comprehensive risk assessment.
- Review for backward compatibility with existing agents and services.

### STEP 2 â€” Increment Version
- Update version in `governance/ai-governance.schema.json`.
- Update `_meta.governance_version` in relevant artifacts and lock files.

### STEP 3 â€” Update Instance (if required)
- Modify `governance/governance.instance.json` to reflect new parameters or rules.

### STEP 4 â€” Recompute Hash
- Recompute the SHA256 hash of updated governance files.
- Update `governance/governance.lock.json` with new hashes.

### STEP 5 â€” Re-sign Governance Files
- Execute `python system/signature_manager.py` to re-sign all governed files.

### STEP 6 â€” Run Full Validation
- Execute `python system/validator_agent.py` and ensure a `PASS` status is returned.

### STEP 7 â€” Log Change
- Create an entry in `docs/CHANGE_IMPACT_LOG.md`.
- Use the tag format: `GOV_UPGRADE_vX.Y.Z`.

## 4. Breaking Change Protocol
- **Major version bump required**: Any change that relaxes enforcement or breaks compatibility.
- **Explicit migration notes**: Documentation must provide a clear path for existing nodes/services.
- **Manual approval required**: Direct authorization from the Founder is mandatory for breaking changes.

## 5. CI/CD Enforcement
- **Block deployment if**:
  - Version has not been incremented appropriately.
  - Governance hashes do not match the lock file.
  - Cryptographic signatures are missing or invalid.

## 6. Immutable Rules
- **Execution model cannot change**: The core operational logic (`strict_sequential`, etc.) is immutable.
- **Enforcement const flags cannot be relaxed**: Security and governance enforcement levels can only be increased or maintained.
- **additionalProperties cannot be removed**: Schema strictness (`additionalProperties: false`) must be maintained.

## 7. Authority Statement
- **Governance evolution authority**: Primary authority for governance evolution is retained by the Founder (**Jawahar R Mallah**).
- **Institutional override**: Institutional overrides are only valid via formal, documented resolution as defined in the advisory framework.

