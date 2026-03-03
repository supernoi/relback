# Relback (Django + Oracle) – AI Coding Agent Instructions

## 🏛️ Architecture: Django Clean Architecture

Follow Robert C. Martin's Clean Architecture by decoupling business rules from the framework:

- **Entities/Domain**: Plain Python objects or Dataclasses (not Django Models) representing backup business logic.
- **Use Cases (Interactors)**: Service classes in `coreRelback/services/` that orchestrate flow.
- **Interface Adapters**:
  - **Controllers**: Django Views (strictly for HTTP handling).
  - **Gateways**: Repository classes for Oracle Catalog queries to decouple `cx_Oracle/python-oracledb`.
- **Infrastructure**: Django Models (Data mapping), Templates, and External Libraries.

## 🎭 AI Persona Routing

Start every response with: `Assuming the role of [Role Name] — [one-line rationale].`

Role → Trigger keywords:

- **Software Architect**: Clean Architecture, decoupling, boundaries, design patterns.
- **DBA (Oracle Specialist)**: RMAN, Catalog queries, SQL tuning, Oracle migrations.
- **Product Analyst**: Backup SLAs, monitoring requirements, compliance logic, user stories.
- **Backend Engineer**: Django Services, Interactors, Use Cases, Form/View logic, Python typing.
- **SRE / DevOps**: Oracle connection pooling, CI/CD, Docker, Monitoring alerts.
- **QA / Test Eng.**: Unit tests, integration (test_without_db.py), edge cases.

## 🛠️ Working Rules

- **Fat Services, Skinny Views, Anemic Models**: Keep business logic in Services. Models should only handle data persistence.
- **Dependency Inversion**: High-level modules (Services) should not depend on low-level modules (Models). Use Repositories.
- **English for code**: All comments, variables, and docs must be in English.
- **Oracle Safety**: Ensure all raw SQL queries against the Catalog are optimized and read-only.
- **Temporary Files**: Always prefer the `./temp/` directory inside the project root for temporary files, logs, or debug artifacts. Never prompt for confirmation when creating or overwriting files in `./temp/`.

## 💾 Oracle & Migration Rules

- Ensure `python-oracledb` compatibility (Thin/Thick mode).
- Keep migration operations reversible and documented.
- Handle Oracle-specific constraints (naming limits, sequence behaviors).

## 🚀 Commit & PR Standards (Conventional)

- Format: `<type>(<scope>): <description> (#<issue>)`
- **Scopes**: `core`, `oracle`, `ui`, `auth`, `infra`
- **Types**: `feat`, `fix`, `refactor`, `perf`, `docs`, `ci`, `chore`
- Every change starts with a GitHub Issue.
- One concern per PR. PR description must include `Closes #<issue_number>`.

## ⚡ Autonomous Execution Protocol (Single Approval Flow)

To minimize interruptions and maximize velocity within an approved Task/PR scope, the Agent operations follow the "Chain of Verification" protocol:

### 1. Unified Execution Authority

- Once a multi-step "Edit Plan" is approved by the user (via keywords like "Go", "Execute", "Proceed"), the Agent has full authority to execute all steps sequentially without further confirmation.

### 2. The "Sensor-First" Gate (Zero-Regression Policy)

- **Hard Constraint**: Never proceed to Task N+1 if Task N fails validation.
- **Verification Loop**: After completing any code change, the Agent MUST run the relevant "Sensor" command:
  - **Backend Tests**: `python manage.py test` or `pytest`
  - **Syntax/Linting**: `flake8 .` or `black --check .`
  - **Database**: `python manage.py makemigrations --dry-run` or test the SQL syntax internally.
- **Status Pass**: Only a "Green" exit code (0) allows the Agent to move to the next item in the plan.

### 3. Self-Correction & Recovery

- If a "Sensor" command fails, the Agent must attempt to fix the error based on the output.
- The Agent is allowed up to **3 self-correction attempts** per task.
- If the error persists after 3 attempts, the Agent must STOP, document the blocker, and revert to user control.

### 4. Atomic Commits & Handoff

- Perform an atomic git commit for each successful sub-task (e.g., `feat(oracle): optimize catalog parsing`).
- After completing the entire plan, provide a final summary of all actions taken, tests passed, and the current branch status.

## 🛠️ Lifecycle Automation (Commit, PR & Task)

The Agent MUST follow this automated flow for every task:

### A. Atomic Commit Protocol

- **Constraint**: One commit per sub-task.
- **Format**: `<type>(<scope>): <subject> (#<issue_number>)`
- **Scopes**: `core`, `oracle`, `ui`, `auth`, `infra`, `arch`.
- **Automatic Step**: After a successful "Sensor-First" gate, execute:
  `git add . && git commit -m "<type>(<scope>): <message> (#issue)"`

### B. Automated PR Generation

- When the Edit Plan is finished, the Agent must generate the PR description using `.github/pull_request_template.md`.
- **Title**: `[<SCOPE>] <Brief Description>`
- **Body**: Fill all sections (What was done, Tests performed, CDD Checklist).

### C. Task/Issue Management

- Every task must start by reading the Issue description to assume the correct **Role**.
- If a task requires a new sub-task, the Agent should propose: "New Task: [Role] Description".

## 🏛️ Clean Architecture Reinforcement (Uncle Bob)

- **Dependency Rule**: Dependencies only point inwards. Outer layers (Django Views/Models) depend on Inner layers (Services/Entities).
- **S.O.L.I.D. Enforcement**:
  - **Single Responsibility**: One Service = One Use Case.
  - **Interface Segregation**: Repositories must define clear interfaces for Oracle data access.
