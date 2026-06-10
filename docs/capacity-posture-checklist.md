**Category:** Checklist

# Capacity-Posture Checklist (every new service inherits this)

> Fleet standard: platform-docs `02-governance/capacity-posture-standard.md` + ADR-098
> (fleet-capacity campaign 2026-06-10). Fill this BEFORE first deploy; the fleet is
> capacity-bound (ADR-096 — no plan upgrades; new workloads must fit or displace).

- [ ] **Working-set measured** — run the service under representative load; record
      `max_over_time(container_memory_working_set_bytes{name="<svc>"}[7d])` (or 24h minimum).
- [ ] **Memory cap set** — measured peak ×2 (range 1.5–3), rounded up to 64Mi; never below
      current working-set ×1.3 (over-tight caps OOM — worse than uncapped).
- [ ] **CPU cap set** — tier: tiny exporter/sidecar 0.25–0.5 · light app 1.0 ·
      medium service 1.5 · heavy/data 2.0. Exporters that burst at scrape need ≥0.5.
- [ ] **Caps live AND in IaC, same change** — compose `cpus:`+`mem_limit:` / Ansible
      `cpus:`+`memory:` / Coolify limits field (docker update alone is reconcile-fragile).
- [ ] **Uncapped only with rationale** — explicit `uncapped-by-policy: <reason>` comment.
- [ ] **Saturation visibility** — container appears in `ContainerMemoryNearLimit` /
      `ContainerCPUThrottled` scope (capped ⇒ automatic); check the fleet-capacity-overview
      Grafana dashboard renders it.
- [ ] **Restart hooks idempotent** — any render/sync hook that restarts this service must be
      content-hash-gated (`infisical-execute-on-change.sh` pattern), never fire-per-cycle.
- [ ] **Headroom check** — confirm the host's "what still fits" envelope
      (platform-docs `11-compliance/capacity-baseline-<latest>.md` §5) accommodates the
      service's peak; if not, displacement decision BEFORE deploy.
