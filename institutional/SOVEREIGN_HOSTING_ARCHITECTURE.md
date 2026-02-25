# Sovereign Hosting Architecture

## Hosting Tiers

### Tier 1: Public Cloud (Initial)
- **Usage**: Development environment, community testing.
- **Providers**: AWS/Azure/GCP (Region-locked to India).
- **Security**: Basic signature verification.

### Tier 2: Dedicated VPS
- **Usage**: Staging and core API hosting.
- **Security**: Full filesystem encryption, managed firewall.

### Tier 3: Private Cloud Cluster
- **Usage**: Production sovereign services.
- **Infrastructure**: Dedicated hardware in sovereign data centers.
- **Governance**: Multi-signature deployment required.

### Tier 4: On-Premise Sovereign Node
- **Usage**: High-security, ultra-sovereign environments.
- **Infrastructure**: Air-gapped or restricted network hardware.
- **Governance**: Physical validation of deployment keys.

## Data Residency Compliance
- No user data shall leave the sovereign jurisdiction (India) unless explicitly authorized for cross-border services.
- Metadata must be anonymized before any telemetry.

## Backup & Recovery
- **Policy**: Daily encrypted backups to secondary sovereign nodes.
- **Signature Verification**: Backups must be re-validated for signature integrity before restoration.
- **Air-Gapped Copy**: Monthly physical backup stored in a secure governance vault.

## Deployment Integrity
- **CI/CD Rule**: No deployment is permitted if the `governance.lock.json` hash or any digital signature fails the `validator_agent`.
