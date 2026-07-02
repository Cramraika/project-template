# project-template

GitHub Template repo for spinning up new projects with the convention-aligned scaffolding (CLAUDE.md tier files + init.sh + .githooks/pre-push + .gitignore baseline).

---

## Claude Preamble
<!-- VERSION: 2026-07-02-v54 -->
<!-- SYNC-SOURCE: ~/.claude/conventions/universal-claudemd.md -->

**Universal laws (§1–§55) load via user-level `~/.claude/conventions/`** — `universal-claudemd.summary.md` (≤50-line salient view, read FIRST) → the 9-invariant kernel in `constitution.md` → per-§ detail in `~/.claude/rules/*.md` (read-on-demand; INDEX.md maps §→module) + `project-hygiene.md`. Do **NOT** assume their content from memory; consult + verify before asserting (§34 / §43.6 / §43.7). The `## Active Cluster Playbooks` block below names this repo's situational playbooks **read-on-demand** (§49.10): Read the named playbook when its trigger fires — never guess its contents; always-load guardrails are inline. Sync: `~/.claude/scripts/sync-preambles.py` (manual cadence; run after any source edit).

## Active Cluster Playbooks (read-on-demand — §49.10; bodies at ~/.claude/conventions/playbooks/)
<!-- BEGIN PLAYBOOKS BLOCK (managed by sync-preambles.py — read-on-demand pointers per §49.10; bodies at ~/.claude/conventions/playbooks/) -->

These cluster playbooks apply to this repo. You do NOT know their contents from memory —
**Read the named file when its trigger fires; never assume** (§49.10, §34, §43.6). Bodies are
NOT inlined and NOT @-imported; the always-load GUARDRAILs below are the only parts that must
hold without a Read.

- `commercial-bound.md` — when: license / sponsor-readiness / graph-tool-output / white-label work. GUARDRAIL: never commit/ship GitNexus (PolyForm-NC) graph output from a commercial-bound repo — CGC is the canonical graph source.

<!-- END PLAYBOOKS BLOCK -->

## License classification: personal/private

## Meta-note (this repo IS the template)

This file is the *self-describing* CLAUDE.md for the project-template repo itself. The three sibling files
- `CLAUDE.md.lightweight` (Tier C — minimal scripts/CLI utilities)
- `CLAUDE.md.standard` (Tier B — typical web apps)
- `CLAUDE.md.advanced` (Tier A — multi-stack production systems)

are the **templates** that `init.sh` copies into a new repo. Do not delete or sync-skip them — `sync-preambles.py` updates them in place at every VERSION bump.

## References
- `~/.claude/conventions/universal-claudemd.md` — universal laws, MCP routing
- `~/.claude/conventions/project-hygiene.md` — doc/scratch placement
- `~/.claude/conventions/repo-inventory.md` — where new repos register

## Stack
- **Stack**: Shell + Markdown (template scaffolding only)
- **Tier**: C (Maintenance — touched on convention bumps + init.sh fixes)

## Build / Test / Deploy
```bash
# To use this template for a new repo
gh repo create <new-repo> --template Cramraika/project-template --private --clone
cd <new-repo>
./init.sh   # copies tier file → CLAUDE.md, sets up .githooks, runs initial sed-replaces

# To update the templates themselves
edit CLAUDE.md.{lightweight,standard,advanced}
~/.claude/scripts/sync-preambles.py   # re-syncs preamble blocks in tier files
git add CLAUDE.md.* && git commit -m "chore: bump tier templates to vN"
```

## Key Directories
- `CLAUDE.md.{lightweight,standard,advanced}` — tier template files (copied by init.sh)
- `init.sh` — bootstrap script for new repos (copies tier file, installs pre-push hook)
- `.githooks/pre-push` — branch-protection helper installed into new repos

## Security & Secrets
- No secrets in templates. `.env.example` patterns only.
- `init.sh` MUST not embed credentials.

## VPS Service Navigation (template stub)

Every new repo that deploys onto the dual-VPS platform SHOULD carry a `## VPS Service Navigation` section in its `CLAUDE.md` so that repo's CC can operate its VPS-side services headlessly (operator does no UI work — CC handles 99% via API / CLI / MCP). Canonical service playbooks: `platform-docs/02-governance/service-playbooks/`. Fill the table below at onboarding:

```markdown
## VPS Service Navigation

| Service | This repo's resource | How CC leverages it | Canonical playbook |
|---|---|---|---|
| **Infisical** (secrets) | Project `[PROJECT_NAME]` id `[INFISICAL_PROJECT_ID]`, envs dev/staging/prod | `mcp__infisical__*` (read) / API with `vps-operator` creds (write) | `service-playbooks/substrate/infisical.md` §9.5 |
| **Coolify** (orchestration) | App `[APP_NAME]` uuid `[COOLIFY_APP_UUID]`, runs on `[vagary-core-1|vagary-compute-1]` | Coolify API; MCP 404 over public → SSH `docker` fallback | `service-playbooks/substrate/coolify.md` §5,§7 |
| **Reverse proxy** | `[Caddy vhost on core-1 | Traefik via Coolify on compute-1]` | Vhost via vps-ansible template / Coolify app config | `service-playbooks/substrate/{caddy,traefik}.md` (canonical) + appendix `05-architecture/part-B-service-appendices/vps-admin/substrate/traefik.md` |
| **DNS + edge** | `[domain]` zone in Cloudflare (CF = DNS authority + edge layer: Workers / R2 / KV / Access / SSL-TLS / Tunnels) | CF API scoped token; CF zone holds product-domain records (Hostinger registrar-only per DNS-authority XOR) | `service-playbooks/substrate/cloudflare.md` |
| **Error store** | GlitchTip/Sentry DSN (in Infisical) | Per-app project; never dual-report | `service-playbooks/observability/glitchtip.md` |
| **Observability** | Loki `{app="[PROJECT_NAME]"}` + Prometheus | `grafana` / Loki MCP | `service-playbooks/observability/*.md` |
| **Mail** | `[n/a | Mailcow domain]` | `platform-docs/docs/runbooks/mail-add-domain.md` | `service-playbooks/specialized/mailcow.md` |
```

`init.sh` leaves this section as the template above; the onboarding session fills the bracketed values per `service-playbooks/substrate/infisical.md` §6 wiring guide.

## Backup Tier

Every new repo declares a backup tier at `init.sh` time. The chosen scaffold lands at the new repo's `.claude/scaffolds/backup/restic.md` so the onboarding session has the full numbered checklist in-repo.

Three tiers (B1–B9 backup-class taxonomy):

| Tier | Description | Backup class | Scaffold |
|---|---|---|---|
| **T1** | SEV1 stateful service (postgres/mongo/mariadb/large volume) — daily restic + offsite fan-out to B2 + CF R2 + GCS | B3 (DB-dump pre-hook) or B7 (volume snapshot) | `.claude/scaffolds/backup/restic-T1.md` |
| **T2** | Coolify-deployed config-only product — weekly via existing substrate-config batch (no product cron) | B6 (config-only) | `.claude/scaffolds/backup/restic-T2.md` |
| **T3** | Mobile / CLI / browser-store / Apps Script — no VPS state; GitHub Releases canonical | B9 (no VPS backup) | `.claude/scaffolds/backup/restic-T3.md` |

**Canonical playbook:** `platform-docs/05-architecture/part-B-service-appendices/vps-admin/substrate/restic.md` (live deployment state + retention + ADR-019 amendments). **Master tier map:** `platform-docs/docs/audits/_archive-2026-05/restic-session-worklog-2026-05-18.md` §W3 3.5.

If unsure which tier applies, default to `skip` at init time and resolve during the first onboarding session against the master tier map.

## Deviations from Universal Laws
- None. (Templates intentionally have placeholder content `[PROJECT_NAME]`, `[STACK]`, `[DESCRIPTION]` — these are not universal-law violations; they're filled in by `init.sh`.)
