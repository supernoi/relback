# API Design Guidelines

## Principles

- Keep endpoints predictable and resource-oriented.
- Use clear HTTP status codes and deterministic error payloads.
- Version APIs only when compatibility requires it.

## Django Conventions

- Prefer class-based views for reusable behavior.
- Validate input at form/serializer boundary.
- Keep business rules outside views when complexity grows.
- Use Django `F()` expressions for counter updates and `select_for_update()` in critical backup status transactions to prevent race conditions.

## Response Guidelines

- Success payloads should be consistent by endpoint family.
- Error payloads should include machine-readable code + human-readable message. Contract example: `{"error_code": "BACKUP_NOT_FOUND", "message": "The requested backup does not exist", "details": {}}`.
