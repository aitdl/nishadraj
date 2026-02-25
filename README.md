# NishadRaj OS

**Founder:** Jawahar R Mallah  
**Organization:** AITDL  
**Architecture Mode:** Governance-Enforced Deterministic Backend  
**Security Level:** Institutional Ready  

---

## 🏛 Overview

NishadRaj OS is a governance-driven backend platform designed with deterministic enforcement, cryptographic integrity, structured auditability, and institutional-grade access control.

This system is not a prototype framework — it is a structured operating backbone.

---

## 🔐 Core Principles

- Strict sequential task execution
- Schema + Instance governance locking
- SHA256 hash verification
- RSA signature enforcement
- Module-wise documentation logging
- Controlled migration review protocol
- Backend-controlled authentication
- No direct database exposure

---

## 🧠 Architecture

```
Frontend
↓
FastAPI Backend (JWT + Optional 2FA + RBAC + Governance)
↓
PostgreSQL (Docker DEV / Supabase PROD)
```

Supabase is used strictly as managed PostgreSQL infrastructure.  
No Supabase Auth is used.

---

## 🔒 Governance Layer

**Location:**
```
/governance
/system/validator_agent.py
/system/governance_upgrade.py
```

**Features:**
- JSON Schema enforcement
- Governance instance validation
- Hash locking
- Signature verification
- Execution blocking on mismatch

**Run validation:**
```bash
python system/validator_agent.py
```

---

## 🗄 Database Strategy

Environment-driven configuration:

- **DEV** → Docker PostgreSQL
- **PROD** → Supabase PostgreSQL
- No multi-runtime switching
- No direct frontend DB access

**Migration workflow:**
1. Generate in DEV
2. SQL preview review
3. Approve
4. Apply
5. Log in documentation

---

## 🔑 Authentication (AUTH_002)

- Email + Password
- Optional TOTP (2FA)
- JWT tokens (30 min expiry)
- Account lockout (5 failed attempts)
- Role-based access (`ADMIN` / `EDITOR` / `AUDITOR`)
- Audit logging enabled
- Governance preflight enforced

---

## 📄 Documentation Structure

**Central:**
```
/docs
```

**Module-wise:**
```
/docs/modules
```

All module actions, errors, and changes are logged automatically.

---

## 🚦 Execution Rules

No task is marked `COMPLETE` without:
- Governance validation pass
- Documentation entry created
- Signature integrity verified

---

## ⚖ License

AGPL-3.0 + Governance Protection Terms  
All Rights Reserved © Jawahar R Mallah | AITDL

---

## 🔧 Development Setup (DEV)

1. Run Docker PostgreSQL
2. Configure `DATABASE_URL_DEV`
3. Run migration review protocol
4. Apply after approval
5. Validate governance

---

## 📊 System Status

| Component | Status |
|-----------|--------|
| Governance | LOCKED |
| Backend Core | ACTIVE |
| AUTH_002 | ACTIVE |
| Migration Protocol | REVIEW_REQUIRED |
| Multi-Environment DB | ENABLED |

---

*NishadRaj OS is built for structured, transparent, governance-first system development.*
