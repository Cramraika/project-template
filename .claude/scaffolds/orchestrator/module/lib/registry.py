"""Registry-as-IaC loader for the {{VENDOR_NAME}} orchestrator.

Pattern source: ADR-068a site-discoverability template.
- Declarative YAML at `<repo>/registry.yml` is source-of-truth.
- Operator authors `desired_state`, `slug`, etc.
- `entity_id` + `last_reconciled` are orchestrator writeback fields only.

Universal rules:
- §27 append-only artefact discipline (only writeback fields mutate).
- §43.7 names-not-evidence (entity_id populated from live API, never inferred).
"""
from __future__ import annotations

import shutil
from dataclasses import dataclass, field, fields
from pathlib import Path
from typing import Any, Optional

import yaml

SUPPORTED_SCHEMA_VERSIONS = (1,)

# Fields the operator authors; reconciler does NOT overwrite these.
INTENT_FIELDS = (
    "name",
    "slug",
    "desired_state",
)

# Fields the orchestrator writes back after reconcile.
WRITEBACK_FIELDS = (
    "entity_id",
    "last_reconciled",
)


@dataclass
class EntityRow:
    """One {{ENTITY_NAME}} row in the registry."""

    name: str
    slug: str
    desired_state: str  # live | tbd | paused | remove
    # Writeback fields:
    entity_id: Optional[int] = None
    last_reconciled: Optional[str] = None
    # Optional per-row extras (operator-extensible).
    extras: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        out: dict[str, Any] = {}
        for f in fields(self):
            if f.name == "extras":
                continue
            out[f.name] = getattr(self, f.name)
        # Flatten extras so per-row custom keys are preserved.
        for k, v in self.extras.items():
            out[k] = v
        return out


_KNOWN_FIELDS = frozenset(f.name for f in fields(EntityRow) if f.name != "extras")


def _row_from_dict(d: dict[str, Any]) -> EntityRow:
    """Build an EntityRow from a raw YAML row.

    Tolerates unknown future keys (forward-compat).
    """
    known = {k: v for k, v in d.items() if k in _KNOWN_FIELDS}
    extras = {k: v for k, v in d.items() if k not in _KNOWN_FIELDS}
    return EntityRow(extras=extras, **known)


@dataclass
class Registry:
    """Registry as-loaded from disk."""

    schema_version: int
    base_url: str
    entities: list[EntityRow]

    @classmethod
    def load(cls, path: Path | str) -> "Registry":
        path = Path(path)
        if not path.exists():
            raise FileNotFoundError(f"registry not found at {path}")
        raw = yaml.safe_load(path.read_text()) or {}
        version = raw.get("schema_version", 1)
        if version not in SUPPORTED_SCHEMA_VERSIONS:
            raise ValueError(
                f"unsupported schema_version {version!r}; "
                f"supported: {SUPPORTED_SCHEMA_VERSIONS}"
            )
        entities = [_row_from_dict(d) for d in (raw.get("{{ENTITY_NAME_PLURAL}}") or [])]
        return cls(
            schema_version=version,
            base_url=raw.get("base_url", "{{API_BASE_URL}}"),
            entities=entities,
        )

    def save(self, path: Path | str) -> None:
        path = Path(path)
        if path.exists():
            shutil.copy2(path, path.with_suffix(path.suffix + ".bak"))
        payload = {
            "schema_version": self.schema_version,
            "base_url": self.base_url,
            "{{ENTITY_NAME_PLURAL}}": [e.to_dict() for e in self.entities],
        }
        path.write_text(
            yaml.safe_dump(payload, sort_keys=False, default_flow_style=False)
        )

    def live(self) -> list[EntityRow]:
        """Entities the orchestrator should reconcile against live state."""
        return [e for e in self.entities if e.desired_state == "live"]

    def tbd(self) -> list[EntityRow]:
        """Entities awaiting operator-OOB activation."""
        return [e for e in self.entities if e.desired_state == "tbd"]
