#!/bin/sh
# Generate self-signed cert for dev if certs are not mounted (e.g. from certbot).
set -e
CERT_DIR="${CERT_DIR:-/etc/nginx/certs}"
mkdir -p "$CERT_DIR"
if [ ! -f "$CERT_DIR/privkey.pem" ]; then
  echo "No TLS key found; generating self-signed certificate for development."
  openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
    -keyout "$CERT_DIR/privkey.pem" \
    -out "$CERT_DIR/fullchain.pem" \
    -subj "/CN=localhost/O=Relback Dev"
fi
exec nginx -g "daemon off;"
