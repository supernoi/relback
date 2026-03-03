---
applyTo: "migrations/**/*.sql"
---
## SQL Migration Rules
- All migrations must be reversible. Always provide a .down.sql file.
- Use IF NOT EXISTS / IF EXISTS for idempotency.
- Tables singular snake_case (user, trip, vehicle).
- Primary keys: {table}_id (user_id, trip_id).
- Timestamps: TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP.
- Index all foreign keys.
- Include EXPLAIN ANALYZE output in PR comments for migrations on large tables.
