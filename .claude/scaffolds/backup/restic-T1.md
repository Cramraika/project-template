# Backup Tier T1 — Daily with Offsite Fan-out

**Source:** copied by `init.sh` from `project-template/.claude/scaffolds/backup/restic-T1.md`.
**Canonical playbook:** `platform-docs/05-architecture/part-B-service-appendices/vps-admin/substrate/restic.md` (live deployment state §2 + retention §3 + ADR-019 amendments).
**Backup-class taxonomy:** B1–B9 — see `docs/audits/restic-session-worklog-2026-05-18.md` §W3 3.4.

---

## What Tier 1 means

**SEV1 stateful service.** Postgres / MongoDB / MariaDB / large mission-critical bind-mount volume. Data loss = revenue / user-trust impact. Backup cadence is **daily** with **multi-cloud offsite parity** (B2 + Cloudflare R2 + GCS per ADR-019-A4).

This scaffold applies if any of the following hold:
- Service has a database whose loss is unrecoverable from upstream sources (postgres / mongo / mariadb owning canonical state)
- Service has a large bind-mount volume that needs whole-tree snapshotting (e.g. Immich library, vagary-platform substrate)
- Service is classed Tier-1 in `02-governance/service-playbooks/products/` or the master tier map in restic-session-worklog §W3 3.5

## Backup class

Pick one of:

- **B3** — `docker-exec` with DB-dump pre-hook. Pattern: `docker exec <container> pg_dump … | restic backup --stdin --stdin-filename <db>.sql`. Used by anjaan-app (postgres), Automated-sales-manager-main, vagary-platform news vertical (mongodump), Infisical, Immich.
- **B7** — volume snapshot. Pattern: `restic backup /var/lib/docker/volumes/<name>/_data` (or specific bind-mount path) with appropriate `--exclude` filters. Used by vagary-platform substrate, vagary-voice, Portainer (BoltDB whole-volume).

Choose B3 if the canonical state lives in a database engine that can dump consistently online; choose B7 if the canonical state is a filesystem tree (image library, BoltDB, append-only logs) where a quiesce + cp-tree is the only consistent snapshot. **Never mix** — one tier, one backup class per service.

## Cron path + schedule

```
/etc/cron.d/<product>-restic-backup
```

Daily schedule between 02:00 and 03:00 UTC (off-peak window; spread across products at 5-minute offsets to avoid cache-dir contention on `/var/cache/restic/`). Example header:

```
# /etc/cron.d/<product>-restic-backup
# Tier T1 daily backup — managed by vps-ansible; do not hand-edit.
# Migrate to systemd timer per Pillar 6 (W5.2) when product is graduated.
SHELL=/bin/bash
PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin

15 2 * * * root /usr/local/bin/restic-backup-<product>.sh >> /var/log/restic-<product>.log 2>&1
```

## Wrapper pattern

Pick the matching wrapper from `vps_host/scripts/`:

- **B3 (DB-dump pre-hook):** `backup_or_skip` — emits dump to staging, restic-ingests via `--stdin`, on dump-failure skips the run with a structured log line so the Loki "absence of EXIT line" alert distinguishes skip vs hard-fail.
- **B7 (volume bind):** `backup_volume_or_skip` — quiesces (where applicable), restic-backups the volume path, post-snapshot integrity log.

Both wrappers source secrets via the **Bootstrap-tier mirror** (`set -a; source /root/.infisical-rendered/main-host.env; set +a`) per ADR-012 Amendment 1 §4 + ADR-030 A1/A2 circular-dep mitigation. Wrappers preserve the defensive `restic-backup: EXIT rc=<n>` terminal line.

## Tag strategy

```
restic backup … \
  --tag <product> \
  --tag substrate-data \
  --tag track-A-batch
```

- `--tag <product>` enables per-product `forget --tag <product>` retention scoping without disturbing peers in the same repo.
- `--tag substrate-data` flags the backup as part of the canonical substrate-data set (vs `substrate-config` for T2 — see restic-T2.md).
- `--tag track-A-batch` slots into the Track-A daily-batch retention cohort.

## Retention

T1 retention is **enforced centrally** by the live `restic-prune.service` systemd unit on core-1:

```
restic forget --keep-daily=14 --keep-weekly=8 --keep-monthly=12 --keep-yearly=5 \
              --prune --max-unused=10% \
              --tag track-A-batch
```

- 14 daily, 8 weekly, 12 monthly, 5 yearly snapshots retained (ADR-019 horizon).
- Prune decoupled from backup (per playbook §3 G-NEW-A) — runs Sunday 05:00 UTC off-peak.
- Do **not** add per-product `forget` to the cron wrapper. Retention is global per tag-cohort.

## Offsite fan-out

`/usr/local/bin/full-backup.sh` fans out the daily restic snapshot tar-bundle to all three cloud upstreams (ADR-019-A4 §4):

- `backblaze-1` (Backblaze B2)
- `cloudflare-storage-1` (Cloudflare R2 — primary per ADR-019-A1)
- `gcs-storage-1` (Google Cloud Storage)

Daily parity probes (W5.6 E6) verify B2 size == R2 size == GCS size for current-day objects. If any cloud is degraded, the run still succeeds locally and emits a `restic_offsite_parity_missing{provider=...}` metric.

## Restore test

**Variant C quarterly** per ADR-019-A7 cadence:
- Variant A = on-host repo open + snapshots listing (weekly auto)
- Variant B = sample-file restore from latest snapshot to staging (monthly auto)
- **Variant C = full-service rehydrate to a sandbox container, smoke-test, then teardown (quarterly, operator-driven)**

Document the Variant C drill in `docs/audits/restic-restore-drill-<YYYY-MM-DD>-<product>.md` per the Portainer / mariadb pattern (restic-session-worklog §W3 tier map lines 431-432).

## Onboarding checklist (numbered)

1. **Confirm tier.** Cross-check the master tier map in `docs/audits/restic-session-worklog-2026-05-18.md` §W3 3.5. If product is not yet listed, propose addition via an audit-doc amendment before authoring cron.
2. **Pick backup class** (B3 or B7). Justify in CLAUDE.md `## Backup Tier` section with one sentence on why the canonical state is DB-dump-able vs filesystem-snapshot-only.
3. **Author cron file** at `/etc/cron.d/<product>-restic-backup` via vps-ansible (`vps-ansible/roles/restic-backup-product/`). **Never** hand-edit cron on the host.
4. **Author wrapper** at `/usr/local/bin/restic-backup-<product>.sh` — copy from `vps_host/scripts/restic-backup-template-<B3|B7>.sh` and parameterize.
5. **Register secrets** in Infisical under `vps-ops/production/restic/<product>` (Tier-1) + mirror to Bitwarden "Chinmay VPS Emergency Access" (Tier-2 break-glass) per ADR-025.
6. **Smoke-test on staging** — run the wrapper manually once with `--dry-run`, then once for real, verify EXIT line + snapshot appears in `restic snapshots --tag <product>`.
7. **Enable systemd timer** (Pillar 6 target) — until cutover, cron is acceptable; document the placeholder in cron header.
8. **Wire alerts** — `BackupAgeStale{tier="T1"}` fires at >36h since last snapshot (W5.6 E2 alert). Verify by stopping the wrapper for one cycle on staging and confirming Slack `#backups` red alert.
9. **Schedule Variant C drill** in calendar for quarter-from-onboarding.
10. **Update CLAUDE.md** `## Backup Tier` section with: class, cron path, retention cohort, offsite providers verified, next drill date.

## Cross-references

- Canonical playbook: `platform-docs/05-architecture/part-B-service-appendices/vps-admin/substrate/restic.md`
- ADRs: ADR-019 + Amendments A1/A2/A4/A6/A7/A8 + ADR-025 + ADR-030 A1/A2
- Restore runbook: `platform-docs/docs/runbooks/restic-restore.md`
- DR drill example (Portainer recovery): `platform-docs/docs/runbooks/restic-dr-drill-portainer-recovery.md`
- Worklog: `platform-docs/docs/audits/restic-session-worklog-2026-05-18.md` §W3 + §W10
