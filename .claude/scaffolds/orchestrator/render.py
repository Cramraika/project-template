#!/usr/bin/env python3
"""Render the orchestrator scaffold into a target tree.

Reads placeholder values from environment + writes the rendered scaffold into
the project root. Invoked by `init.sh` when tier=orchestrator.

Placeholders honored (8):
    ORCHESTRATOR_NAME     e.g. glitchtip-orchestrator
    ORCHESTRATOR_PKG      e.g. glitchtip_orchestrator (underscored)
    VENDOR_NAME           e.g. Glitchtip          (CamelCase / dataclass-safe)
    VENDOR_NAME_UPPER     e.g. GLITCHTIP          (env-var prefix)
    API_BASE_URL          e.g. https://errors.chinmayramraika.in
    INFISICAL_PATH        e.g. /glitchtip-orchestrator
    ENTITY_NAME           e.g. brand
    ENTITY_NAME_PLURAL    e.g. brands
    ENTITY_API_PATH       e.g. projects          (REST list path noun)

Universal rules: §27.5 + §43.6 + §52 — emits log lines on every file written.
"""
from __future__ import annotations

import os
import shutil
import sys
from pathlib import Path

REQUIRED_KEYS = (
    "ORCHESTRATOR_NAME",
    "ORCHESTRATOR_PKG",
    "VENDOR_NAME",
    "VENDOR_NAME_UPPER",
    "API_BASE_URL",
    "INFISICAL_PATH",
    "ENTITY_NAME",
    "ENTITY_NAME_PLURAL",
    "ENTITY_API_PATH",
)


def render(template: str, ctx: dict[str, str]) -> str:
    out = template
    for k, v in ctx.items():
        out = out.replace("{{" + k + "}}", v)
    return out


def _copy_render(src: Path, dst: Path, ctx: dict[str, str]) -> None:
    dst.parent.mkdir(parents=True, exist_ok=True)
    text = src.read_text()
    dst.write_text(render(text, ctx))
    print(f"  rendered: {dst}")


def main() -> int:
    ctx = {}
    missing = []
    for k in REQUIRED_KEYS:
        v = os.environ.get(k)
        if not v:
            missing.append(k)
        else:
            ctx[k] = v
    if missing:
        print(
            "ERROR: missing required env keys: " + ", ".join(missing),
            file=sys.stderr,
        )
        return 1

    scaffold_root = Path(__file__).resolve().parent
    project_root = Path(os.environ.get("PROJECT_ROOT") or os.getcwd()).resolve()
    orch = ctx["ORCHESTRATOR_NAME"]
    pkg = ctx["ORCHESTRATOR_PKG"]

    # Top-level
    _copy_render(scaffold_root / "CLAUDE.md", project_root / "CLAUDE.md.orchestrator", ctx)
    _copy_render(scaffold_root / "Makefile", project_root / "Makefile", ctx)

    pkg_dir = project_root / "scripts" / orch
    _copy_render(scaffold_root / "pyproject.toml", pkg_dir / "pyproject.toml", ctx)
    _copy_render(scaffold_root / "registry.yml", pkg_dir / "registry.yml", ctx)

    mod_dir = pkg_dir / pkg
    _copy_render(scaffold_root / "module" / "__init__.py", mod_dir / "__init__.py", ctx)
    _copy_render(scaffold_root / "module" / "__main__.py", mod_dir / "__main__.py", ctx)
    _copy_render(
        scaffold_root / "module" / "orchestrator.py", mod_dir / "orchestrator.py", ctx
    )

    lib_dir = mod_dir / "lib"
    _copy_render(scaffold_root / "module" / "lib" / "__init__.py", lib_dir / "__init__.py", ctx)
    _copy_render(scaffold_root / "module" / "lib" / "client.py", lib_dir / "client.py", ctx)
    _copy_render(scaffold_root / "module" / "lib" / "registry.py", lib_dir / "registry.py", ctx)
    _copy_render(
        scaffold_root / "module" / "lib" / "state_diff.py", lib_dir / "state_diff.py", ctx
    )

    tests_dir = pkg_dir / "tests"
    _copy_render(scaffold_root / "tests" / "__init__.py", tests_dir / "__init__.py", ctx)
    _copy_render(scaffold_root / "tests" / "test_state_diff.py", tests_dir / "test_state_diff.py", ctx)
    _copy_render(scaffold_root / "tests" / "test_registry.py", tests_dir / "test_registry.py", ctx)
    _copy_render(scaffold_root / "tests" / "test_client.py", tests_dir / "test_client.py", ctx)

    # CI workflow + docs
    _copy_render(
        scaffold_root / "workflows" / "ci.yml",
        project_root / ".github" / "workflows" / "ci.yml",
        ctx,
    )
    _copy_render(
        scaffold_root / "docs" / "runbooks" / "orchestrator-reconcile.md",
        project_root / "docs" / "runbooks" / f"{orch}-reconcile.md",
        ctx,
    )
    _copy_render(
        scaffold_root / "docs" / "specs" / "orchestrator-design.md",
        project_root / "docs" / "specs" / f"{orch}-design.md",
        ctx,
    )

    print(f"\n{orch} scaffold rendered into {project_root}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
