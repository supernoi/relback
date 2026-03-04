#!/usr/bin/env sh
# Run from repo root. Usage: ./deploy/scripts/compose-up.sh [--oracle] [up -d|build|logs|exec ...]
# Creates .env from .env.example if missing. Project name: relback (containers relback-web-1, etc.)

set -e
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
cd "$REPO_ROOT"

# Ensure .env exists
if [ ! -f .env ]; then
  if [ -f .env.example ]; then
    cp .env.example .env
    echo "Created .env from .env.example"
  else
    echo "Error: .env not found and .env.example missing. Create .env with at least DJANGO_SECRET_KEY."
    exit 1
  fi
fi

# Quiet Podman messages when using docker alias
[ -d "${HOME:-/tmp}/.config/containers" ] && touch "${HOME:-/tmp}/.config/containers/nodocker" 2>/dev/null || true
export PODMAN_COMPOSE_WARNING_LOGS=false

COMPOSE_FILES="-f deploy/docker/docker-compose.yml"
if [ "${1:-}" = "--oracle" ]; then
  shift
  COMPOSE_FILES="$COMPOSE_FILES -f deploy/docker/docker-compose.oracle.yml"
fi

COMPOSE_PROJECT="-p relback"

if [ $# -eq 0 ]; then
  set -- up -d
fi

exec docker compose $COMPOSE_PROJECT $COMPOSE_FILES "$@"
