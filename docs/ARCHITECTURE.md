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

| Symbol               | Type         | Purpose                                                        |
| -------------------- | ------------ | -------------------------------------------------------------- |
| `ClientEntity`       | `@dataclass` | Business representation of a backup client                     |
| `HostEntity`         | `@dataclass` | Server/host that runs Oracle                                   |
| `DatabaseEntity`     | `@dataclass` | Oracle database instance                                       |
| `BackupPolicyEntity` | `@dataclass` | RMAN backup policy with cron schedule                          |
| `ScheduleEntry`      | `@dataclass` | Expanded cron forecast entry                                   |
| `BackupJobResult`    | `@dataclass` | One RMAN backup job from RC_RMAN_BACKUP_JOB_DETAILS            |
| `BackupLogEntry`     | `@dataclass` | One output line from RC_RMAN_OUTPUT                            |
| `DashboardStats`     | `@dataclass` | Aggregated counts for dashboard                                |
| `BackupStatusValue`  | `Enum`       | COMPLETED / FAILED / RUNNING / WARNING / INTERRUPTED / UNKNOWN |
| `BackupType`         | `Enum`       | ARCHIVELOG / DB FULL / DB INCR / RECVR AREA / BACKUPSET        |
| `PolicyStatus`       | `Enum`       | ACTIVE / INACTIVE                                              |
| `BackupDestination`  | `Enum`       | DISK / SBT_TAPE                                                |

### 2.2 Gateway Interfaces — `coreRelback/gateways/interfaces.py`

Abstract base classes (Python `ABC`) that define the **ports**. Use cases depend only on these — they never import concrete repositories or ORM models.

| Interface                 | Methods                                                                                |
| ------------------------- | -------------------------------------------------------------------------------------- |
| `IClientRepository`       | `get_all`, `get_by_id`, `count`, `create`, `update`, `delete`                          |
| `IHostRepository`         | `get_all`, `get_by_id`, `count`, `create`, `update`, `delete`                          |
| `IDatabaseRepository`     | `get_all`, `get_by_id`, `count`, `create`, `update`, `delete`                          |
| `IBackupPolicyRepository` | `get_all`, `get_by_id`, `count`, `count_active`, `create`, `update`, `delete`          |
| `IScheduleRepository`     | `get_upcoming`, `delete_all`, `create_batch`                                           |
| `IOracleRmanRepository`   | `get_backup_jobs`, `get_running_jobs_count`, `get_backup_job_detail`, `get_backup_log` |

### 2.3 Concrete Repositories — `coreRelback/gateways/repositories.py`

| Class                          | Backend            | Notes                                                                                                                                           |
| ------------------------------ | ------------------ | ----------------------------------------------------------------------------------------------------------------------------------------------- |
| `DjangoClientRepository`       | Django ORM         | Wraps `Client` model                                                                                                                            |
| `DjangoHostRepository`         | Django ORM         | Wraps `Host` model                                                                                                                              |
| `DjangoDatabaseRepository`     | Django ORM         | Wraps `Database` model                                                                                                                          |
| `DjangoBackupPolicyRepository` | Django ORM         | Wraps `BackupPolicy` model                                                                                                                      |
| `DjangoScheduleRepository`     | Django ORM         | Wraps `Schedule` model                                                                                                                          |
| `OracleRmanRepository`         | python-oracledb    | Queries Oracle RMAN Catalog views (`RC_RMAN_BACKUP_JOB_DETAILS`, `RC_RMAN_OUTPUT`); returns empty lists when `ORACLE_CATALOG` setting is `None` |
| `DemoRmanRepository`           | In-memory fixtures | Returns realistic fake RMAN data when `DEMO_MODE = True` in settings                                                                            |

### 2.4 Use Cases — `coreRelback/services/use_cases.py`

One class per business action (Single Responsibility). Each constructor accepts interface types, never concrete classes.

| Use Case                    | Purpose                                         |
| --------------------------- | ----------------------------------------------- |
| `GetDashboardStatsUseCase`  | Aggregates counts for Dashboard                 |
| `GetScheduleReportUseCase`  | Reads upcoming backup schedule by date range    |
| `GenerateScheduleUseCase`   | Expands cron policy fields into `Schedule` rows |
| `AuditBackupUseCase`        | Correlates schedules with Oracle job results    |
| `GetBackupDetailUseCase`    | Fetches RMAN log lines for a specific job       |
| `CreateClientUseCase`       | Validates + creates a Client                    |
| `UpdateClientUseCase`       | Validates + updates a Client                    |
| `DeleteClientUseCase`       | Removes a Client                                |
| `CreateHostUseCase`         | Validates + creates a Host                      |
| `UpdateHostUseCase`         | Validates + updates a Host                      |
| `DeleteHostUseCase`         | Removes a Host                                  |
| `CreateDatabaseUseCase`     | Validates + creates a Database                  |
| `UpdateDatabaseUseCase`     | Validates + updates a Database                  |
| `DeleteDatabaseUseCase`     | Removes a Database                              |
| `CreateBackupPolicyUseCase` | Validates + creates a BackupPolicy              |
| `UpdateBackupPolicyUseCase` | Validates + updates a BackupPolicy              |
| `DeleteBackupPolicyUseCase` | Removes a BackupPolicy                          |

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

**Thin vs Thick mode (python-oracledb):**

| Mode  | Requirement              | Use case                                      |
| ----- | ------------------------- | --------------------------------------------- |
| Thin  | No Oracle Client install  | Default in Relback — CI, Docker, dev machines |
| Thick | Oracle Client (libs)      | Legacy or when Thin is unsupported            |

Relback uses **Thin only** via `oracledb.connect(user=..., password=..., dsn=...)`. For Thick you would call `oracledb.init_oracle_client(lib_dir=...)` before `connect()`; not used here so deployment stays client-free. DSN format: `host:port/service_name` (e.g. `catalog.example.com:1521/RMANCAT`).

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

| Model              | Table                | Purpose                                                 |
| ------------------ | -------------------- | ------------------------------------------------------- |
| `RelbackUser`      | `users`              | Custom user — no AbstractBaseUser, own password hashing |
| `Client`           | `clients`            | Organizational unit (customer / business unit)          |
| `Host`             | `hosts`              | Physical/virtual server running Oracle                  |
| `Database`         | `databases`          | Oracle instance (identified by `dbid`)                  |
| `BackupPolicy`     | `backup_policies`    | RMAN backup schedule definition                         |
| `Schedule`         | `schedules`          | Expanded forecast entry (policy × time)                 |
| `VwBackupPolicies` | `vw_backup_policies` | Oracle view, `managed=False`                            |

---

## 4. Authentication

Custom session-based auth using `RelbackUser`. No Django `AbstractBaseUser`.

| Component            | Location                                        |
| -------------------- | ----------------------------------------------- |
| `RelbackBackend`     | `coreRelback/backends.py` — custom auth backend |
| `LoginView`          | `coreRelback/views.py`                          |
| `LogoutView`         | `coreRelback/views.py`                          |
| `RegisterView`       | `coreRelback/views.py`                          |
| `LoginRequiredMixin` | Applied to all CRUD views and dashboard         |

Session is stored in `django.contrib.sessions` (database-backed in production, file in dev).

### 4.1 Real-time updates (Phase 18)

Django Channels provides a WebSocket at `/ws/reports/` for the Reports page. Authenticated users receive JSON `{ jobs, summary, oracle_available }` on connect and every 30s. Server: `daphne projectRelback.asgi:application`. Consumer: `coreRelback/consumers.py` (`ReportsJobsConsumer`). In production, set `REDIS_URL` and use Redis channel layer for multi-worker scaling; `docker-compose.yml` includes a `redis` service.

### 4.2 REST API (Phase 17)

Django REST Framework provides read-only JSON endpoints for backup audit data (e.g. dashboards, Grafana).

| Endpoint | Method | Auth | Description |
|----------|--------|------|--------------|
| `/api/backup-audit/` | GET | Session (IsAuthenticated) | List backup jobs from `AuditBackupUseCase`; optional query: `from_date`, `to_date`, `db_name` (ISO dates YYYY-MM-DD). |

**Response shape (200):**

```json
{
  "jobs": [
    {
      "db_name": "ORCL",
      "dbid": 123456,
      "status": "COMPLETED",
      "start_time": "2025-03-01T02:00:00Z",
      "end_time": "2025-03-01T02:15:00Z",
      "backup_type": "DB FULL",
      "output_bytes_display": "10G",
      "time_taken_display": "00:15:00",
      "output_device_type": "DISK",
      "session_key": 42,
      "input_type": "policy-name",
      "severity": "success"
    }
  ],
  "summary": {
    "total": 10,
    "successful": 8,
    "failed": 1,
    "running": 1,
    "oracle_available": true
  }
}
```

- **403 Forbidden:** request without valid session (login required; DRF default).
- **Serializers:** `coreRelback/api/serializers.py` — domain entities (e.g. `BackupJobResult`) mapped to JSON; no Django models in the public API.

### 4.3 Multi-tenant catalog (Phase 19)

Reports and log detail are scoped by client when configured:

- **Client.catalog_dsn** (optional): when set, Oracle RMAN catalog queries for that client use this DSN; credentials from global `ORACLE_CATALOG`.
- **RelbackUser.default_client** (optional): when set, `report_read` passes this client’s id to `AuditBackupUseCase` so only that client’s catalog is queried.
- **report_read_log_detail**: passes `policy.client_id` to `GetBackupDetailUseCase` so the correct client catalog is used.
- **IOracleRmanRepository** and **get_catalog_connection(client_id)** accept optional `client_id`; implementations use the client’s DSN when present.
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

| Token       | relback_light | relback_dark | Purpose                                            |
| ----------- | ------------- | ------------ | -------------------------------------------------- |
| `primary`   | `#C74634`     | `#6366f1`    | Buttons, active elements (Oracle Red / Indigo-500) |
| `secondary` | `#1A1A2E`     | `#94a3b8`    | Secondary labels, muted text                       |
| `accent`    | `#0052CC`     | `#06b6d4`    | Accent highlights (Oracle Blue / Cyan-500)         |
| `base-100`  | `#f8fafc`     | `#0f172a`    | Page background                                    |
| `base-200`  | _(default)_   | `#1e293b`    | Cards, sidebar                                     |
| `base-300`  | _(default)_   | `#334155`    | Borders, dividers                                  |
| `success`   | `#22c55e`     | `#4ade80`    | COMPLETED status (WCAG AA ≥4.5:1 on dark bg)       |
| `warning`   | `#f59e0b`     | `#fbbf24`    | WARNING / RUNNING_WITH_ISSUES                      |
| `error`     | `#ef4444`     | `#f87171`    | FAILED status                                      |
| `info`      | `#3b82f6`     | `#93c5fd`    | RUNNING status                                     |
| `neutral`   | `#1e293b`     | `#334155`    | UNKNOWN / headers                                  |

> Dark theme uses lighter status colors (400-series instead of 600-series) to meet WCAG AA contrast ratio ≥4.5:1 against `#0f172a` background — critical for NOC/operations monitor readability.

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

| Module                     | Count | DB required  | Purpose                                                            |
| -------------------------- | ----- | ------------ | ------------------------------------------------------------------ |
| `coreRelback.tests_domain` | 46    | No           | Pure domain: entities, use cases, schedule expansion, RMAN parsing |
| `coreRelback.tests`        | 37    | Yes (SQLite) | Integration: views, auth, HTTP status codes                        |

---

## 7. Configuration Files

| File                               | Use case                                                               | Oracle    | DEMO_MODE |
| ---------------------------------- | ---------------------------------------------------------------------- | --------- | --------- |
| `projectRelback/settings.py`       | Base (not used directly)                                               | hardcoded | off       |
| `projectRelback/settings_dev.py`   | Dev — `DATABASES={}`, `DEBUG=True`                                     | off       | off       |
| `projectRelback/settings_local.py` | Local UI: SQLite file db + realistic mock RMAN data                    | off       | on        |
| `projectRelback/settings_test.py`  | CI integration tests: SQLite in-memory                                 | off       | off       |
| `projectRelback/settings_prod.py`  | Production/Docker: `DEBUG=False`, WhiteNoise, all config from env vars | env vars  | auto      |

| File              | Purpose                                                                                                            |
| ----------------- | ------------------------------------------------------------------------------------------------------------------ |
| `.sqlfluff`       | sqlfluff dialect + excluded rules                                                                                  |
| `.sqlfluffignore` | Oracle PL/SQL files excluded from lint                                                                             |
| `.djlintrc`       | djlint profile=django, enforces T003 (named endblocks)                                                             |
| `.prettierignore` | Prevents Prettier from formatting Django templates                                                                 |
| `.env.example`    | Documented env var template — `DJANGO_SECRET_KEY`, `ALLOWED_HOSTS`, `DB_*`, `ORACLE_CATALOG_*`, `GUNICORN_WORKERS` |
| `.dockerignore`   | Lean Docker build context — excludes `.venv/`, `__pycache__/`, `db.sqlite3`, `.git/`                               |

---

## 8. Management Commands

| Command                             | Module                                         | Purpose                                                                                                                               |
| ----------------------------------- | ---------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------- |
| `python manage.py tailwind install` | django-tailwind                                | Install npm dependencies                                                                                                              |
| `python manage.py tailwind build`   | django-tailwind                                | Compile Tailwind CSS (production)                                                                                                     |
| `python manage.py tailwind start`   | django-tailwind                                | Watch mode (development)                                                                                                              |
| `python manage.py seed_demo`        | `coreRelback/management/commands/seed_demo.py` | Populate SQLite with realistic demo data (4 clients, 8 hosts, 8 databases, 8 policies, simulated RMAN jobs). Supports `--flush` flag. |

---

## 9. Production Deployment

### Stack

| Component  | Version     | Role                                                                   |
| ---------- | ----------- | ---------------------------------------------------------------------- |
| Gunicorn   | 21.x–22.x   | WSGI application server (see `requirements.txt`)                       |
| WhiteNoise | 6.x         | Compressed static file serving (no Nginx needed for small deployments) |
| Docker     | multi-stage | Node 20 CSS builder + Python 3.13 runtime                              |

### Dockerfile (multi-stage)

```
Stage 1 (css-builder)   node:20-slim
  npm ci + npm run build → theme/static/css/dist/styles.css

Stage 2 (runtime)       python:3.13-slim
  pip install requirements.txt
  collectstatic → STATIC_ROOT
  useradd relback (non-root)
  CMD: gunicorn projectRelback.wsgi --bind 0.0.0.0:8000 --workers ${GUNICORN_WORKERS:-3}
```

### Environment Variables (production)

| Variable                                                                 | Required  | Default               | Notes                                             |
| ------------------------------------------------------------------------ | --------- | --------------------- | ------------------------------------------------- |
| `DJANGO_SECRET_KEY`                                                      | Yes       | —                     | No unsafe fallback in prod                        |
| `ALLOWED_HOSTS`                                                          | Yes       | `localhost,127.0.0.1` | Comma-separated                                   |
| `DB_ENGINE`                                                              | No        | sqlite3               | `django.db.backends.oracle` for Oracle            |
| `DB_NAME` / `DB_USER` / `DB_PASSWORD` / `DB_HOST` / `DB_PORT`            | If Oracle | —                     | Oracle credentials                                |
| `ORACLE_CATALOG_USER` / `ORACLE_CATALOG_PASSWORD` / `ORACLE_CATALOG_DSN` | If Oracle | —                     | RMAN catalog connection; empty → `DEMO_MODE=True` |
| `GUNICORN_WORKERS`                                                       | No        | 3                     | `(2 * CPU) + 1` is standard                       |

### Quick Start

```bash
cp .env.example .env        # fill DJANGO_SECRET_KEY at minimum
docker compose up --build   # http://localhost:80 (Nginx) or https://localhost:443 (self-signed)
docker compose exec web python manage.py seed_demo  # optional demo data
# Login: admin / demo1234
```

### Nginx + TLS (reverse proxy)

| Component | Role |
| --------- | ----- |
| **Nginx** | Reverse proxy in front of Gunicorn; listens on 80 (HTTP) and 443 (HTTPS). |
| **Dev** | On first run, `nginx/entrypoint.sh` generates a self-signed certificate so HTTPS works without setup. |
| **Prod** | Mount Let's Encrypt (certbot) certs: add to `docker-compose` for service `nginx`: `volumes: - ./certs:/etc/nginx/certs:ro` with `fullchain.pem` and `privkey.pem` in `./certs`. |

**Files:** `nginx/nginx.conf`, `nginx/entrypoint.sh`, `nginx/Dockerfile`. Compose service `nginx` depends on `web` (healthcheck). Optional env in `.env.example`: `NGINX_CERTS_PATH` to document where prod certs live.

---

## 10. Project Structure

```
relback/
├── coreRelback/
│   ├── domain/
│   │   └── entities.py          ← Pure domain entities / value objects
│   ├── gateways/
│   │   ├── interfaces.py        ← Abstract ports (IClientRepository, IOracleRmanRepository…)
│   │   ├── repositories.py      ← Django ORM adapters + DemoRmanRepository
│   │   └── oracle_catalog.py    ← python-oracledb adapter (Thin mode)
│   ├── services/
│   │   └── use_cases.py         ← All business interactors
│   ├── management/commands/
│   │   └── seed_demo.py         ← Demo data seeder (idempotent, --flush flag)
│   ├── templates/               ← Django HTML templates (DaisyUI components)
│   ├── models.py                ← Django ORM models (outer layer)
│   ├── views.py                 ← HTTP adapter (thin — delegates to use cases)
│   └── urls.py
├── projectRelback/
│   ├── settings.py              ← Base settings
│   ├── settings_dev.py          ← Dev: DATABASES={}, DEBUG=True
│   ├── settings_local.py        ← Local: SQLite file + DEMO_MODE=True
│   ├── settings_test.py         ← CI: SQLite in-memory
│   └── settings_prod.py         ← Production: DEBUG=False, WhiteNoise, env-based
├── theme/                       ← django-tailwind app
│   └── static_src/              ← Tailwind + DaisyUI build chain
│       ├── tailwind.config.js   ← DaisyUI themes: relback_light + relback_dark
│       └── src/styles.css       ← @tailwind base/components/utilities entry point
├── databaseProject/             ← Oracle DDL / migration scripts
├── docs/
│   ├── ARCHITECTURE.md          ← This document
│   ├── ROADMAP_TAILWIND_DAISYUI.md
│   └── UX_UI_analysis.md
├── nginx/                       ← Nginx reverse proxy (Phase 13): nginx.conf, entrypoint.sh, Dockerfile
├── Dockerfile                   ← Multi-stage (Node 20 CSS + Python 3.13 Gunicorn)
├── docker-compose.yml           ← Web + Nginx; TLS self-signed (dev) or mount certs (prod)
├── .env.example                 ← Env var template (commit safe — no real values)
├── .dockerignore
├── .sqlfluff / .djlintrc        ← Lint configs
└── .github/workflows/ci.yml     ← CI pipeline (check + tests + lint + docker build)
```

---

## 11. Future Roadmap (Phase 12+)

High-level next steps are tracked in **`docs/ROADMAP_TAILWIND_DAISYUI.md`** (Phase 12+ table and implementation plan). Summary:

| Focus            | Phases (priority)                                                                 |
| ---------------- | ---------------------------------------------------------------------------------- |
| **Infra & data** | 12 — Oracle Reconnect; 13 — Nginx + TLS                                            |
| **Product**      | 14 — Alerting & SLA Monitor; 15 — Pagination; 16 — User Roles & Permissions        |
| **Integration**  | 17 — API Layer (DRF); 18 — Real-time (Channels); 19 — Multi-tenant                 |

All new features must respect the Dependency Rule: new use cases in `coreRelback/services/`, new gateways in `coreRelback/gateways/`, entities in `coreRelback/domain/entities.py`.

---

## 12. Build & Troubleshooting

| Issue | Cause | Fix |
| ----- | ----- | --- |
| Docker build fails at `npm run build` (exit 127) | Stage 1 uses `npm ci --omit=dev`; `tailwindcss` is a devDependency and is not installed. | In `Dockerfile` stage `css-builder`, use `npm ci` (or `npm ci --include=dev`) so Tailwind CLI is available. |
| `python manage.py check` fails in container | Missing env vars (`DJANGO_SECRET_KEY`, `ALLOWED_HOSTS`). | Set at least `DJANGO_SECRET_KEY` and `ALLOWED_HOSTS` (e.g. in `docker run -e ...` or `.env`). |
| Oracle catalog "not available" in UI | `ORACLE_CATALOG_*` not set or invalid in settings. | Configure in `settings_prod.py` (env) or use Demo Mode (`settings_local.py`) for local preview. |
