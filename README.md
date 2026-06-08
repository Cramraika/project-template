# Project Template

> **Ready-to-fork GitHub Template with Claude Code v52 conventions, CI/CD, security rules, and 3 tiered CLAUDE.md variants baked in.**

[![GitHub Sponsors](https://img.shields.io/github/sponsors/Cramraika?logo=github&label=Sponsor)](https://github.com/sponsors/Cramraika)
[![Use this template](https://img.shields.io/badge/-Use%20this%20template-2ea44f?logo=github)](https://github.com/Cramraika/project-template/generate)

Reusable template for new projects with Claude Code configuration, CI/CD pipelines, security settings, standardized `.gitignore`, Renovate dependency updates, and pre-push branch protection.

## Sponsor

This template encodes months of real-world Claude Code workflow refinement — feel free to [sponsor the work](https://github.com/sponsors/Cramraika) if it saves you time spinning up new repos.

## Quick Start

1. Click **"Use this template"** on GitHub to create a new repo
2. Clone the new repo locally
3. Run the setup script:
   ```bash
   chmod +x init.sh && ./init.sh
   ```
4. Fill in the remaining placeholders in the generated `CLAUDE.md` (`[DESCRIPTION]`, `[VISION]`, role-lanes, build/test commands, etc.)
5. Commit and push

## The 3 CLAUDE.md tier variants

The template ships with **three tier-scaled `CLAUDE.md` variants**. `init.sh` copies one of them to `CLAUDE.md` at setup time based on your Tier answer; the other two plus the original `.advanced / .standard / .lightweight` files are then deleted from the new repo.

| Tier | Variant file | Body size | Use when | Sections |
|---|---|---|---|---|
| **A** | `CLAUDE.md.advanced` | ~100+ lines | Complex products — multi-service, DB, domain rules, cross-team | References, Stack+Vision, Role-Lanes, Critical Domain Rules (schema traps, query patterns, business invariants), Build/Test/Deploy, Key Directories, Dependency Graph, Known Limitations, Security, Deployment Envs, External Services/MCPs, Roadmap, Doc Maintainers, Deviations |
| **B** | `CLAUDE.md.standard` | ~60 lines | Typical apps — single service, active feature work | References, Stack+Vision, Role-Lanes, Build/Test/Deploy, Key Directories, Known Limitations, Security, Deployment Envs, External Services, Roadmap, Doc Maintainers, Deviations |
| **C** | `CLAUDE.md.lightweight` | ~30 lines | Utility / scripts / tool repos — low-complexity, mostly stable | References, Stack, Build/Test/Deploy, Key Directories, Security, Deviations |

### Add-on: orchestrator scaffold

Beyond the 3 tier variants, `init.sh` can additionally render an **orchestrator scaffold** per [ADR-068 registry-as-IaC pattern](https://github.com/Cramraika/platform-docs/blob/main/04-decision-memory/adrs/ADR-068a-site-discoverability-orchestration.md). Pick this when the new repo's purpose is to **manage per-entity lifecycle against a vendor API** (Glitchtip projects, Mailcow domains, GSC properties, Cloudflare zones, etc.) in a `reconcile` + `apply` pattern.

Reference orchestrators:
- `vps_host/scripts/glitchtip-orchestrator/` (commit `83a04df`)
- `vps_host/scripts/mailcow-orchestrator/` (commit `e04e612`)
- `vps_host/scripts/site-discoverability/`

The scaffold renders Python 3.12+ with `pytest` + `ruff`, a vendor-API client + YAML registry + state-diff lib, `reconcile` / `apply` / `list-live` subcommands, a runbook, a design-doc skeleton (with §27.6 closing-pass checklist), and CI (`ruff` + `pytest` + jq registry-shape lint). Out of the box: **14 unit tests pass** on the rendered example.

Placeholders prompted (8): `ORCHESTRATOR_NAME`, `VENDOR_NAME`, `API_BASE_URL`, `INFISICAL_PATH`, `ENTITY_NAME`, `ENTITY_NAME_PLURAL`, `ENTITY_API_PATH` (+ derived `ORCHESTRATOR_PKG` from `ORCHESTRATOR_NAME`).

### Common preamble

All three variants open with the same slim v52 preamble:
- `VERSION: 2026-06-04-v52` tagged + `SYNC-SOURCE` pointing to `~/.claude/conventions/universal-claudemd.md`
- Universal laws (§1–§55) are NOT inlined — they load from `~/.claude/conventions/` (`universal-claudemd.summary.md` → `universal-claudemd.md` + `project-hygiene.md`) and are always in context; the preamble's job is to point at them + remind not to assume their content from memory (consult/verify per §34 / §43.6 / §43.7)
- Sourced from `~/.claude/conventions/universal-claudemd.md` and `~/.claude/conventions/project-hygiene.md`

Keep the preamble in sync across all per-repo files via `~/.claude/scripts/sync-preambles.py`.

### Placeholders

All three variants contain bracketed placeholders. `init.sh` fills two of them automatically; you fill the rest manually after setup:

| Placeholder | Filled by | Example |
|---|---|---|
| `[PROJECT_NAME]` | `init.sh` (from prompt) | `my-cool-app` |
| `[STACK]` | `init.sh` (from prompt) | `Node.js`, `Python`, `Python + Node.js + Docker`, `Google Apps Script` |
| `[DESCRIPTION]` | manual | One-sentence business line |
| `[VISION]` | manual (standard/advanced) | Pinnacle form — drives role-lane activation |
| `[DEV COMMAND]`, `[BUILD COMMAND]`, etc. | manual | Stack-specific |
| Role-lanes, domain traps, invariants | manual | Depends on project |

## What's Included

| File / Dir | Purpose |
|---|---|
| `CLAUDE.md.advanced` / `.standard` / `.lightweight` | Tier-scaled project instruction templates |
| `.claude/settings.json` | Universal deny list for dangerous commands |
| `.gitignore-templates/` | Language-specific `.gitignore` (node / python / fullstack / apps-script) |
| `.github/workflows/` | CI/CD pipeline templates (node, python, fullstack, docker variants) + `renovate.yml` |
| `.github/FUNDING.yml` | Sponsor config |
| `.githooks/pre-push` | Blocks direct push to `main/master` (auto-installed by init.sh) |
| `.env.example` | Environment variable placeholder |
| `renovate.json` | Renovate dependency-update config (auto-merge minor/patch dev deps) |
| `init.sh` | Interactive setup script |

## `init.sh` behavior

Running `./init.sh` prompts for these inputs:
1. **Project name** — substitutes `[PROJECT_NAME]` in `CLAUDE.md`
2. **Stack** (`node` / `python` / `fullstack` / `apps-script`) — substitutes `[STACK]`, copies the right `.gitignore`, picks the matching CI workflow
3. **Tier** (`A` / `B` / `C`, default `C`) — picks which `CLAUDE.md.*` variant becomes `CLAUDE.md`
4. **Orchestrator scaffold?** (`y` / `n`, default `n`) — if `y`, prompts for `ORCHESTRATOR_NAME`, `VENDOR_NAME`, `API_BASE_URL`, `INFISICAL_PATH`, `ENTITY_NAME`, `ENTITY_NAME_PLURAL`, `ENTITY_API_PATH`, then renders `scripts/<name>/` per ADR-068
5. **Backup tier** (`T1` / `T2` / `T3` / `skip`) — picks the restic backup playbook scaffold

Then it:
- Copies the chosen tier variant to `CLAUDE.md` + substitutes the two placeholders
- Copies `.gitignore-templates/<stack>.gitignore` to `.gitignore`
- Copies `.github/workflows/ci-<stack>.yml` to `.github/workflows/ci.yml`
- Installs `.githooks/pre-push` into `.git/hooks/` (if inside a git repo)
- **Deletes template scaffolding**: the unused `CLAUDE.md.*` variants, `.gitignore-templates/`, `.githooks/`, unused `.github/workflows/ci-*.yml` templates, and `init.sh` itself

After setup, only the consumed output remains — the scaffolding exits cleanly.

## CI/CD Templates

| Template | Stack |
|---|---|
| `ci-node.yml` | Node.js (ESLint / build) |
| `ci-python.yml` | Python (flake8 lint) |
| `ci-node-docker.yml` | Node.js + Docker build |
| `ci-python-docker.yml` | Python + Docker build |
| `ci-fullstack.yml` | Python backend + Node frontend + Docker |
| `renovate.yml` | Renovate dependency-update scheduler |

## Security Features

Every project created from this template gets:
- `.env` and `.env.*` excluded from git (with `!.env.example` preserved)
- `.claude/settings.local.json` and `.mcp.json` excluded from git
- Deny list blocking: `rm -rf`, `sudo`, `git push --force`, `git reset --hard`
- `.env` read access denied in Claude Code
- `pre-push` hook blocking direct pushes to `main` / `master`
- Renovate `vulnerabilityAlerts.enabled = true`
