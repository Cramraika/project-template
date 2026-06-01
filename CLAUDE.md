# project-template

GitHub Template repo for spinning up new projects with the convention-aligned scaffolding (CLAUDE.md tier files + init.sh + .githooks/pre-push + .gitignore baseline).

---

## Claude Preamble
<!-- VERSION: 2026-06-01-v48.1 -->
<!-- SYNC-SOURCE: ~/.claude/conventions/universal-claudemd.md -->

**Universal laws** (§4), **MCP routing** (§6), **Drift protocol** (§11), **Dynamic maintenance** (§14), **Capability resolution** (§15), **Subagent SKILL POLICY** (§16), **Session continuity** (§17), **Decision queue** (§17.a), **Attestation** (§18), **Cite format** (§19), **Three-way disagreement** (§20), **Pre-conditions** (§21), **Provenance markers** (§22), **Redaction rules** (§23), **Token budget** (§24), **Tool-failure fallback** (§25), **Prompt-injection rule** (§26), **Append-only discipline** (§27), **Closure-claim live-probe** (§27.5 — new in v47), **Design-doc self-consistency closing-pass** (§27.6 — new in v47), **Post-closure substrate-shift re-probe** (§27.7 — new in v47.3), **Workspace-resource canonical-declaration** (§27.8 — new in v48), **BLOCKED_BY markers** (§28), **Stop-loss ladder** (§29), **Business-invariant checks** (§30), **Plugin rent rubric** (§31), **Context ceilings** (§32), **Doc reference graph** (§33), **Anti-hallucination** (§34), **Past+Present+Future body** (§35), **Project trackers** (§36), **Doc ownership** (§37), **Archive-on-delete** (§38), **Sponsor + white-label** (§39 — moved to `playbooks/commercial-bound.md`), **Doc-vs-code drift** (§40), **Brand architecture** (§41), **Design system integration** (§42 — moved to `playbooks/tier-a-design.md`), **Session cognition** (§43), **Plugin dispatch** (§44), **Cross-repo clusters** (§45), **Tool-cascade workflow** (§46), **Multi-role agent matrix** (§47), **Parsimony / smallest-tool-first** (§48), **Audit triage discipline** (§49), **Source-of-truth matrix** (§50 — universal rows only; cluster-specific rows moved to playbooks), **Composite cascade catalog** (§51 — §51.2/51.4/51.6 moved to playbooks), **Session launch context + unattended-mode contract** (§52), **Recurrence detection + root-cause escalation** (§53). Sub-sections new in v44: **§4.5 cascade-commit exception**, **§17.b stale-P0 escalation**, **§32.5 canonical-doc size ceiling**, **§38.5 HANDOFF lifecycle enforcement**. Sub-sections new in v47: **§27.5 closure-claim live-probe discipline** (R8 root-cause fix; landed 2026-05-18) + **§27.6 design-doc self-consistency closing-pass discipline** (R3 root-cause fix; landed 2026-05-18 v47.1). Sub-section new in v47.2: **§53.5 count-instrument pre-population on recurrence detection** (lychee fleet-wide agent closure proposal; landed 2026-05-19). Sub-section new in v47.3: **§27.7 post-closure substrate-shift re-probe discipline** (R8 N=4 path-(b); landed 2026-05-19). Sub-section new in v48: **§27.8 workspace-resource canonical-declaration discipline** (R-SCRD path-(a) procedural fix; broader scope per operator decision 2026-05-19; landed 2026-05-19T22:50Z).

**Cluster playbooks** (per-repo `@-import` based on cluster membership): `~/.claude/conventions/playbooks/vps-infra.md` (DNS XOR for VPS-infra repos), `~/.claude/conventions/playbooks/deployed-service.md` (Sentry/Glitchtip XOR + production-incident triage + time-window correlation for repos with prod telemetry), `~/.claude/conventions/playbooks/tier-a-design.md` (Figma/Stitch + design system for Tier A/B), `~/.claude/conventions/playbooks/multi-lang.md` (cross-language refactor cascade for multi-language repos), `~/.claude/conventions/playbooks/commercial-bound.md` (sponsor-readiness + license-aware code-graph routing), `~/.claude/conventions/playbooks/brand-registry.md` (Vagary brand architecture for Vagary-family repos), `~/.claude/conventions/playbooks/bellring-cluster.md` (Bellring server↔extension; v1-stub), `~/.claude/conventions/playbooks/pulseboard-cluster.md` (Pulseboard Android↔Windows; v1-stub), `~/.claude/conventions/playbooks/vagary-cluster.md` (Vagary product cross-repo; v1-stub). **`tech-debt-audit.md`** is Read-on-demand (NOT @-imported) per ENTRY #169 §49 audit-triage discipline — invoked when user requests audit / tech-debt / dead-code work.

**Sources**: **`~/.claude/conventions/universal-claudemd.summary.md`** (≤43-line salient view — read FIRST; load the full canonical only where the summary points) → `~/.claude/conventions/universal-claudemd.md` (full laws, MCP routing, lifecycle, rent rubric, doc-graph, anti-hallucination, brand architecture) + `~/.claude/conventions/project-hygiene.md` (doc placement, cleanup, archive-on-delete, ownership matrix) + cluster playbooks under `~/.claude/conventions/playbooks/` (loaded per-repo via `@-import` in `## Active Cluster Playbooks` section; see list above). Read relevant sections before significant work. Sync: `~/.claude/scripts/sync-preambles.py` (manual cadence; run after any source edit).

## Active Cluster Playbooks (per v40 cluster-split — content auto-inlined)
<!-- BEGIN PLAYBOOKS BLOCK (managed by sync-preambles.py — content inlined; source at ~/.claude/conventions/playbooks/) -->

Source @-imports (declarative pointer; content inlined below since Claude Code does not recursively expand `@-imports` in per-repo CLAUDE.md):
- `@~/.claude/conventions/playbooks/commercial-bound.md`

### Playbook: commercial-bound.md (verbatim from `~/.claude/conventions/playbooks/commercial-bound.md`)

# Commercial-bound + Sponsor-readiness Playbook

**VERSION: 2026-05-06-v1**
Loaded only in repos that are sponsor-ready public OSS, or commercial-bound (sold, embedded in paid product, or redistributed under permissive license). Per-repo `CLAUDE.md` `@-imports` this file when applicable.

Source: extracted verbatim from `~/.claude/conventions/universal-claudemd.md` v39 §39 + §50.2 during v40 cluster-split refactor. No content changes — only relocation so non-commercial / non-sponsor repos don't carry these rules.

**Applies to repos**: `aakhara`, `bellring-server`, `bellring-extension`, `bulk`, `pulseboard` (Android), `pulseboard-desktop`, `tldv_downloader`, `portfolio`, `project-template`, `vagary-platform` (sponsor-ready, has public-vertical surfaces), `host_page` (sponsor-ready landing template).

---

## 1. Sponsor-readiness + white-label pivot (originally §39)

### Sponsor-ready checklist for public repos
- `.github/FUNDING.yml` pointing to `github.com/sponsors/<user>`
- README "Sponsor" section near the top (badge + 1-paragraph ask)
- `LICENSE` (MIT for utilities, AGPL for commercial pressure, other for proprietary)
- At least one GitHub Release (binary attached if applicable, e.g. APK)
- CI green badge

### White-label pivot pattern
When an internal tool goes OSS (e.g. NetworkMonitorCN → **Pulseboard** rebrand 2026-04-19) OR an OSS utility forks into SaaS (e.g. **Bellring** — formerly codenamed Salvo — from sales-notification):

1. **Fork or publish** — new repo with clean name, no internal branding in code
2. **Strip tenant-specific** — remove hardcoded emails/domains/org IDs; parameterize via env/config
3. **Document "Fork + rebrand"** — README section listing the edits a downstream forker makes
4. **Record sibling spec** — `~/.claude/specs/YYYY-MM-DD-<name>-whitelabel.md` if a SaaS pivot
5. **Update inventory** — add to `repo-inventory.md` with sponsor-ready / white-label flags

### Current inventory (2026-04-19)
- **Sponsor-ready public**: tldv_downloader, bulk (renamed from `bulk_api_trigger` 2026-04-19), **pulseboard** (renamed from `NetworkMonitorCN` 2026-04-19), portfolio, project-template, vagary-platform (renamed from `index-of-news` 2026-04-19; flagship vertical retains Index of News brand)
- **White-label pivot applied**: **Bellring** (formerly codenamed Salvo) — repos `bellring-server` + `bellring-extension` (renamed from `sales-notification-backend` / `sales-notification-extension` 2026-04-19). Spec: `~/.claude/specs/2026-04-19-sales-notification-whitelabel.md`.
- **Recently renamed (2026-04-19 Phase 3)**: `sales-notification-backend` → `bellring-server`, `sales-notification-extension` → `bellring-extension`, `NetworkMonitorCN` → `pulseboard`, `training-bot` → `aakhara`.
- **Recently renamed (2026-04-19 Phases 1-2)**: `AI_voice_builder` → `vagary-voice`, `chat-bot` → `anjaan-app`, `bulk_api_trigger` → `bulk`, `index-of-news` → `vagary-platform`. `webhook_trigger` archived (superseded by `bulk`). See `~/.claude/conventions/project-hygiene.md` § Rename Propagation Protocol.
- **Brand umbrella**: Vagary Labs (tech/R&D division of Vagary Life Pvt Ltd; see §41) holds the platform + products + OSS utilities.

## 2. License-aware tool routing (originally §50.2)

Repos categorized as **commercial-bound** (will be sold, embedded in paid product, or redistributed under permissive license):
- `bellring-server`, `bellring-extension` (Bellring SaaS — paid tiers)
- `aakhara` (paid sales-training product)
- `pulseboard`, `pulseboard-desktop` (Public OSS; permissive license required for derivatives)

When working in commercial-bound repos:
- `gitnexus` MCP MAY be used for **read-only investigation** (cypher queries, impact analysis in conversation)
- `gitnexus wiki`, `gitnexus group sync` derivatives, indexed JSON exports MUST NOT be committed/shipped (PolyForm-NC contamination)
- `codegraphcontext` MCP is the canonical graph-derivative source for these repos

When working in **personal/private repos** (vagary-platform, vagary-voice, vagary-earnings, ASM, anjaan-app, internal Cramraika): GitNexus permitted freely.

Per-repo CLAUDE.md should declare classification: `## License classification: commercial-bound` or `## License classification: personal/private`.

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
| **Reverse proxy** | `[Caddy vhost on core-1 | Traefik via Coolify on compute-1]` | Vhost via vps-ansible template / Coolify app config | `service-playbooks/substrate/{caddy,traefik}.md` |
| **DNS** | `[domain]` zone in Cloudflare | CF API scoped token | `service-playbooks/substrate/cloudflare.md` |
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

**Canonical playbook:** `platform-docs/05-architecture/part-B-service-appendices/vps-admin/substrate/restic.md` (live deployment state + retention + ADR-019 amendments). **Master tier map:** `platform-docs/docs/audits/restic-session-worklog-2026-05-18.md` §W3 3.5.

If unsure which tier applies, default to `skip` at init time and resolve during the first onboarding session against the master tier map.

## Deviations from Universal Laws
- None. (Templates intentionally have placeholder content `[PROJECT_NAME]`, `[STACK]`, `[DESCRIPTION]` — these are not universal-law violations; they're filled in by `init.sh`.)
