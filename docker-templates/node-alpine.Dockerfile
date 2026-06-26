# Hardened Node service Dockerfile (multi-stage, alpine) — fleet canonical template.
# Pattern source: host_page (build → runtime split); hardening (non-root + curl +
# HEALTHCHECK) added per docker-templates/README.md convention.
#
# Adapt: the build output dir (dist/), EXPOSE/PORT, and CMD to your app.

FROM node:22-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm install --ignore-scripts --legacy-peer-deps
COPY . .
RUN npm run build

FROM node:22-alpine
WORKDIR /app

# curl: required by the Coolify HTTP health-check + the HEALTHCHECK below
# (alpine ships neither curl nor wget for HTTP by default).
RUN apk add --no-cache curl

# Non-root runtime user (Semgrep dockerfile.security.missing-user).
RUN addgroup -g 1001 -S nodejs && adduser -S nodeapp -u 1001

COPY --from=builder --chown=nodeapp:nodejs /app/dist ./dist
COPY --from=builder --chown=nodeapp:nodejs /app/node_modules ./node_modules
COPY --from=builder --chown=nodeapp:nodejs /app/package.json ./

USER nodeapp
EXPOSE 5000
ENV NODE_ENV=production
ENV PORT=5000

HEALTHCHECK --interval=30s --timeout=10s --start-period=15s --retries=3 \
    CMD curl -fsS "http://localhost:${PORT}/" || exit 1

CMD ["node", "dist/index.js"]
