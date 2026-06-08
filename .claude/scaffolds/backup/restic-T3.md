# Backup Tier T3 — No VPS Backup (GitHub Releases Canonical)

**Source:** copied by `init.sh` from `project-template/.claude/scaffolds/backup/restic-T3.md`.
**Canonical playbook:** `platform-docs/05-architecture/part-B-service-appendices/vps-admin/substrate/restic.md`.
**Backup-class taxonomy:** B1–B9 — see `docs/audits/_archive-2026-05/restic-session-worklog-2026-05-18.md` §W3 3.4.

---

## What Tier 3 means

**No VPS state to back up.** The product is a mobile app, CLI tool, browser extension shipping via Web Store, OSS script, or Google Apps Script — its canonical source of truth is **GitHub Releases** (or the equivalent store listing). Binaries are **immutable** once published; the build pipeline is reproducible from the tagged source commit.

This scaffold applies to:
- Android apps (`pulseboard`)
- Windows / cross-platform CLI utilities (`pulseboard-desktop`, `bulk`, `tldv_downloader`)
- Browser extension store builds (`bellring-extension` store artifacts — note: the **server** is T2)
- Google Apps Script projects (`google-sheet-sales-manager`)
- OSS scripts with no deployed-runtime (`torn-smart-scripts`)

## Backup class

**B9** — no VPS backup.

There is **no restic involvement** for T3 products. The product does not appear in any `/etc/cron.d/*-restic-backup` file, does not contribute a tag to the restic repository, and does not participate in the offsite fan-out.

## Rationale

- **Source of truth is GitHub Releases.** The release tarball + signed asset + release notes form the canonical artifact set. Anyone (operator or downstream forker) can re-download verbatim.
- **Binaries are immutable.** Once a release is tagged + assets uploaded, GitHub does not allow asset mutation; only release deletion. Treat each release as cryptographically anchored.
- **Build is reproducible.** Tagged source commit + CI pipeline (`.github/workflows/release.yml`) deterministically rebuild the binary from scratch. No state drift between releases.
- **Backing up VPS state would be lying about coverage.** There is no VPS runtime to snapshot. Including a T3 product in the restic tag-cohort would produce zero-byte snapshots and a false sense of redundancy.

## Required for T3 onboarding

1. **GitHub release cadence.** Tag a release for every shipped change. No "rolling main" production; every production-equivalent binary is a tagged + signed release.
2. **SHA256 sums.** Every release asset has its SHA256 published in the release notes and committed to `SHA256SUMS` in the release tarball. CI computes + signs.
3. **Release notes.** Each release notes: what changed, what migrated, any breaking changes, any data-format bumps. Markdown-formatted; auto-generated from conventional-commit history is acceptable as a baseline.
4. **Signed assets (where applicable).** Android APK signed with the upload key stored in Infisical (`vps-ops/production/android-signing/<product>`). Windows binaries signed with Authenticode where the budget supports a code-sign cert. Otherwise SHA256 + GPG signature on `SHA256SUMS` is the floor.
5. **CI workflow for release builds.** `.github/workflows/release.yml` triggers on tag push (`v*.*.*`), runs the build, attaches assets, signs `SHA256SUMS`, publishes the release.
6. **Reproducible-build documentation.** README "Build from source" section lists the exact toolchain versions + steps to rebuild a published release locally. Verified at least once per major version.

## Restore

**Re-download from GitHub Releases:**

1. Identify the target release tag (latest, or specific version per recovery requirement).
2. Download all assets from `https://github.com/<owner>/<repo>/releases/tag/<tag>`.
3. Verify SHA256 sums match `SHA256SUMS` in the tarball.
4. Verify GPG signature on `SHA256SUMS` against the publisher's published GPG key.
5. Install / deploy per the product's published install instructions.

For OSS forkers: same path — public GitHub Releases are the redistribution channel. There is no Vagary-Labs-side recovery dependency.

## What T3 explicitly does NOT have

- No `/etc/cron.d/*-restic-backup` file.
- No restic tag.
- No participation in the offsite fan-out.
- No `BackupAgeStale` alert (the product has no backup to age).
- No quarterly Variant C drill. (The release pipeline itself is the drill — every release tag exercises the rebuild path.)
- No T1/T2 onboarding steps.

## Onboarding checklist (numbered)

1. **Confirm tier.** Cross-check master tier map (restic-session-worklog §W3 3.5). T3 is the default for non-VPS-deployed products.
2. **Verify GitHub Releases CI workflow exists** and produces signed assets with SHA256 sums. If not, author it before claiming T3 coverage.
3. **Verify reproducible-build doc** in README is current for the latest release tag.
4. **Verify signing keys are in Infisical** (Android keystore, GPG keys for SHA256SUMS signing).
5. **Update CLAUDE.md** `## Backup Tier` section with: T3, B9 class, "no VPS backup — GitHub Releases canonical", link to latest release.

## Cross-references

- Canonical playbook: `platform-docs/05-architecture/part-B-service-appendices/vps-admin/substrate/restic.md`
- Worklog: `platform-docs/docs/audits/_archive-2026-05/restic-session-worklog-2026-05-18.md` §W3 + §W10
- Sponsor-readiness / OSS rules: `~/.claude/conventions/playbooks/commercial-bound.md`
