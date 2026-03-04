#!/usr/bin/env sh
# Run from repo root. Stops and removes the relback stack.
# Usage: ./deploy/scripts/compose-down.sh [--oracle] [options]

set -e
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
cd "$REPO_ROOT"

[ -d "${HOME:-/tmp}/.config/containers" ] && touch "${HOME:-/tmp}/.config/containers/nodocker" 2>/dev/null || true
export PODMAN_COMPOSE_WARNING_LOGS=false

COMPOSE_FILES="-f deploy/docker/docker-compose.yml"
if [ "${1:-}" = "--oracle" ]; then
  shift
  COMPOSE_FILES="$COMPOSE_FILES -f deploy/docker/docker-compose.oracle.yml"
fi

COMPOSE_PROJECT="-p relback"

if ! docker compose $COMPOSE_PROJECT $COMPOSE_FILES down "$@"; then
  echo "Compose down failed (e.g. Podman rootless + Oracle). Force-removing remaining containers..."
  ids=$(docker compose $COMPOSE_PROJECT $COMPOSE_FILES ps -a -q 2>/dev/null) || true
  if [ -n "$ids" ]; then
    for id in $ids; do docker rm -f "$id" 2>/dev/null || true; done
    docker compose $COMPOSE_PROJECT $COMPOSE_FILES down "$@" 2>/dev/null || true
  fi
  echo "Stack stopped."
fi
