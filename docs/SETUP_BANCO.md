# Setup do banco de dados — Relback

Configuração do banco para desenvolvimento e produção.

---

## SQLite (local / demo)

Com `settings_local` o Django usa um arquivo SQLite (`db.sqlite3`). Não é necessário instalar outro SGBD.

```bash
export DJANGO_SETTINGS_MODULE=projectRelback.settings_local
python manage.py migrate --run-syncdb
python manage.py seed_demo
```

Se aparecer erro "no such column", apague o arquivo e recrie: `rm -f db.sqlite3` e rode os comandos de novo.

---

## Oracle (produção / catálogo RMAN)

1. Configure o banco no `.env` (ou variáveis de ambiente):
   - `DB_ENGINE=django.db.backends.oracle`
   - `DB_NAME=host:port/service_name`
   - `DB_USER=...` e `DB_PASSWORD=...`
2. Para o **catálogo RMAN** (somente leitura): `ORACLE_CATALOG_USER`, `ORACLE_CATALOG_PASSWORD`, `ORACLE_CATALOG_DSN`.
3. Rode as migrações: `python manage.py migrate --noinput`.

---

## Criar superusuário

```bash
python manage.py createsuperuser
```

---

*Ver também `docs/RUNBOOK.md` e `docs/QUICKSTART.md`.*
