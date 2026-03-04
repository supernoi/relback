# Docker e Podman — Relback

Procedimentos para build, execução e testes com containers.  
**Guia de troubleshooting:** `docs/TROUBLESHOOTING_CONTAINERS.md`.

---

## Pré-requisitos

- **Docker** (https://docs.docker.com/get-docker/) ou **Podman** (https://podman.io/)
- Para Compose: `docker compose` (Docker 20.10+) ou `podman compose` (plugin)

---

## Testar agora (mínimo)

Execute na raiz do repositório. O script cria `.env` a partir de `.env.example` se não existir:

```bash
./deploy/scripts/compose-up.sh
./deploy/scripts/compose-up.sh exec web python manage.py migrate --noinput
./deploy/scripts/compose-up.sh exec web python manage.py seed_demo
```

Acesse http://localhost:8080 ou http://localhost:8000. Login: admin / demo1234.

---

## Com Oracle Database Free

```bash
./deploy/scripts/compose-up.sh --oracle
# Aguardar log: "DATABASE IS READY TO USE" (primeira vez pode levar 5–10 min)
./deploy/scripts/compose-up.sh --oracle exec web python manage.py migrate --noinput
./deploy/scripts/compose-up.sh --oracle exec web python manage.py seed_demo
```

No `.env`: `ORACLE_PWD`, `ORACLE_CATALOG_DSN=oracle:1521/RELBACKPDB1` (e opcionalmente `ORACLE_CATALOG_USER` / `ORACLE_CATALOG_PASSWORD`).

---

## Comandos úteis

Use os scripts na raiz (ou `-f deploy/docker/docker-compose.yml` e `-f deploy/docker/docker-compose.oracle.yml` com `-p relback`):

| Comando | Descrição |
|--------|-----------|
| `./deploy/scripts/compose-up.sh` | Sobe em background. |
| `./deploy/scripts/compose-up.sh logs -f web` | Logs do app. |
| `./deploy/scripts/compose-up.sh exec web python manage.py migrate --noinput` | Rodar migrações. |
| `./deploy/scripts/compose-up.sh exec web python manage.py seed_demo` | Carregar dados demo. |
| `./deploy/scripts/compose-down.sh` | Parar e remover containers. |
| `./deploy/scripts/compose-up.sh build --no-cache web` | Rebuild sem cache. |

Com Oracle: use `./deploy/scripts/compose-up.sh --oracle` e `./deploy/scripts/compose-down.sh --oracle`.

---

## Troubleshooting

- **Port 8000 em uso:** altere em `docker-compose.yml` (ex.: `"8001:8000"`).
- **Erro de permissão (Podman):** use rootless; evite volumes com UID/GID incompatíveis.
- **Oracle não sobe:** verifique memória (≥ 2 GB); aguarde o log "DATABASE IS READY TO USE".

---

*Documentação em `docs/` conforme convenção do projeto.*
