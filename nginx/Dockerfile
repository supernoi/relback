# Nginx reverse proxy for Relback (Gunicorn)
# Uses entrypoint to generate self-signed cert for dev when no certs are mounted.
FROM nginx:alpine
RUN apk add --no-cache openssl
COPY nginx.conf /etc/nginx/conf.d/default.conf
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]
