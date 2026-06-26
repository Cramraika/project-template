# Hardened Python service Dockerfile — fleet canonical template.
# Source exemplar: anjaan-app (verified-working, deployed to Coolify).
# See docker-templates/README.md for the hardening convention.
#
# Adapt: PORT, the install command, and CMD to your app. Keep the non-root
# user, the curl install, and the HEALTHCHECK.

FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# curl is required by the Coolify container healthcheck (HTTP GET on the app port)
# AND by the HEALTHCHECK below. Without it, every deploy rolls back as "unhealthy".
RUN apt-get update \
    && apt-get install -y --no-install-recommends curl \
    && rm -rf /var/lib/apt/lists/*

# Create non-root app user (Semgrep dockerfile.security.missing-user).
# The app binds a high port (>1024) — no root needed at runtime.
RUN groupadd --system app && useradd --system --gid app --create-home app

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
RUN chown -R app:app /app

USER app

ENV PORT=9000

# Mirrors the Coolify HTTP health-check so `docker ps`/Compose health gating works too.
HEALTHCHECK --interval=30s --timeout=10s --start-period=15s --retries=3 \
    CMD curl -fsS "http://localhost:${PORT}/" || exit 1

CMD ["gunicorn", "--bind", "0.0.0.0:9000", "app:app"]
