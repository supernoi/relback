# Guia de troubleshooting — Containers (RelBack)

Guia para investigar problemas quando a aplicação roda em Docker ou Podman. Pensado para quem tem mais experiência com bancos de dados (ex.: Oracle DBA) e menos com desenvolvimento e containers.

---

## Credenciais padrão (login na tela de Sign In)

Após rodar `seed_demo` (local ou no container):

| Campo    | Valor       |
|----------|-------------|
| **Usuário** | `admin`   |
| **Senha**   | `demo1234` |

Se não conseguir logar, confira se executou `seed_demo` depois das migrações (veja [Fluxo de investigação](#fluxo-de-investigação) abaixo).

---

## Conceitos rápidos

- **Container**: processo isolado (como um “servidorzinho” rodando uma aplicação ou serviço). No RelBack: `web` (Django/Gunicorn), `nginx` (proxy), `redis` (cache), `oracle` (opcional).
- **Compose**: orquestra vários containers juntos. Os nossos arquivos estão em `deploy/docker/` e são chamados via `./deploy/scripts/compose-up.sh`.
- **Prefixo dos containers**: todos os containers deste projeto têm o prefixo **`relback-`** (ex.: `relback-web-1`, `relback-nginx-1`). Use esse nome nos comandos quando for inspecionar um container específico.

---

## Fluxo de investigação

Siga na ordem. Em cada passo, use os **comandos** indicados; se algo falhar, anote a mensagem e vá para a seção [Problemas comuns](#problemas-comuns).

### 1. Os containers estão rodando?

**O que verificar:** se os serviços (web, nginx, redis e, se usar, oracle) estão “up”.

**Comandos (na raiz do repositório):**

```bash
./deploy/scripts/compose-up.sh ps
# ou, se subiu com Oracle:
./deploy/scripts/compose-up.sh --oracle ps
```

**O que esperar:** `relback-web-1`, `relback-nginx-1`, `relback-redis-1` (e, com Oracle, `relback-oracle-1`) com status “Up” ou “running”.

**Se algum estiver “Exited” ou não aparecer:** suba de novo e veja o log:  
`./deploy/scripts/compose-up.sh --oracle logs -f web` (Ctrl+C para sair).

---

### 2. A aplicação responde? (health check)

**O que verificar:** se o Gunicorn (app) está respondendo.

**Comando:**

```bash
curl -s http://127.0.0.1:8000/health/
```

**Resposta esperada:** algo como  
`{"status": "ok", "database": "ok", "oracle_catalog": "unconfigured"}`.

- **Não responde / conexão recusada:** o container `web` pode não estar rodando ou a porta 8000 não está publicada. Volte ao passo 1 e veja os logs do `web`.
- **Responde:** o app está vivo. Se o navegador não abrir, o problema pode ser Nginx ou porta (passo 4).

---

### 3. Logs do container `web` (Django/Gunicorn) — “tail” dos logs

A aplicação **não grava em arquivo de log**: tudo vai para **stdout**. Para fazer o equivalente a “tail -f”:

```bash
# Últimas 100 linhas
./deploy/scripts/compose-up.sh --oracle logs --tail=100 web

# Acompanhar em tempo real (Ctrl+C para sair)
./deploy/scripts/compose-up.sh --oracle logs -f web
```

Sem o script:

```bash
docker compose -p relback -f deploy/docker/docker-compose.yml -f deploy/docker/docker-compose.oracle.yml logs -f web
# ou pelo nome do container:
docker logs -f relback-web-1
```

**O que procurar:**  
`OperationalError`, `Migration`, `No such table`, `no such column`, `500`, tracebacks em Python.  
Se aparecer erro de tabela ou migração, vá em [Migrações e seed_demo](#migrações-e-seed_demo).

---

### 4. Acesso pelo navegador (porta e Nginx)

**URLs corretas:**

- **Com Nginx:** **http://localhost:8080** (não use porta 80 no rootless).
- **Direto no Gunicorn:** **http://localhost:8000** ou **http://127.0.0.1:8000**.

**Se der “Não foi possível acessar / connection refused”:**

1. Confirme a URL: `http://` (não `https://`) e porta **8080** ou **8000**.
2. Se o health em 8000 funcionar mas 8080 não, reinicie o Nginx:  
   `./deploy/scripts/compose-up.sh --oracle restart nginx`

---

### 5. Migrações e seed_demo

**Sintomas:** página inicial em branco, 500, ou “tabela não existe” nos logs; login não funciona com admin / demo1234.

**O que fazer:**

```bash
./deploy/scripts/compose-up.sh --oracle exec web python manage.py migrate --noinput
./deploy/scripts/compose-up.sh --oracle exec web python manage.py seed_demo
```

Se `migrate` falhar com erro de migração, veja [Erros de migração](#erros-de-migração).

---

### 6. Rebuild da imagem (quando mudou código ou migrações)

Se você alterou código ou arquivos de migração:

```bash
./deploy/scripts/compose-up.sh --oracle build --no-cache web
./deploy/scripts/compose-up.sh --oracle up -d --force-recreate web
# Depois rode migrate e seed_demo de novo (passo 5).
```

---

## Problemas comuns

| Sintoma | Possível causa | O que fazer |
|--------|----------------|-------------|
| **ERR_CONNECTION_REFUSED** no navegador | URL errada ou containers parados | Usar **http://localhost:8080** ou **http://127.0.0.1:8000**. Ver passo 1 e 4. |
| **502 Bad Gateway** em 8080 | Nginx não alcança o Gunicorn | `./deploy/scripts/compose-up.sh --oracle restart nginx`. Ou acessar **http://127.0.0.1:8000**. |
| **500 Internal Server Error** na página inicial | Banco não migrado ou sem dados | Rodar `migrate --noinput` e `seed_demo` no container (passo 5). |
| **500 ao fazer login** | Tabela `users` sem coluna `last_login` | Rodar migrações (incl. a que adiciona `last_login`). Rebuild da imagem se precisar. |
| **/health/ não responde** | Imagem antiga ou app não sobe | Rebuild sem cache do `web` (passo 6). Depois `curl -v http://127.0.0.1:8000/health/`. |
| **Login não aceita admin / demo1234** | `seed_demo` não foi executado | Rodar `seed_demo` no container (passo 5). |
| **Erro “env file .env not found”** | Falta arquivo de ambiente | Na raiz: `cp .env.example .env`. Ou usar `./deploy/scripts/compose-up.sh`, que cria `.env` se não existir. |
| **Oracle não sobe / não fica “ready”** | Memória ou primeira inicialização lenta | Verificar memória (≥ 2 GB). Primeira subida pode levar 5–10 min; acompanhe com `logs -f oracle`. |
| **Compose down não para o Oracle (Podman)** | Rootless e rede | Usar `./deploy/scripts/compose-down.sh --oracle`; o script força a remoção se o down normal falhar. |

---

## Erros de migração

- **“duplicate column name”** ou **“no such column”**: a imagem do `web` pode estar com migrações antigas. Rebuild sem cache do serviço `web` (passo 6) e rode `migrate` de novo.
- Sempre que alterar arquivos em `coreRelback/migrations/`, reconstrua a imagem e recrie o container antes de rodar `migrate`.

---

## Comandos de referência rápida

Execute na **raiz do repositório**. Use `--oracle` nos scripts se subiu a stack com Oracle.

| Objetivo | Comando |
|----------|---------|
| Subir a stack | `./deploy/scripts/compose-up.sh --oracle` |
| Ver status dos containers | `./deploy/scripts/compose-up.sh --oracle ps` |
| Logs do app (web) | `./deploy/scripts/compose-up.sh --oracle logs -f web` |
| Health check | `curl -s http://127.0.0.1:8000/health/` |
| Migrações | `./deploy/scripts/compose-up.sh --oracle exec web python manage.py migrate --noinput` |
| Criar admin e dados demo | `./deploy/scripts/compose-up.sh --oracle exec web python manage.py seed_demo` |
| Rebuild do web | `./deploy/scripts/compose-up.sh --oracle build --no-cache web` |
| Parar a stack | `./deploy/scripts/compose-down.sh --oracle` |

---

## Referências

- **Quickstart:** `docs/QUICKSTART.md`
- **Docker/Podman:** `docs/DOCKER_PODMAN.md`
- **README do Compose:** `deploy/docker/README.md`
