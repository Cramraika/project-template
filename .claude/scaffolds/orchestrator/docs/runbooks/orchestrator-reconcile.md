# {{ORCHESTRATOR_NAME}} — reconcile runbook

> Operator runbook for `{{ORCHESTRATOR_NAME}}` registry-as-IaC orchestrator.
> Pattern source: ADR-068 site-discoverability template.

## Purpose

Reconcile the declared YAML registry against live {{VENDOR_NAME}} state. Surface
drift; on `--confirm`, create missing entities for `desired_state: live` rows.

## Prerequisites

- `{{VENDOR_NAME_UPPER}}_API_TOKEN` rendered via Infisical
  (path: `{{INFISICAL_PATH}}/<entity>/<key>`).
- Optional: `{{VENDOR_NAME_UPPER}}_BASE_URL` to override registry default.
- Optional: `REGISTRY=/path/to/registry.yml`.

## Recurring schedule (cron)

```cron
# /etc/cron.d/{{ORCHESTRATOR_NAME}}-reconcile
SHELL=/bin/bash
PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
15 * * * * root /usr/local/bin/with-secrets.sh -- {{ORCHESTRATOR_NAME}} reconcile --json >> /var/log/{{ORCHESTRATOR_NAME}}-reconcile.log 2>&1
```

## Subcommands

### `reconcile` (read-only)

```bash
{{ORCHESTRATOR_NAME}} reconcile
{{ORCHESTRATOR_NAME}} reconcile --json
```

Prints a per-{{ENTITY_NAME}} drift report. Exit code 0 on success; non-zero on
unrecoverable errors (missing registry, missing token, API 5xx).

### `apply` (mutating, §29-gated)

```bash
# Dry-run (always safe):
{{ORCHESTRATOR_NAME}} apply

# Apply ALL missing live entities (full blast radius):
{{ORCHESTRATOR_NAME}} apply --confirm

# Apply ONE entity (narrow blast radius):
{{ORCHESTRATOR_NAME}} apply --confirm --target <name>
```

§27.5 closure-claim live-probe: each create logs the POST request line + the
201 response with `entity_id`. Registry writeback is persisted with a `.bak`
snapshot of the prior state.

### `list-live`

```bash
{{ORCHESTRATOR_NAME}} list-live
```

## Operator-OOB activation flow (TBD → live)

1. Operator authors a new row with `desired_state: tbd`.
2. `reconcile` reports the row under DECLARED tbd.
3. Operator validates entity readiness (e.g. domain DNS, OAuth scopes).
4. Operator flips `desired_state: tbd` → `live` in `registry.yml`.
5. Operator runs `{{ORCHESTRATOR_NAME}} apply --confirm --target <name>`.
6. Re-run `reconcile` to verify in-sync.

## Failure modes

| Symptom | Likely cause | Fix |
|---|---|---|
| `FATAL: {{VENDOR_NAME_UPPER}}_API_TOKEN unset` | Secret not rendered | Run via `with-secrets.sh` wrapper |
| `no registry.yml found` | Default path missing | Pass `--registry` or set `REGISTRY=` |
| `requests.HTTPError 401` | Token revoked / expired | Rotate token in Infisical; re-render |
| Persistent UNMANAGED entries | Live state not declared | Add row to registry OR delete live entity |
