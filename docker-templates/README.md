# Hardened Dockerfile templates (canonical home)

Copy-into-repo Dockerfile archetypes + the fleet hardening convention. This is the
**canonical home** for fleet Dockerfile patterns — when a new repo needs a container,
copy the matching archetype and adapt, rather than hand-rolling a fresh Dockerfile
(the source of the 22-way base/hardening drift documented in
`platform-docs/docs/specs/2026-06-26-fleet-uniformity-gap-register.md` G-08).

`init.sh` propagates project-template into new repos; these templates ride that path.

## Why templates, not a shared base image

A single `Cramraika/base-*` image was REJECTED as the default mechanism (G-08, live-probed
2026-06-26): the fleet's container stacks are **genuinely distinct** — `python:3.11-slim`,
`node:NN-alpine`, multi-stage `next.js` standalone — so one base cannot serve all. A real
base image also adds ongoing cost (a container registry + a build/publish pipeline + a CVE
re-bake cadence + a redeploy per consumer) — an operator build-vs-template decision, not a
unilateral stand-up. Templates give uniform hardening with zero new infra. If the python
trio (anjaan/bulk/aakhara) later justifies a shared `base-python`, it is a deliberate
follow-up (tracked as an OW), not the default.

## The hardening convention (every fleet Dockerfile should carry these)

1. **Non-root user.** Create a system user and `USER` it before `CMD`
   (Semgrep `dockerfile.security.missing-user`). The app binds a high port (>1024),
   so no root is needed at runtime.
2. **`curl` present when a Coolify HTTP health-check is configured.** Coolify's container
   health-check does an HTTP GET; if `curl` (or `wget`) is absent the container reports
   `unhealthy` and every deploy rolls back. (`slim`/`alpine` bases ship neither by default.)
3. **A `HEALTHCHECK` instruction** mirroring the Coolify check, so `docker ps`/Compose
   health gating works even outside Coolify. Keep the path/port in sync with the app's
   health endpoint.
4. **Pinned base tag.** Pin the major (and let Renovate `pinDigests` add the digest) — never
   float (`:latest`). Renovate keeps the pin current fleet-wide.
5. **WHY-comments on non-obvious hardening** (e.g. *why* curl is installed) so a future
   editor doesn't strip a load-bearing line. The `python.Dockerfile` carries the
   anjaan-app exemplar's comments verbatim — they were earned by real rollback incidents.

## Archetypes

| File | Stack | Source exemplar |
|---|---|---|
| `python.Dockerfile` | Python service (FastAPI/gunicorn), `python:3.11-slim` | anjaan-app (verified-working, deployed) |
| `node-alpine.Dockerfile` | Node service/static, multi-stage `node:NN-alpine` | host_page pattern + hardening added |
| `nextjs-standalone.Dockerfile` | Next.js standalone output, multi-stage | vagary-earnings / bellring-landing (byte-identical pair) |

## Applying to existing repos

Per-instance application to already-deployed apps is **deploy-gated** (serialize, watch the
post-deploy health) and tracked as a gated OW, not auto-applied. The byte-identical
`vagary-earnings` / `bellring-landing` Next.js Dockerfiles are the canonical
`nextjs-standalone.Dockerfile` — keep them in sync with this template on next touch.
