# Contributing to project-template

This repo is a reusable template, so doc and scaffold changes should be treated
as propagation changes: one edit here affects every future repo created from it.

## Core rules

- Keep `README.md`, `init.sh`, and the shipped scaffold in sync. If the template
  includes a file, the README should mention it, and `init.sh` should preserve
  or remove it intentionally.
- Keep the tiered `CLAUDE.md` variants aligned with the current convention
  contract before changing the bootstrap flow.
- Prefer minimal template surface. If a file exists only for generation-time
  scaffolding, make that explicit and ensure `init.sh` cleans it up.

## When editing template behavior

- Changing a shipped default is a compatibility decision, not just a local edit.
- If a stack-specific file is added, decide whether it should live in
  `.gitignore-templates/`, `.github/workflows/`, or as a repo-root default.
- If a security or docs rule changes, update both the generated files and the
  README explanation.

## Cross-references

- `README.md` — template contract and shipped scaffold
- `CLAUDE.md` — repo operating contract
- `HANDOFF-R6-8708193.md` — recent carry-forward decisions

