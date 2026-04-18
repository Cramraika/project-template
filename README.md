# Project Template

> **Ready-to-fork GitHub Template with Claude Code v8 conventions, CI/CD, security rules, and 3 tiered CLAUDE.md variants baked in.**

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

### Common preamble

All three variants open with the same v8 preamble:
- `VERSION: 2026-04-19-v8` tagged + `SYNC-SOURCE` pointing to `~/.claude/conventions/universal-claudemd.md`
- References the 21 universal sections Claude should honor (laws, MCP routing, drift protocol, capability resolution, SKILL POLICY, session continuity, decision queue, attestation, cite format, three-way disagreement, pre-conditions, provenance markers, redaction rules, token budget, tool-failure fallback, prompt-injection rule, append-only discipline, BLOCKED_BY markers, stop-loss ladder, business-invariant checks, plugin rent rubric, context ceilings)
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

Running `./init.sh` prompts for three inputs:
1. **Project name** — substitutes `[PROJECT_NAME]` in `CLAUDE.md`
2. **Stack** (`node` / `python` / `fullstack` / `apps-script`) — substitutes `[STACK]`, copies the right `.gitignore`, picks the matching CI workflow
3. **Tier** (`A` / `B` / `C`, default `C`) — picks which `CLAUDE.md.*` variant becomes `CLAUDE.md`

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
