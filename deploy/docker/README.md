# Docker Compose — Relback

Orquestração da aplicação (e opcionalmente Oracle). **Execute na raiz do repositório.**

Containers usam o prefixo **`relback-`** (ex.: `relback-web-1`, `relback-nginx-1`).

## Scripts (recomendado)

```bash
# Subir (cria .env a partir de .env.example se não existir)
./deploy/scripts/compose-up.sh
./deploy/scripts/compose-up.sh --oracle   # com Oracle Free

# Migrações e dados demo
./deploy/scripts/compose-up.sh exec web python manage.py migrate --noinput
./deploy/scripts/compose-up.sh exec web python manage.py seed_demo

# Parar
./deploy/scripts/compose-down.sh
./deploy/scripts/compose-down.sh --oracle
```

## Arquivos

| Arquivo | Uso |
|--------|-----|
| `docker-compose.yml` | Web, Redis, Nginx. SQLite em volume. |
| `docker-compose.oracle.yml` | Override com Oracle Database Free (porta 1521). |

## URLs

- **Nginx:** http://localhost:8080 (porta 80 não exposta em rootless)
- **Gunicorn direto:** http://localhost:8000
- **Login:** admin / demo1234

## Troubleshooting

Ver **`docs/TROUBLESHOOTING_CONTAINERS.md`** para fluxo de investigação e erros comuns.
