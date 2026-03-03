# Relback — System Architecture

**Stack:** Django 6.0 · Python 3.13 · Oracle Database (oracledb) · SQLite (dev/test) · Tailwind CSS + DaisyUI  
**Pattern:** Clean Architecture (Robert C. Martin) — strict dependency rule, inner layers never reference outer layers.

---

## 1. Architectural Overview

```
┌──────────────────────────────────────────────────────────────────────────┐
│  OUTER LAYER — Infrastructure & Delivery                                │
│                                                                          │
│  ┌─────────────────┐  ┌──────────────────────────────────────────────┐  │
│  │  Django Views   │  │  Templates (DaisyUI/Tailwind)                │  │
│  │  (HTTP adapter) │  │  base.html, reports.html, index.html, …      │  │
│  └────────┬────────┘  └──────────────────────────────────────────────┘  │
│           │ calls                                                        │
│  ┌────────▼────────────────────────────────────────────────────────────┐│
│  │  USE CASES (Interactors)              coreRelback/services/          ││
│  │  GetDashboardStatsUseCase                                            ││
│  │  AuditBackupUseCase                                                  ││
│  │  GetScheduleReportUseCase                                            ││
│  │  GenerateScheduleUseCase                                             ││
│  │  GetBackupDetailUseCase                                              ││
│  │  Create/Update/Delete CRUD use cases (Client, Host, Database, Policy)││
│  └────────┬────────────────────────────────────────────────────────────┘│
│           │ depends on (interfaces only)                                 │
│  ┌────────▼────────────────────────────────────────────────────────────┐│
│  │  GATEWAY INTERFACES (Ports)           coreRelback/gateways/          ││
│  │  IClientRepository                                                   ││
│  │  IHostRepository                                                     ││
│  │  IDatabaseRepository                                                 ││
│  │  IBackupPolicyRepository                                             ││
│  │  IScheduleRepository                                                 ││
│  │  IOracleRmanRepository                                               ││
│  └────────────────────────────────────────────────────────────────────-┘│
│           ▲                                                              │
│           │ implements                                                   │
│  ┌────────┴────────────────────────────────────────────────────────────┐│
│  │  CONCRETE REPOSITORIES                coreRelback/gateways/          ││
│  │  DjangoClientRepository      → Django ORM (SQLite / Oracle)         ││
│  │  DjangoHostRepository        → Django ORM                           ││
│  │  DjangoDatabaseRepository    → Django ORM                           ││
│  │  DjangoBackupPolicyRepository → Django ORM                          ││
│  │  DjangoScheduleRepository    → Django ORM                           ││
│  │  OracleRmanRepository        → python-oracledb (Thin mode)          ││
│  │  DemoRmanRepository          → in-memory fixture data (DEMO_MODE)   ││
│  └────────────────────────────────────────────────────────────────────-┘│
│                                                                          │
│  INNERMOST LAYER — Domain                                               │
│  ┌────────────────────────────────────────────────────────────────────┐ │
│  │  ENTITIES & VALUE OBJECTS             coreRelback/domain/entities.py │
│  │  ClientEntity, HostEntity, DatabaseEntity, BackupPolicyEntity        │
│  │  BackupJobResult, BackupLogEntry, ScheduleEntry, DashboardStats      │
│  │  BackupStatusValue (enum), BackupType (enum), PolicyStatus (enum)    │
│  └──────────────────────────────────────────────────────────────────── │
└──────────────────────────────────────────────────────────────────────────┘
```

### Dependency Rule

> Code dependencies always point **inward** — from Infrastructure → Use Cases → Entities.  
> Entities know nothing about Django. Use Cases know nothing about Oracle or HTTP.

---

## 2. Layer Details

### 2.1 Domain Layer — `coreRelback/domain/entities.py`

Pure Python dataclasses and enums. Zero imports from Django, Oracle, or any framework.

| Symbol | Type | Purpose |
|---|---|---|
| `ClientEntity` | `@dataclass` | Business representation of a backup client |
| `HostEntity` | `@dataclass` | Server/host that runs Oracle |
| `DatabaseEntity` | `@dataclass` | Oracle database instance |
| `BackupPolicyEntity` | `@dataclass` | RMAN backup policy with cron schedule |
| `ScheduleEntry` | `@dataclass` | Expanded cron forecast entry |
| `BackupJobResult` | `@dataclass` | One RMAN backup job from RC_RMAN_BACKUP_JOB_DETAILS |
| `BackupLogEntry` | `@dataclass` | One output line from RC_RMAN_OUTPUT |
| `DashboardStats` | `@dataclass` | Aggregated counts for dashboard |
| `BackupStatusValue` | `Enum` | COMPLETED / FAILED / RUNNING / WARNING / INTERRUPTED / UNKNOWN |
| `BackupType` | `Enum` | ARCHIVELOG / DB FULL / DB INCR / RECVR AREA / BACKUPSET |
| `PolicyStatus` | `Enum` | ACTIVE / INACTIVE |
| `BackupDestination` | `Enum` | DISK / SBT\_TAPE |

### 2.2 Gateway Interfaces — `coreRelback/gateways/interfaces.py`

Abstract base classes (Python `ABC`) that define the **ports**. Use cases depend only on these — they never import concrete repositories or ORM models.

| Interface | Methods |
|---|---|
| `IClientRepository` | `get_all`, `get_by_id`, `count`, `create`, `update`, `delete` |
| `IHostRepository` | `get_all`, `get_by_id`, `count`, `create`, `update`, `delete` |
| `IDatabaseRepository` | `get_all`, `get_by_id`, `count`, `create`, `update`, `delete` |
| `IBackupPolicyRepository` | `get_all`, `get_by_id`, `count`, `count_active`, `create`, `update`, `delete` |
| `IScheduleRepository` | `get_upcoming`, `delete_all`, `create_batch` |
| `IOracleRmanRepository` | `get_backup_jobs`, `get_running_jobs_count`, `get_backup_job_detail`, `get_backup_log` |

### 2.3 Concrete Repositories — `coreRelback/gateways/repositories.py`

| Class | Backend | Notes |
|---|---|---|
| `DjangoClientRepository` | Django ORM | Wraps `Client` model |
| `DjangoHostRepository` | Django ORM | Wraps `Host` model |
| `DjangoDatabaseRepository` | Django ORM | Wraps `Database` model |
| `DjangoBackupPolicyRepository` | Django ORM | Wraps `BackupPolicy` model |
| `DjangoScheduleRepository` | Django ORM | Wraps `Schedule` model |
| `OracleRmanRepository` | python-oracledb | Queries Oracle RMAN Catalog views (`RC_RMAN_BACKUP_JOB_DETAILS`, `RC_RMAN_OUTPUT`); returns empty lists when `ORACLE_CATALOG` setting is `None` |
| `DemoRmanRepository` | In-memory fixtures | Returns realistic fake RMAN data when `DEMO_MODE = True` in settings |

### 2.4 Use Cases — `coreRelback/services/use_cases.py`

One class per business action (Single Responsibility). Each constructor accepts interface types, never concrete classes.

| Use Case | Purpose |
|---|---|
| `GetDashboardStatsUseCase` | Aggregates counts for Dashboard |
| `GetScheduleReportUseCase` | Reads upcoming backup schedule by date range |
| `GenerateScheduleUseCase` | Expands cron policy fields into `Schedule` rows |
| `AuditBackupUseCase` | Correlates schedules with Oracle job results |
| `GetBackupDetailUseCase` | Fetches RMAN log lines for a specific job |
| `CreateClientUseCase` | Validates + creates a Client |
| `UpdateClientUseCase` | Validates + updates a Client |
| `DeleteClientUseCase` | Removes a Client |
| `CreateHostUseCase` | Validates + creates a Host |
| `UpdateHostUseCase` | Validates + updates a Host |
| `DeleteHostUseCase` | Removes a Host |
| `CreateDatabaseUseCase` | Validates + creates a Database |
| `UpdateDatabaseUseCase` | Validates + updates a Database |
| `DeleteDatabaseUseCase` | Removes a Database |
| `CreateBackupPolicyUseCase` | Validates + creates a BackupPolicy |
| `UpdateBackupPolicyUseCase` | Validates + updates a BackupPolicy |
| `DeleteBackupPolicyUseCase` | Removes a BackupPolicy |

### 2.5 Views — `coreRelback/views.py`

Django views act as **HTTP adapters only**. They:
1. Parse the HTTP request
2. Instantiate concrete repositories and inject them into a use case
3. Execute the use case
4. Pass the returned entities to a template

Views never contain business logic. They never call `Client.objects.filter(...)` directly.

### 2.6 Oracle RMAN Gateway — `coreRelback/gateways/oracle_catalog.py`

Implemented with `python-oracledb` in **Thin mode** (no Oracle Client required).  
Connection target is configured via `settings.ORACLE_CATALOG`:

```python
ORACLE_CATALOG = {
    "user": "rman_user",
    "password": "...",
    "dsn": "host:1521/CATALOG",
}
```

When `ORACLE_CATALOG = None`, `OracleRmanRepository` returns empty lists — the UI renders an "Oracle catalog not available" banner without crashing.

---

## 3. Data Model

```
RelbackUser
    │
    └── created_by / updated_by (FK on all entities below)

Client
    ├── Host (FK: id_client)
    │     └── Database (FK: id_client, id_host)
    │           └── BackupPolicy (FK: id_client, id_host, id_database)
    │                 └── Schedule (FK: id_policy)
    │                 └── CronDay / CronHour / CronMinute / CronMonth / CronDayWeek / CronYear
    └── BackupPolicy (FK: id_client)
```

### Key Models

| Model | Table | Purpose |
|---|---|---|
| `RelbackUser` | `users` | Custom user — no AbstractBaseUser, own password hashing |
| `Client` | `clients` | Organizational unit (customer / business unit) |
| `Host` | `hosts` | Physical/virtual server running Oracle |
| `Database` | `databases` | Oracle instance (identified by `dbid`) |
| `BackupPolicy` | `backup_policies` | RMAN backup schedule definition |
| `Schedule` | `schedules` | Expanded forecast entry (policy × time) |
| `VwBackupPolicies` | `vw_backup_policies` | Oracle view, `managed=False` |

---

## 4. Authentication

Custom session-based auth using `RelbackUser`. No Django `AbstractBaseUser`.

| Component | Location |
|---|---|
| `RelbackBackend` | `coreRelback/backends.py` — custom auth backend |
| `LoginView` | `coreRelback/views.py` |
| `LogoutView` | `coreRelback/views.py` |
| `RegisterView` | `coreRelback/views.py` |
| `LoginRequiredMixin` | Applied to all CRUD views and dashboard |

Session is stored in `django.contrib.sessions` (database-backed in production, file in dev).

---

## 5. Frontend Architecture

```
theme/                          ← Django app managed by django-tailwind
  static_src/
    src/styles.css              ← Entry point: @tailwind base/components/utilities
    tailwind.config.js          ← DaisyUI plugin, relback_light/dark themes
    package.json                ← tailwindcss 3.x, daisyui 4.x, autoprefixer
  static/
    css/dist/styles.css         ← Compiled output (minified, ~100 KB)

coreRelback/templates/
  base.html                     ← DaisyUI drawer layout, theme switcher
  index.html                    ← Dashboard: DaisyUI stats component
  reports.html                  ← RMAN job table + badge status
  reportsReadLog.html           ← RMAN log detail lines
  clients.html / hosts.html … ← CRUD list views
  *_form.html                   ← DaisyUI form-control inputs
  auth/login.html               ← DaisyUI card form
```

### DaisyUI Theme Tokens

| Token | relback\_dark | Purpose |
|---|---|---|
| `primary` | `#C74634` | Oracle Red — buttons, badges |
| `base-100` | `#0f172a` | Page background |
| `success` | `#16a34a` | COMPLETED status |
| `error` | `#dc2626` | FAILED status |
| `warning` | `#d97706` | WARNING / RUNNING\_WITH\_ISSUES |
| `info` | `#2563eb` | RUNNING status |
| `neutral` | `#334155` | UNKNOWN / headers |

---

## 6. CI Pipeline

```
.github/workflows/ci.yml
  ├── check-and-test       Gate 1: django check | Gate 2: 46 domain tests | Gate 3: 37 integration tests
  ├── sql-lint             sqlfluff lint databaseProject/ (config: .sqlfluff, exclusions: .sqlfluffignore)
  ├── template-lint        djlint coreRelback/templates/ --lint (config: .djlintrc)
  └── tailwind-build       npm ci + npm run build → CSS > 1 KB assertion
```

### Test Modules

| Module | Count | DB required | Purpose |
|---|---|---|---|
| `coreRelback.tests_domain` | 46 | No | Pure domain: entities, use cases, schedule expansion, RMAN parsing |
| `coreRelback.tests` | 37 | Yes (SQLite) | Integration: views, auth, HTTP status codes |

---

## 7. Configuration Files

| File | Purpose |
|---|---|
| `projectRelback/settings.py` | Production settings (Oracle, Tailwind app) |
| `projectRelback/settings_dev.py` | Development: SQLite, `DEBUG=True`, `ORACLE_CATALOG=None` |
| `projectRelback/settings_test.py` | CI integration tests: SQLite in-memory |
| `.sqlfluff` | sqlfluff dialect + excluded rules |
| `.sqlfluffignore` | Oracle PL/SQL files excluded from lint |
| `.djlintrc` | djlint profile=django, enforces T003 |
| `.prettierignore` | Prevents Prettier from formatting Django templates |

---

## 8. Management Commands

| Command | Module | Purpose |
|---|---|---|
| `python manage.py tailwind install` | django-tailwind | Install npm dependencies |
| `python manage.py tailwind build` | django-tailwind | Compile Tailwind CSS (production) |
| `python manage.py tailwind start` | django-tailwind | Watch mode (development) |
| `python manage.py seed_demo` | `coreRelback/management/commands/seed_demo.py` | Populate SQLite with realistic demo data (clients, hosts, databases, policies, simulated RMAN jobs) |

---

## 9. Project Structure

```
relback/
├── coreRelback/
│   ├── domain/
│   │   └── entities.py          ← Pure domain entities / value objects
│   ├── gateways/
│   │   ├── interfaces.py        ← Abstract ports (IClientRepository, IOracleRmanRepository…)
│   │   ├── repositories.py      ← Django ORM adapters + DemoRmanRepository
│   │   └── oracle_catalog.py    ← python-oracledb adapter
│   ├── services/
│   │   └── use_cases.py         ← All business interactors
│   ├── management/commands/
│   │   └── seed_demo.py         ← Demo data seeder
│   ├── templates/               ← Django HTML templates
│   ├── models.py                ← Django ORM models (outer layer)
│   ├── views.py                 ← HTTP adapter (thin — delegates to use cases)
│   └── urls.py
├── projectRelback/
│   ├── settings.py              ← Production settings
│   ├── settings_dev.py          ← Development settings
│   └── settings_test.py         ← Test settings
├── theme/                       ← django-tailwind app
│   └── static_src/              ← Tailwind + DaisyUI build chain
├── databaseProject/             ← Oracle DDL / migration scripts
├── docs/                        ← Architecture + Roadmap docs
├── .sqlfluff / .djlintrc        ← Lint configs
└── .github/workflows/ci.yml     ← CI pipeline
```
