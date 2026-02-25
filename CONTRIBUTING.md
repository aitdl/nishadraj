# Contributing to NishadRaj OS

Welcome! We appreciate your interest in contributing to NishadRaj OS. This project is unique because it is protected by a deterministic AI Governance Layer.

## Setup Instructions
1. Fork the repository.
2. Install dependencies: `pip install cryptography`.
3. Ensure your environment has Python 3.8+ installed.

## Governance Enforcement
This system enforces strict rules via a **Validator Agent** and a **Digital Signature Layer**:
- **Author Attribution**: Every file must contain the correct author and license header.
- **Integrity**: Governance schemas and registries are hashed and signed.
- **Strict Sequence**: Tasks must be executed in the order defined in the Task Registry.

## Contribution Workflow
1. **Registered Tasks**: Only changes that correspond to a registered task will pass the validator.
2. **Preflight Check**: Run `python system/validator_agent.py [TASK_ID]` before submitting your PR to ensure your changes are compliant.
3. **Header Requirements**: Ensure all new files include the mandatory AGPL-3.0 + Governance header.

## Coding Standards
- Follow PEP 8 for Python.
- Maintain high code-to-comment ratios.
- Do not modify files in `/governance` or `/security` unless part of an authorized governance upgrade.

**Copyright © AITDL | NISHADRAJ**
**All Rights Reserved**

