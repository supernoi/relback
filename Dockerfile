# ==============================================================================
#  Stage 1: Build Tailwind / DaisyUI compressed CSS
# ==============================================================================
FROM node:20-slim AS css-builder

WORKDIR /app

# Install npm dependencies first (cached layer if package.json unchanged)
COPY theme/static_src/package*.json theme/static_src/
RUN cd theme/static_src && npm ci --silent

# Copy config + source CSS
COPY theme/static_src/tailwind.config.js theme/static_src/
COPY theme/static_src/postcss.config.js  theme/static_src/
COPY theme/static_src/src/                theme/static_src/src/

# Copy templates and JS that Tailwind scans for class names
COPY coreRelback/templates/ coreRelback/templates/
COPY static/js/             static/js/

# Build minified CSS → theme/static/css/dist/styles.css
RUN cd theme/static_src && npm run build

# ==============================================================================
#  Stage 2: Python / Gunicorn runtime
# ==============================================================================
FROM python:3.13-slim AS runtime

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    DJANGO_SETTINGS_MODULE=projectRelback.settings_prod

WORKDIR /app

# Install Python production dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application source
COPY . .

# Overlay compiled CSS from Stage 1
COPY --from=css-builder /app/theme/static/css/dist/ theme/static/css/dist/

# Collect static files for WhiteNoise
# SECRET_KEY placeholder satisfies settings_prod import; not used at collectstatic
RUN DJANGO_SECRET_KEY=build-phase-placeholder \
    python manage.py collectstatic --no-input

# Non-root user for security
RUN useradd --no-create-home --shell /bin/false relback \
    && chown -R relback:relback /app
USER relback

EXPOSE 8000

# Tune workers via GUNICORN_WORKERS (default: 3 sync workers)
CMD ["sh", "-c", \
     "gunicorn projectRelback.wsgi:application \
      --bind 0.0.0.0:8000 \
      --workers ${GUNICORN_WORKERS:-3} \
      --timeout 120 \
      --access-logfile - \
      --error-logfile -"]
