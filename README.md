# Project Template

Reusable template for new projects with Claude Code configuration, CI/CD pipelines, security settings, and standardized .gitignore.

## Quick Start

1. Click **"Use this template"** on GitHub to create a new repo
2. Clone the new repo locally
3. Run the setup script:
   ```bash
   chmod +x init.sh && ./init.sh
   ```
4. Review and customize the generated `CLAUDE.md` for your project
5. Commit and push

## What's Included

| File | Purpose |
|------|---------|
| `CLAUDE.md.*` | Project instruction templates (3 tiers) |
| `.claude/settings.json` | Universal deny list for dangerous commands |
| `.gitignore-templates/` | Language-specific .gitignore files |
| `.github/workflows/` | CI/CD pipeline templates |
| `.env.example` | Environment variable placeholder |
| `init.sh` | Interactive setup script |

## Template Tiers

| Tier | Template | Use For |
|------|----------|---------|
| A (Advanced) | `CLAUDE.md.advanced` | Complex projects with DB, multi-service, domain rules |
| B (Standard) | `CLAUDE.md.standard` | Active projects with moderate complexity |
| C (Lightweight) | `CLAUDE.md.lightweight` | Simple scripts, tools, dormant projects |

## CI/CD Templates

| Template | Stack |
|----------|-------|
| `ci-node.yml` | Node.js (ESLint/build) |
| `ci-python.yml` | Python (flake8 lint) |
| `ci-node-docker.yml` | Node.js + Docker build |
| `ci-python-docker.yml` | Python + Docker build |
| `ci-fullstack.yml` | Python backend + Node frontend + Docker |

## Security Features

Every project created from this template gets:
- `.env` and `.env.*` excluded from git (with `!.env.example` preserved)
- `.claude/settings.local.json` and `.mcp.json` excluded from git
- Deny list blocking: `rm -rf`, `sudo`, `git push --force`, `git reset --hard`
- `.env` read access denied in Claude Code
