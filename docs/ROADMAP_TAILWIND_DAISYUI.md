# Roadmap: Tailwind CSS + DaisyUI Integration

**Project:** Relback (Django + Oracle)  
**Objective:** Modernize the UI to a high-density, dark-mode-ready dashboard for Oracle backup monitoring.  
**Architecture:** `django-tailwind` package integrated as a proper Django app (`theme/`), following Clean Architecture — CSS infrastructure is an outer layer detail, invisible to domain entities and use cases.

---

## Prerequisites (System-Level — outside any PR)

```bash
# Install Node.js ≥ 18 (required for npm / PostCSS / Tailwind CLI)
sudo apt install nodejs npm        # Debian/Ubuntu
# OR via nvm (preferred for version management):
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.7/install.sh | bash
nvm install --lts
```

---

## Phase Overview

| Phase | Name                                      | Status         | PR                    |
| ----- | ----------------------------------------- | -------------- | --------------------- |
| 1     | Setup — Infrastructure                    | ✅ Done        | #13                   |
| 2     | Theme — DaisyUI + Design Tokens           | ✅ Done        | #17                   |
| 3     | Base Layout Migration                     | ✅ Done        | #21                   |
| 4     | Component Migration (Dashboard, Tables)   | ✅ Done        | #23 / #25 / #27 / #29 |
| 5     | Remaining Templates + Auth                | ✅ Done        | #31                   |
| 6     | Live Oracle RMAN Gateway                  | ✅ Done        | #34                   |
| 7     | Oracle Reports — UI Enhancements          | ✅ Done        | #36                   |
| 8     | Report Log Detail View                    | ✅ Done        | #38                   |
| 9     | CI — Hardening & Quality Gates            | ✅ Done        | #42 / #44             |
| 10    | Demo Mode — Seed data for local preview   | ✅ Done        | #46                   |
| 11    | Production Deployment (Docker + Gunicorn) | 🔲 Pending     | —                     |

---

## Phase 1 — Setup (Infrastructure)

**Goal:** Get `django-tailwind` wired into Django. After this phase, running `python manage.py tailwind start` produces a compiled `theme.css`.

| #   | Task                                                                                                    | Files Impacted                        | Sensor                                              |
| --- | ------------------------------------------------------------------------------------------------------- | ------------------------------------- | --------------------------------------------------- |
| 1.1 | Install `django-tailwind[reload]` and add to `requirements.txt`                                         | `requirements.txt`                    | `pip install -r requirements.txt` → exit 0          |
| 1.2 | Add `tailwind` and `theme` to `INSTALLED_APPS`; set `TAILWIND_APP_NAME`, `INTERNAL_IPS`, `NPM_BIN_PATH` | `projectRelback/settings.py`          | `python manage.py check`                            |
| 1.3 | Scaffold `theme/` app via `manage.py tailwind init`                                                     | `theme/` (new Django app)             | Directory exists; `python manage.py check`          |
| 1.4 | Add DaisyUI to `theme/static_src/package.json`                                                          | `theme/static_src/package.json`       | `cat theme/static_src/package.json` shows `daisyui` |
| 1.5 | Configure `tailwind.config.js` — content paths, DaisyUI plugin, Relback themes                          | `theme/static_src/tailwind.config.js` | `cat theme/static_src/tailwind.config.js`           |
| 1.6 | Run `python manage.py tailwind install` (requires Node ≥ 18)                                            | `theme/static_src/node_modules/`      | Exit 0 — `node_modules` is created                  |
| 1.7 | Load `{% tailwind_css %}` tag in `base.html`                                                            | `coreRelback/templates/base.html`     | Page renders without 404 on CSS                     |

**First commit after Phase 1:**

```
feat(ui): bootstrap django-tailwind + DaisyUI theme app (#12)
```

---

## Phase 2 — Theme: DaisyUI + Design Tokens

**Goal:** Define the Relback color palette and DaisyUI themes (light/dark/dracula).

### Backup Status Color Palette

| Status                | Semantic | DaisyUI Token | Hex                   |
| --------------------- | -------- | ------------- | --------------------- |
| `COMPLETED`           | Success  | `success`     | `#22c55e` (green-500) |
| `RUNNING`             | Info     | `info`        | `#3b82f6` (blue-500)  |
| `FAILED`              | Error    | `error`       | `#ef4444` (red-500)   |
| `RUNNING_WITH_ISSUES` | Warning  | `warning`     | `#f59e0b` (amber-500) |
| `UNKNOWN`             | Neutral  | `neutral`     | `#6b7280` (gray-500)  |

### DaisyUI Custom Theme (`tailwind.config.js` excerpt)

```js
daisyui: {
  themes: [
    {
      relback_light: {
        "primary":   "#C74634",   // Oracle Red
        "secondary": "#1A1A2E",   // Deep Navy
        "accent":    "#0052CC",   // Oracle Blue
        "neutral":   "#1e293b",
        "base-100":  "#f8fafc",
        "success":   "#22c55e",
        "warning":   "#f59e0b",
        "error":     "#ef4444",
        "info":      "#3b82f6",
      },
      relback_dark: {
        "primary":   "#C74634",
        "secondary": "#e2e8f0",
        "accent":    "#60a5fa",
        "neutral":   "#334155",
        "base-100":  "#0f172a",
        "success":   "#16a34a",
        "warning":   "#d97706",
        "error":     "#dc2626",
        "info":      "#2563eb",
      },
    },
    "dracula",
  ],
  defaultTheme: "relback_dark",
},
```

| #   | Task                                                                           | Files Impacted                                 | Sensor                                     |
| --- | ------------------------------------------------------------------------------ | ---------------------------------------------- | ------------------------------------------ |
| 2.1 | Define Relback color tokens and DaisyUI theme objects                          | `theme/static_src/tailwind.config.js`          | `python manage.py tailwind build` → exit 0 |
| 2.2 | Add theme switcher (light/dark/dracula) via `data-theme` attribute on `<html>` | `base.html`, `theme/static_src/src/styles.css` | Visual: theme toggle changes colors        |
| 2.3 | Tag `BackupStatusValue` enum display in template with status-to-badge mapping  | `coreRelback/templates/reports.html`           | `python manage.py test coreRelback.tests`  |

---

## Phase 3 — Base Layout Migration

**Goal:** Replace the current `md-navbar` / `md-main-content` custom CSS layout with a Tailwind `drawer` sidebar layout from DaisyUI.

### Target Layout (DaisyUI Drawer)

```
┌─────────────────────────────────────────────────────┐
│  Sidebar (fixed, w-64)  │  Main Content (scrollable)│
│  - Logo + App name      │  - Page title bar         │
│  - Nav links            │  - {% block content %}    │
│  - User menu + logout   │                           │
└─────────────────────────────────────────────────────┘
```

| #   | Task                                                           | Files Impacted                      | Sensor                                                    |
| --- | -------------------------------------------------------------- | ----------------------------------- | --------------------------------------------------------- |
| 3.1 | Rewrite `base.html` structure with DaisyUI `drawer` component  | `coreRelback/templates/base.html`   | `python manage.py test coreRelback.tests` — 20 tests pass |
| 3.2 | Migrate navbar links to sidebar `<ul class="menu">`            | `base.html`                         | Visual: links render with hover states                    |
| 3.3 | Migrate user dropdown to `<div class="dropdown dropdown-end">` | `base.html`                         | Logout POST still works                                   |
| 3.4 | Add breadcrumbs component to page title bar                    | `base.html`                         | `python manage.py check`                                  |
| 3.5 | Migrate `auth/login.html` and `auth/register.html` to Tailwind | `coreRelback/templates/auth/*.html` | `python manage.py test coreRelback.tests`                 |

---

## Phase 4 — Component Migration

**Goal:** Replace page-by-page, starting with highest-visibility views.

### Migration Priority

1. **Dashboard (`index.html`)** — DaisyUI `stats` component for counters (Clients, Hosts, Databases, Policies)
2. **Reports (`reports.html`)** — DaisyUI `table` + `badge` for backup job status
3. **CRUD Lists** (`clients.html`, `hosts.html`, `databases.html`, `policies.html`) — DaisyUI `table` with row actions
4. **CRUD Forms** — DaisyUI `form-control` + `label` + `input`/`select`

| #   | Task                                                             | Files Impacted                                                            | Sensor                                        |
| --- | ---------------------------------------------------------------- | ------------------------------------------------------------------------- | --------------------------------------------- |
| 4.1 | Dashboard stats cards with `stats` component                     | `templates/index.html`                                                    | Visual + `python manage.py test`              |
| 4.2 | Reports table + `badge` for `BackupStatusValue`                  | `templates/reports.html`                                                  | All 20 tests pass                             |
| 4.3 | CRUD list views with DaisyUI `table`                             | `templates/clients.html`, `hosts.html`, `databases.html`, `policies.html` | All 20 tests pass                             |
| 4.4 | CRUD forms with DaisyUI `form-control`                           | `templates/*_form.html`, `templates/*_confirm_delete.html`                | All 20 tests pass                             |
| 4.5 | Auth pages (login/register) with DaisyUI `card` + `form-control` | `templates/auth/login.html`, `register.html`                              | `LoginViewTests` + `LogoutRegisterTests` pass |

---

## Running Commands Reference

```bash
# Build CSS once (production)
DJANGO_SETTINGS_MODULE=projectRelback.settings python manage.py tailwind build

# Watch mode (development)
DJANGO_SETTINGS_MODULE=projectRelback.settings python manage.py tailwind start

# Full install (needs Node ≥ 18 first)
python manage.py tailwind install
```

---

## Files Created / Modified by Phase 1

| File                                  | Action                                                                                           |
| ------------------------------------- | ------------------------------------------------------------------------------------------------ |
| `requirements.txt`                    | Add `django-tailwind[reload]>=3.8.0,<4.0`                                                        |
| `projectRelback/settings.py`          | Add `tailwind`, `theme` to `INSTALLED_APPS`; `TAILWIND_APP_NAME`, `INTERNAL_IPS`, `NPM_BIN_PATH` |
| `theme/`                              | New Django app (scaffolded by `manage.py tailwind init`)                                         |
| `theme/static_src/tailwind.config.js` | DaisyUI plugin + content paths + Relback themes                                                  |
| `theme/static_src/package.json`       | `daisyui` added as dependency                                                                    |
| `coreRelback/templates/base.html`     | Add `{% load tailwind_tags %}` + `{% tailwind_css %}`                                            |

---

## CI Quality Gates (active on every PR)

| Job | Tool | What it enforces |
|---|---|---|
| `check-and-test` | Django + pytest | System check, 46 domain tests, 37 integration tests |
| `sql-lint` | sqlfluff 3+ | SQL hygiene in `databaseProject/` — exits non-zero on violations |
| `template-lint` | djlint 1.36+ | Named endblocks, no collapsed `{% block %}` tags (T003) |
| `tailwind-build` | Node 20 + npm | Compiled `theme/static/css/dist/styles.css` > 1 KB |

Config files: `.sqlfluff`, `.sqlfluffignore`, `.djlintrc`, `.prettierignore`

---

## Completed Delivery History

| PR | Issue | Type | Description |
|---|---|---|---|
| #2 | #1 | refactor | Initial Clean Architecture — CRUD use cases, entities, repositories |
| #5 | #4 | feat | LoginRequiredMixin on all CRUD views |
| #7 | #6 | chore | Remove EOL Angular.js + Materialize CSS |
| #9 | #8 | fix | Integration tests after auth gates |
| #11 | #10 | feat | Login / logout / register views wired |
| #13 | #12 | feat | Tailwind CSS + DaisyUI Phase 1 — infrastructure |
| #15 | #14 | feat | Phase 1 hardening — CSS guard, WCAG tokens, CI Tailwind build gate |
| #17 | #16 | feat | Phase 2 — DaisyUI status badges + theme switcher |
| #19 | #18 | chore | Commit package-lock.json + formatter normalisation |
| #21 | #20 | feat | Phase 3 — DaisyUI drawer layout + auth templates |
| #23 | #22 | feat | Phase 4.1 — Dashboard stats with DaisyUI `stats` |
| #25 | #24 | feat | Phase 4.2 — Reports table + `badge` for backup status |
| #27 | #26 | feat | Phase 4.3 — CRUD list views with DaisyUI `table` |
| #29 | #28 | feat | Phase 4.4 — CRUD forms with DaisyUI `form-control` |
| #31 | #30 | feat | Phase 5 — remaining templates + creators page |
| #34 | #33 | feat | Live Oracle RMAN Catalog gateway + graceful fallback |
| #36 | #35 | feat | Reports UI — oracle-available banner + running_jobs |
| #38 | #37 | feat | Report log detail view (RC_RMAN_OUTPUT) |
| #40 | #39 | fix | Template formatter regression hotfix |
| #42 | #41 | ci | sqlfluff hardening — remove `|| true` |
| #44 | #43 | ci | djlint template-lint gate + named endblocks |


---

## CI Quality Gates (active on every PR)

| Job | Tool | What it enforces |
|---|---|---|
| `check-and-test` | Django + pytest | System check, 46 domain tests, 37 integration tests |
| `sql-lint` | sqlfluff 3+ | SQL hygiene in `databaseProject/` — exits non-zero on violations |
| `template-lint` | djlint 1.36+ | Named endblocks, no collapsed `{% block %}` tags (T003) |
| `tailwind-build` | Node 20 + npm | Compiled `theme/static/css/dist/styles.css` > 1 KB |

Config files: `.sqlfluff`, `.sqlfluffignore`, `.djlintrc`, `.prettierignore`

---

## Completed Delivery History

| PR | Issue | Type | Description |
|---|---|---|---|
| #2 | #1 | refactor | Initial Clean Architecture — CRUD use cases, entities, repositories |
| #5 | #4 | feat | LoginRequiredMixin on all CRUD views |
| #7 | #6 | chore | Remove EOL Angular.js + Materialize CSS |
| #9 | #8 | fix | Integration tests after auth gates |
| #11 | #10 | feat | Login / logout / register views wired |
| #13 | #12 | feat | Tailwind CSS + DaisyUI Phase 1 — infrastructure |
| #15 | #14 | feat | Phase 1 hardening — CSS guard, WCAG tokens, CI Tailwind build gate |
| #17 | #16 | feat | Phase 2 — DaisyUI status badges + theme switcher |
| #19 | #18 | chore | Commit package-lock.json + formatter normalisation |
| #21 | #20 | feat | Phase 3 — DaisyUI drawer layout + auth templates |
| #23 | #22 | feat | Phase 4.1 — Dashboard stats with DaisyUI `stats` |
| #25 | #24 | feat | Phase 4.2 — Reports table + badge for backup status |
| #27 | #26 | feat | Phase 4.3 — CRUD list views with DaisyUI table |
| #29 | #28 | feat | Phase 4.4 — CRUD forms with DaisyUI form-control |
| #31 | #30 | feat | Phase 5 — remaining templates + creators page |
| #34 | #33 | feat | Live Oracle RMAN Catalog gateway + graceful fallback |
| #36 | #35 | feat | Reports UI — oracle-available banner + running_jobs |
| #38 | #37 | feat | Report log detail view (RC_RMAN_OUTPUT) |
| #40 | #39 | fix | Template formatter regression hotfix |
| #42 | #41 | ci | sqlfluff hardening — remove `|| true` |
| #44 | #43 | ci | djlint template-lint gate + named endblocks |
