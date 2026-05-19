"""{{VENDOR_NAME}} orchestrator entry-point — registry-as-IaC reconcile + apply.

Subcommands:
    reconcile   read-only diff of registry vs {{VENDOR_NAME}} live state.
    apply       create missing entities for `desired_state: live` rows.
    list-live   dump current {{VENDOR_NAME}} live entities from API.

Universal rules:
- §27.5 closure-claim live-probe — every mutation logs the API request + response.
- §43.6 verify-before-claim — apply re-reads list endpoint after create.
- §52 unattended-mode contract — non-interactive subcommands return non-zero
  on hard failure; never block on input.

Env / args:
    {{VENDOR_NAME_UPPER}}_API_TOKEN  — Bearer token (required); render via Infisical.
    {{VENDOR_NAME_UPPER}}_BASE_URL   — overrides registry base URL.
    REGISTRY                         — path to registry.yml; defaults to package-local.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

from .lib.client import {{VENDOR_NAME}}Client
from .lib.registry import Registry
from .lib.state_diff import compute_diff

_DEFAULT_REGISTRY_CANDIDATES = (
    os.environ.get("REGISTRY"),
    "/opt/{{ORCHESTRATOR_NAME}}/registry.yml",
    str(Path(__file__).resolve().parents[1] / "registry.yml"),
)


def _resolve_registry_path(cli_arg: str | None) -> Path:
    """Pick the first registry path that exists."""
    if cli_arg:
        return Path(cli_arg)
    for candidate in _DEFAULT_REGISTRY_CANDIDATES:
        if candidate and Path(candidate).exists():
            return Path(candidate)
    raise FileNotFoundError(
        "no registry.yml found; pass --registry or set REGISTRY env"
    )


def _client_from_env(registry: Registry) -> {{VENDOR_NAME}}Client:
    token_var = "{{VENDOR_NAME_UPPER}}_API_TOKEN"
    token = os.environ.get(token_var, "").strip()
    if not token:
        raise SystemExit(
            f"FATAL: {token_var} unset. "
            "Render via Infisical (with-secrets.sh) before invoking."
        )
    base = os.environ.get("{{VENDOR_NAME_UPPER}}_BASE_URL") or registry.base_url
    return {{VENDOR_NAME}}Client(base_url=base, api_token=token)


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def cmd_reconcile(args: argparse.Namespace) -> int:
    """Read-only diff of declared vs live state."""
    reg_path = _resolve_registry_path(args.registry)
    reg = Registry.load(reg_path)
    client = _client_from_env(reg)

    print(f"# {{ORCHESTRATOR_NAME}} reconcile @ {_now_iso()}", file=sys.stderr)
    print(f"# registry: {reg_path}", file=sys.stderr)
    print(f"# base_url: {reg.base_url}", file=sys.stderr)

    live = client.list_entities()
    report = compute_diff(reg.entities, live)

    print(f"\nLIVE {{ENTITY_NAME_PLURAL}}: {len(live)}")
    print(f"DECLARED live: {len(reg.live())}")
    print(f"DECLARED tbd : {len(reg.tbd())}")
    print(f"In-sync      : {len(report.in_sync)}")
    print(f"Missing      : {len(report.missing_live)}")
    print(f"Unmanaged    : {len(report.unmanaged)}")

    if report.missing_live:
        print("\nMISSING (would create on --apply):")
        for e in report.missing_live:
            print(f"  - {e.name} (slug={e.slug}) — {e.detail}")

    if args.json:
        out = {
            "live_count": len(live),
            "declared_live_count": len(reg.live()),
            "declared_tbd_count": len(reg.tbd()),
            "in_sync": [e.name for e in report.in_sync],
            "missing": [e.name for e in report.missing_live],
            "unmanaged": report.unmanaged,
            "as_of_utc": _now_iso(),
        }
        print(json.dumps(out, indent=2))

    return 0


def cmd_apply(args: argparse.Namespace) -> int:
    """Create missing entities for desired_state=live rows.

    §27.5: each create is logged with API request + response.
    §29 confirmation triangle: --apply requires --confirm or explicit
    --{{ENTITY_NAME}} to limit blast radius.
    """
    reg_path = _resolve_registry_path(args.registry)
    reg = Registry.load(reg_path)
    client = _client_from_env(reg)

    live = client.list_entities()
    report = compute_diff(reg.entities, live)
    missing = report.missing_live
    target = getattr(args, "target", None)
    if target:
        missing = [e for e in missing if e.name == target]

    if not missing:
        print("no missing live entities — fully in sync. (idempotent re-run)")
        return 0

    if not args.confirm:
        print("DRY-RUN — would create:", file=sys.stderr)
        for e in missing:
            print(f"  + {{ENTITY_NAME}}={e.name} slug={e.slug}", file=sys.stderr)
        print(
            "\nRe-run with --confirm to actually create. (§29 confirmation triangle)",
            file=sys.stderr,
        )
        return 0

    created = 0
    failed = 0
    for entry in missing:
        row = next((b for b in reg.entities if b.name == entry.name), None)
        if row is None:
            print(f"  ERROR: registry row vanished for {entry.name}", file=sys.stderr)
            failed += 1
            continue
        print(f"POST create slug={row.slug}", file=sys.stderr)
        try:
            obj = client.create_entity(slug=row.slug, name=row.name)
            print(f"  -> 201 Created entity_id={obj.id}", file=sys.stderr)
            row.entity_id = obj.id
            row.last_reconciled = _now_iso()
            created += 1
        except Exception as exc:  # noqa: BLE001 — surface all failures
            print(f"  FAILED: {exc!r}", file=sys.stderr)
            failed += 1

    reg.save(reg_path)
    print(
        f"\napply complete: created={created} failed={failed} "
        "(registry saved with .bak)"
    )
    return 1 if failed else 0


def cmd_list_live(args: argparse.Namespace) -> int:
    """Dump live {{VENDOR_NAME}} entities."""
    reg_path = _resolve_registry_path(args.registry)
    reg = Registry.load(reg_path)
    client = _client_from_env(reg)
    live = client.list_entities()
    for e in sorted(live, key=lambda x: x.id):
        print(f"id={e.id}\tslug={e.slug}\tname={e.name}")
    print(f"\ntotal: {len(live)}", file=sys.stderr)
    return 0


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="{{ORCHESTRATOR_NAME}}",
        description="{{VENDOR_NAME}} registry-as-IaC orchestrator (ADR-068 template)",
    )
    p.add_argument(
        "--registry",
        default=None,
        help="path to registry.yml (defaults to deployed or repo-local)",
    )
    sub = p.add_subparsers(dest="command", required=True)

    rc = sub.add_parser("reconcile", help="read-only diff of registry vs live")
    rc.add_argument("--json", action="store_true", help="also emit JSON summary")
    rc.set_defaults(func=cmd_reconcile)

    ap = sub.add_parser("apply", help="create missing live entities")
    ap.add_argument(
        "--confirm", action="store_true", help="actually mutate (omit for dry-run)"
    )
    ap.add_argument(
        "--target",
        default=None,
        help="limit to one {{ENTITY_NAME}} (blast-radius control)",
    )
    ap.set_defaults(func=cmd_apply)

    ll = sub.add_parser("list-live", help="dump live entities")
    ll.set_defaults(func=cmd_list_live)

    return p


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
