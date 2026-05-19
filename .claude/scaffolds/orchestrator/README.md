# Orchestrator Tier Scaffold

> **Per ADR-068 + OW-106 — registry-as-IaC orchestrator template.**

This scaffold builds a Python orchestrator repo (or sub-tree) following the canonical pattern proven by:

- **Glitchtip orchestrator** (`vps_host/scripts/glitchtip-orchestrator/`, commit `83a04df`) — per-brand error-tracking project lifecycle.
- **Mailcow orchestrator** (`vps_host/scripts/mailcow-orchestrator/`, commit `e04e612`) — per-domain mailbox + alias lifecycle.
- **Site-discoverability orchestrator** (`vps_host/scripts/site-discoverability/`) — multi-vendor (GSC + GA4 + Bing) onboarding lifecycle.
- **ADR-068** (`platform-docs/04-decision-memory/adrs/ADR-068-site-discoverability-orchestration.md`) — registry-as-IaC + least-privilege SA + master OAuth client.

## What `init.sh` renders

When you choose `orchestrator` tier, `init.sh` prompts for:

| Placeholder | Used in | Example |
|---|---|---|
| `{{ORCHESTRATOR_NAME}}` | dir/package names, CLI entry-point | `glitchtip-orchestrator` |
| `{{ORCHESTRATOR_PKG}}` | Python package (underscored) | `glitchtip_orchestrator` |
| `{{VENDOR_NAME}}` | docs/spec titles, comments | `Glitchtip` |
| `{{API_BASE_URL}}` | registry default base URL | `https://errors.chinmayramraika.in` |
| `{{INFISICAL_PATH}}` | secret path placeholder in registry/runbook | `/glitchtip-orchestrator` |
| `{{ENTITY_NAME}}` | per-row noun in registry (e.g. brand, domain, mailbox) | `brand` |
| `{{ENTITY_NAME_PLURAL}}` | YAML list key | `brands` |
| `{{ENTITY_API_PATH}}` | REST list path noun | `projects` |

After rendering, the scaffold is a working `pytest` skeleton with subcommand-shaped CLI (`reconcile` / `apply` / `list-live`) wired against a mock-friendly client.

## Pattern parameters (8 placeholders)

The 8 placeholders above are sufficient to parameterize a fresh orchestrator from
the Glitchtip / Mailcow / site-discoverability common shape. Anything else
(per-row fields, alert rules, custom subcommands) is left for the operator to
fill in after `init.sh` completes.

## File layout

```
<rendered repo>/
├── CLAUDE.md                          # orchestrator-flavored preamble
├── Makefile                           # reconcile / apply / test / lint targets
├── pyproject.toml                     # Python 3.12+ + pytest + ruff
├── .github/workflows/ci.yml           # ruff + pytest + jq schema check
├── scripts/{{ORCHESTRATOR_NAME}}/
│   ├── pyproject.toml                 # package metadata
│   ├── registry.yml                   # declared state (operator-authored)
│   ├── {{ORCHESTRATOR_PKG}}/
│   │   ├── __init__.py
│   │   ├── __main__.py
│   │   ├── orchestrator.py            # CLI entry-point
│   │   └── lib/
│   │       ├── __init__.py
│   │       ├── client.py              # vendor API client
│   │       ├── registry.py            # YAML loader/saver
│   │       └── state_diff.py          # declared-vs-live diff
│   └── tests/
│       ├── __init__.py
│       ├── test_client.py
│       ├── test_registry.py
│       └── test_state_diff.py
└── docs/
    ├── runbooks/{{ORCHESTRATOR_NAME}}-reconcile.md
    └── specs/{{ORCHESTRATOR_NAME}}-design.md
```

## When to use this tier

Pick `orchestrator` tier when the new repo's purpose is to **manage per-entity
lifecycle against a vendor API** in a reconcile + apply pattern (Sentry/Glitchtip
projects, Mailcow domains, GSC properties, Cloudflare zones, etc.). For
ordinary applications, pick `A` / `B` / `C` instead.

## Universal-rule wiring

The rendered scaffold embeds:

- §27.5 closure-claim live-probe (every mutation logs the API request + response).
- §43.6 verify-before-claim (apply re-reads list endpoint after mutation).
- §43.7 names-not-evidence (slug/id resolution is API-driven).
- §52 unattended-mode contract (non-interactive subcommands; non-zero on hard fail).
- §29 confirmation triangle (`--apply` requires `--confirm` or `--{{ENTITY_NAME}}`).
- §27 append-only artefact discipline (registry writeback fields only).
