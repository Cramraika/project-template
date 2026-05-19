"""{{VENDOR_NAME}} orchestrator — registry-as-IaC (ADR-068 template).

Reconciles a declared YAML registry against the live {{VENDOR_NAME}} API.

Universal rules honored:
- §27 append-only artefact discipline (writeback fields only).
- §27.5 closure-claim live-probe (apply logs API request + response).
- §43.6 verify-before-claim (reconcile reads live state before declaring drift).
- §43.7 names-not-evidence (entity id resolved via API, never inferred).
- §52 unattended-mode (non-interactive subcommands; non-zero on hard fail).
"""

__version__ = "0.1.0"
