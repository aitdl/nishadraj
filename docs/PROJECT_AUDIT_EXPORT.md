# Project Audit Report â€” NishadRaj OS

**Project**: NishadRaj OS  
**Founder**: Jawahar R Mallah  
**Organization**: AITDL  
**Audit Timestamp**: 2026-02-25T13:10:00Z  
**Security Status**: READ-ONLY / NON-DESTRUCTIVE  

---

## 1. Directory Tree Export (Governed Structure)

```text
D:.
?   aitdl
?   aitdl.pub
?   CONTRIBUTING.md
?   Jawahar.templates
?   README.md
?   task_registry.json
?   
+---agents
?       auditor_agent.py
?       builder_agent.py
?       guardian_agent.py
?       planner_agent.py
?       
+---docs
?       BRAND_POSITIONING.md
?       CHANGE_IMPACT_LOG.md
?       DOCUMENTATION_MANIFEST.md
?       ERROR_REGISTRY.md
?       INSTITUTIONAL_DECLARATION.md
?       MODULE_STATUS_LEDGER.json
?       PROJECT_RENAME_COMMAND_NISHADRAJ_OS.md
?       PUBLIC_LAUNCH_PLAN.md
?       ROADMAP_PUBLIC.md
?       TASK_LOG.md
?       TRANSPARENCY_DASHBOARD_SPEC.md
?       
+---financial
?       ENDOWMENT_STRUCTURE.md
?       SUSTAINABLE_REVENUE_MODEL.md
?       
+---governance
?       ai-governance.schema.json
?       file_header_templates.json
?       governance.lock.json
?       
+---institutional
?       ACADEMIC_PARTNERSHIP_FRAMEWORK.md
?       ADVISORY_COUNCIL_STRUCTURE.md
?       FOUNDATION_MODEL.md
?       FOUNDING_CHARTER.md
?       GOVERNANCE_NEUTRALITY_POLICY.md
?       INSTITUTIONAL_ENGAGEMENT_MODEL.md
?       POLICY_FRAMEWORK.md
?       SOVEREIGN_HOSTING_ARCHITECTURE.md
?       TRADEMARK_STRATEGY.md
?       
+---legal
?       CONTRIBUTOR_LICENSE_AGREEMENT.md
?       LICENSE.md
?       OPEN_SOURCE_POLICY.md
?       OWNERSHIP_DECLARATION.md
?       
+---public
?   +---github
?   ?       ORG_PROFILE_README.md
?   ?       
?   +---strategy
?   ?       ACADEMIC_OUTREACH_PACKET.md
?   ?       GLOBAL_OUTREACH_MODEL.md
?   ?       
?   +---website
?   ?       LANDING_PAGE_COPY.md
?   ?       
?   +---whitepaper
?           NISHADRAJ_OS_WHITEPAPER.md
?           
+---security
?       fork_monitor.py
?       fork_registry.json
?       signature_registry.json
?       
+---services
?   +---api
?       ?   Dockerfile
?       ?   requirements.txt
?       ?   
?       +---alembic
?       +---app
?           ?   main.py
?           ?   
?           +---core
?           ?       config.py
?           ?       governance_hook.py
?           ?       roles.py
?           ?       security.py
?           ?       
?           +---database
?           ?       base.py
?           ?       session.py
?           ?       
?           +---routes
?                   health.py
?                   
+---src
?   +---dashboard
?           transparency_api.py
?           
+---system
    ?   signature_manager.py
    ?   task_engine.py
    ?   task_registry.json
    ?   validator_agent.py
```

---

## 2. Governance File Export

### 2.1 ai-governance.schema.json (v1.2.0)
```json
{
    "_meta": {
        "project": "NishadRaj OS",
        "author": "Jawahar R Mallah",
        "role": "Software Architect",
        "organization": "AITDL",
        "websites": [
            "https://aitdl.com",
            "https://nishadraj.com"
        ],
        "governance_version": "1.2.0",
        "copyright": "Copyright © AITDL | NISHADRAJ",
        "usage": "All Rights Reserved"
    },
    "$schema": "http://json-schema.org/draft-07/schema#",
    "title": "NishadRaj OS Governance Schema",
    "description": "Deterministic enforcement layer for autonomous AI operations.",
    "version": "1.2.0",
    "status": "LOCKED",
    "type": "object",
    "additionalProperties": false,
    "properties": {
        "execution_model": {
            "type": "string",
            "const": "strict_sequential",
            "description": "Strict sequential execution model enforcement."
        },
        "enforcement_rules": {
            "type": "object",
            "properties": {
                "dependency_enforcement": { "type": "boolean", "const": true },
                "documentation_mandatory": { "type": "boolean", "const": true },
                "code_integrity_check": { "type": "boolean", "const": true },
                "maintainability_standards": { "type": "boolean", "const": true }
            }
        },
        "protocols": {
            "type": "object",
            "properties": {
                "error_handling": { "type": "string", "const": "strict" },
                "review_protocol": { "type": "string", "const": "mandatory" },
                "pre_execution_validation": { "type": "boolean", "const": true }
            }
        },
        "lifecycle_control": {
            "type": "object",
            "properties": {
                "autonomous_control": { "type": "boolean", "const": true },
                "authorization_gating": { "type": "boolean", "const": true }
            }
        },
        "author_attribution_policy": {
            "type": "object",
            "properties": {
                "mandatory": { "type": "boolean", "const": true },
                "author_name": { "type": "string", "default": "Jawahar R Mallah" },
                "require_in_all_generated_files": { "type": "boolean", "const": true }
            }
        }
    },
    "required": [
        "execution_model", "enforcement_rules", "protocols", "lifecycle_control", 
        "legal_enforcement", "author_attribution_policy", "open_source_mode", 
        "trademark_protection", "hybrid_expansion_layer", "block_if_schema_mismatch", 
        "block_execution_if_missing"
    ]
}
```

### 2.2 governance.lock.json
```json
{
    "_meta": {
        "project": "NishadRaj OS",
        "author": "Jawahar R Mallah",
        "governance_version": "1.2.0"
    },
    "governance_schema_hash": "B2F01B25584FE8534CB7725FFAE9BFFB2E772E9D0B4AC742AF1442C2C543E671",
    "digital_signature_enforced": true,
    "signature_algorithm": "RSA-4096",
    "system_status": "ACTIVE",
    "backend_status": "GOVERNED",
    "hybrid_expansion_status": "ACTIVE"
}
```

### 2.3 task_registry.json
```json
{
    "tasks": [
        {
            "id": "INIT-001",
            "description": "Governance Layer Initialization",
            "status": "IN_PROGRESS"
        },
        {
            "id": "BACKEND_CORE_001",
            "name": "Initialize FastAPI Backend Core",
            "status": "COMPLETED",
            "risk_level": "LOW"
        }
    ]
}
```

---

## 3. Backend Structure Export (/services/api)

| Name | Size (Bytes) | Last Modified |
|------|--------------|---------------|
| Dockerfile | 661 | 2026-02-25 12:56:54 |
| requirements.txt | 205 | 2026-02-25 12:56:27 |
| app/main.py | 957 | 2026-02-25 12:56:36 |
| app/core/config.py | 745 | 2026-02-25 12:56:47 |
| app/core/governance_hook.py | 553 | 2026-02-25 12:56:38 |
| app/core/roles.py | 571 | 2026-02-25 12:56:49 |
| app/core/security.py | 992 | 2026-02-25 12:56:51 |
| app/routes/health.py | 488 | 2026-02-25 12:56:39 |

---

## 4. Hash Report

```json
{
  "schema_hash": "B2F01B25584FE8534CB7725FFAE9BFFB2E772E9D0B4AC742AF1442C2C543E671",
  "lock_hash": "75AECE76A14D0462A289D3B019EA38401A9BBDBE2225B2AE8D2A1008BDF0311A",
  "registry_hash": "72715F340A3F46F4059944047DAB4EBE639819864C0EA28328F3C36A606C5011"
}
```

---

## 5. Status Summary

```json
{
  "governance_version": "1.2.0",
  "backend_present": true,
  "hybrid_expansion_active": true,
  "hard_enforcement_mode": true,
  "signature_enforced": true
}
```

---
**Audit Certified: NishadRaj OS Auditor Agent | AITDL**

