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

Imagem oficial: `container-registry.oracle.com/database/free:latest` (faça `docker login container-registry.oracle.com` antes do primeiro pull).

```bash
cp .env.example .env
# Opcional: ORACLE_PWD=YourSysPassword (senha SYS; default no compose: oracle)

docker compose -f docker-compose.yml -f docker-compose.oracle.yml up -d
# Aguardar no log: "DATABASE IS READY TO USE" (primeira vez pode levar 5–10 min)
docker compose -f docker-compose.yml -f docker-compose.oracle.yml logs -f oracle
```

No `.env`, configure o catálogo RMAN (pluggable DB = FREEPDB1):

- `ORACLE_CATALOG_DSN=oracle:1521/FREEPDB1`
- `ORACLE_CATALOG_USER=` e `ORACLE_CATALOG_PASSWORD=` (usuário/senha do schema no Oracle)

Se usar Oracle também como banco do Django: `DB_ENGINE`, `DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_HOST=oracle`, `DB_PORT=1521`.

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
