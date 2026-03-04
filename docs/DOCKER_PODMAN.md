# Docker e Podman — Relback

Procedimentos para build, execução e testes com containers.

---

## Pré-requisitos

- **Docker** (https://docs.docker.com/get-docker/) ou **Podman** (https://podman.io/)
- Para Compose: `docker compose` (Docker 20.10+) ou `podman compose` (plugin)

---

## Testar agora (mínimo)

```bash
cp .env.example .env
# Editar .env: DJANGO_SECRET_KEY (obrigatório); DB_* e ORACLE_* vazios = SQLite + Demo

docker compose up --build
# ou
podman compose up --build
```

Acesse http://localhost:8000. Para dados demo:

```bash
docker compose exec web python manage.py seed_demo
# Login: admin / demo1234
```

---

## Com Oracle Database Free

```bash
cp .env.example .env
# Definir ORACLE_PWD no .env

docker compose -f docker-compose.yml -f docker-compose.oracle.yml up -d
# Aguardar log: "DATABASE IS READY TO USE" (primeira vez pode levar 5–10 min)
```

Configure no `.env` (se usar Oracle como DB do Django): `DB_ENGINE`, `DB_NAME`, `DB_USER`, `DB_PASSWORD`, `ORACLE_CATALOG_*`.

---

## Comandos úteis

| Comando | Descrição |
|--------|-----------|
| `docker compose up -d` | Sobe em background. |
| `docker compose logs -f web` | Logs do app. |
| `docker compose exec web python manage.py migrate --noinput` | Rodar migrações. |
| `docker compose exec web python manage.py seed_demo` | Carregar dados demo. |
| `docker compose down` | Parar e remover containers. |
| `docker compose build --no-cache` | Rebuild sem cache. |

Com Podman: substitua `docker` por `podman`.

---

## Troubleshooting

- **Port 8000 em uso:** altere em `docker-compose.yml` (ex.: `"8001:8000"`).
- **Erro de permissão (Podman):** use rootless; evite volumes com UID/GID incompatíveis.
- **Oracle não sobe:** verifique memória (≥ 2 GB); aguarde o log "DATABASE IS READY TO USE".

---

*Documentação em `docs/` conforme convenção do projeto.*
