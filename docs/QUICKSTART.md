# Quickstart — Relback

Comandos para iniciar o servidor em cada modo. Detalhes: `docs/ARCHITECTURE.md` e `docs/RUNBOOK.md`.

---

## Pré-requisitos

- Python 3.12+
- Node 20 (para build do tema Tailwind, se compilar CSS localmente)

```bash
python3 -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
```

---

## 1. Servidor normal (local com SQLite + dados demo)

```bash
export DJANGO_SETTINGS_MODULE=projectRelback.settings_local
# Se der erro "no such column": rm -f db.sqlite3 e rode de novo
python manage.py migrate --run-syncdb
python manage.py seed_demo
python manage.py runserver
```

- **URL:** http://127.0.0.1:8000  
- **Login:** `admin` / `demo1234`

---

## 2. Modo teste/demo (sem Oracle)

**Opção A — Local:** idem ao “Servidor normal” acima.

**Opção B — Docker/Podman:**

```bash
cp .env.example .env
docker compose up --build
# Em outro terminal:
docker compose exec web python manage.py seed_demo
```

- **URL:** http://localhost:8000  
- **Login:** `admin` / `demo1234`

**Opção C — Testes automatizados:**

```bash
DJANGO_SETTINGS_MODULE=projectRelback.settings_test python manage.py test coreRelback
```

---

## 3. Modo debug (sem banco)

Para inspeção de templates/estáticos sem migrações:

```bash
export DJANGO_SETTINGS_MODULE=projectRelback.settings_dev
python manage.py runserver
```

---

## 4. Resumo dos modos

| Modo           | Settings         | Comando típico                          |
|----------------|------------------|-----------------------------------------|
| Normal (demo)  | `settings_local` | `migrate --run-syncdb` → `seed_demo` → `runserver` |
| Docker         | compose          | `docker compose up --build` + `exec … seed_demo`    |
| Testes         | `settings_test`  | `python manage.py test coreRelback`     |
| Debug (sem DB) | `settings_dev`   | `runserver`                             |

---

## 5. Health check

```bash
curl -s http://127.0.0.1:8000/health/
```

Resposta esperada (ex.): `{"status": "ok", "database": "ok", "oracle_catalog": "unconfigured"}`.
