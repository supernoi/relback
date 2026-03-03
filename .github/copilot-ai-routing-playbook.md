# AI Routing Playbook

## Purpose

Guidance to route coding tasks to the best implementation path.

## Routing Rules

- Django backend changes: prioritize `coreRelback/` + `projectRelback/`.
- UI template changes: prioritize `coreRelback/templates/` + `static/css/`.
- DB schema changes: prioritize Django migrations and SQL scripts under `databaseProject/`.
- CI/CD changes: prioritize `.github/workflows/`.
- Backup error investigation: prioritize `databaseProject/` and RMAN logs first.
- Screen/UI error investigation: prioritize `coreRelback/templates/` and `static/` first.

## Quality Gates

- Keep scope minimal per task.
- Validate with `python manage.py check` and `python manage.py test` when possible.
- Document assumptions in PR description.
