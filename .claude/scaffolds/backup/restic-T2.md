# Backup Tier T2 — Weekly Config-Only

**Source:** copied by `init.sh` from `project-template/.claude/scaffolds/backup/restic-T2.md`.
**Canonical playbook:** `platform-docs/05-architecture/part-B-service-appendices/vps-admin/substrate/restic.md`.
**Backup-class taxonomy:** B1–B9 — see `docs/audits/restic-session-worklog-2026-05-18.md` §W3 3.4.

---

## What Tier 2 means

**Config-only.** No large stateful data; the only thing to preserve is the **Coolify app config** (env vars, build config, persistent-storage mounts) plus the **Infisical env-export** for the product's secrets. Source code is on GitHub; databases (if any) are external-managed or already covered by their own Tier-1 backup at the substrate level.

This scaffold applies to:
- Coolify-deployed apps with no canonical state on the VPS filesystem
- Static sites + landing pages (host_page, portfolio)
- Chrome extension backends with no persistent DB on VPS (bellring-server before postgres migration)
- Internal admin tooling whose state lives in an external SaaS (n8n workflows that store state in upstream-managed DB)

Reference T2 products from the master tier map (restic-session-worklog §W3 3.5): `host_page`, `portfolio`, `bellring-server`, `bellring-extension`, `anjaan-app`, `aakhara`, `vagary-earnings`, `Automated-sales-manager-main`, `n8n-workflows`.

## Backup class

**B6** — config-only.

Pattern: the daily Coolify config dump + Infisical env-export, ingested by the **substrate-config batch cron** running 02:15 UTC on core-1 against `/data/coolify/source`. The product itself does **not** need its own `/etc/cron.d/` file — the substrate batch already covers it.

## Cron path + schedule

**No additional cron needed if product is Coolify-deployed.**

The existing substrate batch cron at `/etc/cron.d/main-restic-backup` (02:15 UTC daily — see live playbook §2 line 45) walks `/data/coolify/source` and restic-ingests every app's config. New Coolify apps are picked up automatically on next run.

For non-Coolify T2 products (rare — e.g. raw systemd-unit-deployed services), add a minimal config-dump script invoked by the same batch wrapper.

## Wrapper invocation

The substrate batch wrapper `/usr/local/bin/restic-backup-main-batch.sh` already covers Coolify config. **No product-side wrapper authoring required.**

If the product writes any out-of-Coolify config (e.g. an in-repo `.env` referenced by a sidecar systemd unit), add the path to the substrate batch include-list via vps-ansible `vps-ansible/roles/restic-backup-batch/vars/main.yml` `extra_config_paths:`.

## Tag strategy

```
restic backup … \
  --tag <product> \
  --tag substrate-config
```

- `--tag <product>` for per-product retrieval.
- `--tag substrate-config` flags T2 cohort — distinct from `substrate-data` T1 cohort. Retention applies per-tag.

## Retention

T2 retention is enforced by the same `restic-prune.service` against the `substrate-config` tag cohort with a **weekly-leaning** policy:

```
restic forget --keep-weekly=12 --keep-monthly=12 --keep-yearly=3 \
              --prune --max-unused=10% \
              --tag substrate-config
```

(Daily snapshots produced by the 02:15 batch are forget-collapsed weekly; configs change rarely so finer granularity wastes space.)

## Offsite

Same `full-backup.sh` fan-out as T1 — B2 + CF R2 + GCS daily parity. Config is small (<100 MB per product) so egress is negligible.

## Restore

Full config restore from a Coolify config snapshot:

1. `restic restore <snapshot-id> --target /tmp/restore-<product> --include /data/coolify/source/<app-uuid>`
2. Copy `docker-compose.yml` + `.env` + `coolify.yml` back into Coolify's app directory OR re-import via Coolify API (`POST /api/v1/applications/import`).
3. Restore Infisical env-export to the project's `production` env (`infisical secrets set --import-file=…`).
4. Trigger Coolify deploy; verify app comes up green.

Document the first-time restore-test (Variant B sample-restore) in `docs/audits/restic-restore-drill-<YYYY-MM-DD>-<product>.md`. T2 does **not** require quarterly Variant C drills — the substrate batch is drilled as a whole quarterly per ADR-019-A7.

## Onboarding checklist (numbered)

1. **Confirm tier.** Cross-check master tier map (restic-session-worklog §W3 3.5). T2 is the default for any non-stateful Coolify-deployed product.
2. **Confirm Coolify deployment.** If product is not on Coolify, escalate to T2-non-Coolify variant (rare; talk to vps-admin).
3. **Confirm no canonical state on VPS filesystem.** Audit bind mounts via `docker inspect <container> | jq '.Mounts'`. Any non-config mount = re-classify as T1 (B7 volume).
4. **Verify substrate-config cron picks up the app.** After Coolify deploy lands, wait one cycle (next 02:15 UTC), then `restic snapshots --tag <product>` should show a snapshot from that batch run.
5. **Verify Infisical env-export coverage** — product's secrets must live under an Infisical project that the daily env-export script (`vps_host/scripts/infisical-env-export.sh`) iterates.
6. **Wire alerts.** `BackupAgeStale{tier="T2"}` fires at >8.4 days (W5.6 E2 alert — 7d × 1.2 grace).
7. **Update CLAUDE.md** `## Backup Tier` section with: T2, B6 class, "covered by substrate-config batch — no product cron".

## Cross-references

- Canonical playbook: `platform-docs/05-architecture/part-B-service-appendices/vps-admin/substrate/restic.md`
- ADRs: ADR-019 + ADR-025 + ADR-030
- Restore runbook: `platform-docs/docs/runbooks/restic-restore.md`
- Worklog: `platform-docs/docs/audits/restic-session-worklog-2026-05-18.md` §W3 + §W10
