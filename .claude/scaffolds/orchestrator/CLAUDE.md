# {{ORCHESTRATOR_NAME}} — CLAUDE.md (orchestrator tier)

## Claude Preamble
<!-- VERSION: 2026-05-19-v47.2 -->
<!-- SYNC-SOURCE: ~/.claude/conventions/universal-claudemd.md -->

**Universal laws** (§4), **Plugin dispatch** (§44), **Tool-cascade workflow** (§46),
**Multi-role agent matrix** (§47), **Parsimony / smallest-tool-first** (§48),
**Audit triage discipline** (§49), **Source-of-truth matrix** (§50),
**Composite cascade catalog** (§51), **Session launch context + unattended-mode
contract** (§52), **Recurrence detection + root-cause escalation** (§53).
Sub-sections honored: **§27.5 closure-claim live-probe discipline**, **§27.6
design-doc self-consistency closing-pass**, **§29 confirmation triangle**, **§29.5
protected paths**, **§43.6 verify-before-claim**, **§43.7 names-not-evidence**.

**Sources**: `~/.claude/conventions/universal-claudemd.md` + `~/.claude/conventions/project-hygiene.md`.

## Identity & Role

This repo is a **registry-as-IaC orchestrator** for **{{VENDOR_NAME}}**. It
reconciles a declared YAML registry against the live vendor API, surfaces drift,
and (with `--confirm`) creates missing entities.

Pattern source: ADR-068 site-discoverability template (`platform-docs/04-decision-memory/adrs/ADR-068-site-discoverability-orchestration.md`).
Sibling examples: `vps_host/scripts/glitchtip-orchestrator/` (commit `83a04df`), `vps_host/scripts/mailcow-orchestrator/` (commit `e04e612`), `vps_host/scripts/site-discoverability/`.

## Stack

- Python 3.12+
- `pyyaml` (registry loader), `requests` (vendor API)
- `pytest` (unit tests with mock-friendly client)
- `ruff` (lint/format)

## Build / Test / Deploy

```bash
make lint        # ruff check
make test        # pytest -v
make reconcile   # read-only diff of registry vs live API
make apply       # mutating: create missing live entities (gated by --confirm)
```

## Key Directories

- `scripts/{{ORCHESTRATOR_NAME}}/registry.yml` — operator-authored declared state
- `scripts/{{ORCHESTRATOR_NAME}}/{{ORCHESTRATOR_PKG}}/orchestrator.py` — CLI entry-point
- `scripts/{{ORCHESTRATOR_NAME}}/{{ORCHESTRATOR_PKG}}/lib/` — client + registry + state_diff
- `scripts/{{ORCHESTRATOR_NAME}}/tests/` — pytest suite
- `docs/runbooks/{{ORCHESTRATOR_NAME}}-reconcile.md` — operator runbook
- `docs/specs/{{ORCHESTRATOR_NAME}}-design.md` — design doc

## Critical domain rules

- **§27 append-only artefact discipline**: `registry.yml` writeback fields are
  `entity_id` + `last_reconciled` only; intent fields (`desired_state`, `slug`,
  etc.) are operator-authored and never overwritten.
- **§27.5 closure-claim live-probe**: every mutation logs the API request line
  + response status. No bare "applied/created/wired" claims without probe.
- **§29 confirmation triangle for delete/mutation**: `apply` requires
  `--confirm` OR `--{{ENTITY_NAME}}` blast-radius limiter.
- **§43.7 names-not-evidence**: slug-to-id resolution is API-driven; never
  inferred from filenames or registry rows.
- **§52 unattended-mode**: subcommands return non-zero on hard failure; never
  block on input.

## Security & Secrets

- Vendor API token is read from environment (e.g. `{{VENDOR_NAME_UPPER}}_API_TOKEN`).
- Render via Infisical (path: `{{INFISICAL_PATH}}/<entity>/<secret-key>`).
- Never commit tokens; `.env*` is gitignored.

## External Services / MCPs

- Primary vendor API: `{{API_BASE_URL}}`.
- Secrets: Infisical (`mcp__infisical__get-secret`).

## Doc Maintainers

- `CLAUDE.md` — live contract; update on stack/scope shift.
- `registry.yml` — operator-authored; reconciler writes back two fields only.
- `docs/specs/{{ORCHESTRATOR_NAME}}-design.md` — design canon.

## Deviations from Universal Laws

None.
