# Runbook — Relback

Procedimentos operacionais: subir ambiente, migrações, rollback e variáveis críticas.

---

## 1. Subir o ambiente

**Docker/Podman:**

```bash
cp .env.example .env
docker compose up -d
# ou: podman compose up -d
```

**Com Oracle Database Free:**

```bash
cp .env.example .env
# Definir ORACLE_PWD no .env
docker compose -f docker-compose.yml -f docker-compose.oracle.yml up -d
# Aguardar log do oracle: "DATABASE IS READY TO USE"
```

**Local (venv):**

```bash
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
export DJANGO_SETTINGS_MODULE=projectRelback.settings_local
python manage.py migrate --noinput
python manage.py runserver
```

---

## 2. Migrações

| Comando | Uso |
|--------|-----|
| `python manage.py migrate --noinput` | Aplicar migrações (CI/containers). |
| `python manage.py makemigrations` | Gerar migrações após alterar models. |
| `python manage.py showmigrations` | Listar aplicadas e pendentes. |

---

## 3. Rollback

```bash
python manage.py migrate coreRelback <nome_migração_anterior>
```

Só use se a migração for reversível.

---

## 4. Variáveis críticas

| Variável | Obrigatória | Descrição |
|----------|-------------|-----------|
| `SECRET_KEY` | Sim (produção) | Chave secreta Django. |
| `ALLOWED_HOSTS` | Sim (produção) | Hosts permitidos (vírgula). |
| `DEBUG` | Não | `False` em produção. |
| `DB_ENGINE` / `DB_NAME` / `DB_USER` / `DB_PASSWORD` | Se não SQLite | Backend Django. |
| `ORACLE_CATALOG_DSN` / `ORACLE_CATALOG_USER` / `ORACLE_CATALOG_PASSWORD` | Não | Catálogo RMAN; vazio = demo. |
| `DEMO_MODE` | Não | `True` = dados fictícios sem Oracle. |

Ver `.env.example` para a lista completa.

---

## 5. Health check

```bash
curl -s http://localhost:8000/health/
```

200 = ok; 503 = degradado (DB ou catálogo inacessível).

---

## 6. Superusuário e dados demo

```bash
python manage.py createsuperuser
python manage.py seed_demo
# Opcional: python manage.py seed_demo --flush
```

---

*Documentação em `docs/` conforme convenção do projeto.*
