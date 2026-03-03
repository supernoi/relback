# Architecture Notes

## Request Flow

```mermaid
sequenceDiagram
    participant Django View
    participant UseCase (Service)
    participant Gateway (Repository)
    participant Oracle RMAN

    Django View->>UseCase: Call execute(params)
    UseCase->>Gateway: Request data or operation
    Gateway->>Oracle RMAN: Raw Read-Only SQL Query
    Oracle RMAN-->>Gateway: Result Set
    Gateway-->>UseCase: Map to Python Dict/Entity
    UseCase-->>Django View: Return BackupStatus Entity
```

## Current Structure

- `projectRelback/`: project configuration and root URLs.
- `coreRelback/`: domain app with models, forms, views and templates.
- `static/`: shared static assets.
- `databaseProject/`: SQL artifacts and operational scripts.

## Architectural Guardrails

- Keep views slim and cohesive.
- Move reusable domain logic to services/helpers.
- Prefer explicit migrations for model evolution.
- Keep template behavior server-first with minimal JS coupling.
- Oracle Catalog queries must be encapsulated in read-only gateways, ensuring Django never attempts accidental writes to Oracle RMAN system tables.
