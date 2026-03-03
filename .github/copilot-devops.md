# DevOps Guidelines

## CI Objectives
- Fail fast on configuration errors.
- Keep runtime matrix minimal unless required.
- Prefer deterministic installs from `requirements.txt`.
- Include **Oracle Syntax Validation** in CI using SQL linting tools to validate `databaseProject/` queries.

## Delivery Rules
- Protect `master` with required CI checks.
- Keep secrets in GitHub Secrets only.
- Avoid embedding infrastructure credentials in repo files.

## Operations
- Run `python manage.py check` as baseline gate.
- Run tests before merge.
