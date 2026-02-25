# AUTH Module Logs

Registry of all module-specific events.

--------------------------------
CHANGE_ID: AUTH_MODULE_002_OPTIONAL_2FA
MODULE: AUTH
IMPACT: Authentication + TOTP enabled
RISK_LEVEL: MEDIUM
TIMESTAMP: 2026-02-25T14:19:36.538721
--------------------------------

--------------------------------
TASK_ID: AUTH_002
MODULE: AUTH
STATUS: COMPLETED
NOTES: Institutional Ready Auth implemented
TIMESTAMP: 2026-02-25T14:24:45.535902
--------------------------------

## MIGRATION_REVIEW_AUTH_002
**Project**: NishadRaj OS  
**Status**: PENDING_APPROVAL  
**Timestamp**: 2026-02-25T14:58:00Z  

### 1. Tables Created
- `audit_logs`: Centralized security and governance event log.

### 2. Columns Installed
- `audit_logs.id` (UUID, PK)
- `audit_logs.event_type` (VARCHAR(100))
- `audit_logs.user_id` (UUID, FK -> users.id)
- `audit_logs.module` (VARCHAR(100), Default: 'AUTH')
- `audit_logs.description` (VARCHAR(255))
- `audit_logs.timestamp` (DATETIME, Default: now())
- `audit_logs.ip_address` (VARCHAR(45))
- `audit_logs.details` (JSON)
- `users.account_locked` (BOOLEAN, Default: false)

### 3. Constraints & Indexes
- `audit_logs_pkey`: PRIMARY KEY (id)
- `audit_logs_user_id_fkey`: FOREIGN KEY (user_id) REFERENCES users (id)

### 4. Review Summary
- **Drops**: NONE (consolidated view)
- **Security Level**: INSTITUTIONAL_READY
- **Action Required**: Manual SQL inspection of `migration_review_auth_002.sql` requested.

## MIGRATION_REVIEW_AUTH_002_DEV
**Environment**: DEV  
**Revision**: `84a1d5271cf2`  
**Status**: GENERATED_NOT_APPLIED  
**Timestamp**: 2026-02-25T15:33:00Z  
**Risk**: LOW  

### Safety Scan Result: ✅ PASSED
No destructive operations detected (`DROP`, `TRUNCATE`, `CASCADE`, `REVOKE`).

### Tables Created
- `users`: Core authentication table with RBAC, lockout, and 2FA columns.
- `audit_logs`: Centralized security event log for AUTH module.

### Columns (users)
| Column | Type | Notes |
|--------|------|-------|
| id | UUID | PK |
| email | VARCHAR(255) | UNIQUE INDEX |
| hashed_password | VARCHAR(255) | bcrypt |
| role | ENUM(userrole) | ADMIN/EDITOR/AUDITOR |
| is_active | BOOLEAN | Default: true |
| totp_secret | VARCHAR(32) | Nullable |
| is_2fa_enabled | BOOLEAN | Default: false |
| failed_login_attempts | INTEGER | Default: 0 |
| account_locked | BOOLEAN | Default: false |
| last_login_at | TIMESTAMP | Nullable |
| created_at | TIMESTAMP | Auto |
| updated_at | TIMESTAMP | Auto |

### Columns (audit_logs)
| Column | Type | Notes |
|--------|------|-------|
| id | UUID | PK |
| event_type | VARCHAR(100) | NOT NULL |
| user_id | UUID | FK → users.id |
| module | VARCHAR(100) | Default: AUTH |
| description | VARCHAR(255) | NOT NULL |
| timestamp | TIMESTAMP | Default: now() |
| ip_address | VARCHAR(45) | Nullable |
| details | JSON | Nullable |

### Indexes
- `ix_users_email` (UNIQUE) on `users.email`

### Constraints
- `users_pkey`: PRIMARY KEY (id)
- `audit_logs_pkey`: PRIMARY KEY (id)
- `audit_logs_user_id_fkey`: FOREIGN KEY (user_id) → users(id)

### Review Status: PENDING_APPROVAL

## MIGRATION_APPLIED_AUTH_002_DEV
**Environment**: DEV  
**Revision**: `84a1d5271cf2`  
**Status**: APPLIED  
**Timestamp**: 2026-02-25T15:39:00Z  
**auth_schema_state**: ACTIVE_DEV  

### Tables Verified Post-Apply ✅
| Table | Status | Columns |
|-------|--------|---------|
| `users` | ✅ ACTIVE | id, email, hashed_password, role, is_active, totp_secret, is_2fa_enabled, failed_login_attempts, account_locked, last_login_at, created_at, updated_at |
| `audit_logs` | ✅ ACTIVE | id, event_type, user_id, module, description, timestamp, ip_address, details |

### Final State
- **migration_status**: APPLIED_DEV
- **apply_status**: COMPLETE
- **auth_schema_state**: ACTIVE_DEV
