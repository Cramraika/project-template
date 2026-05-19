"""Declared-vs-live state diff for the {{VENDOR_NAME}} orchestrator.

Universal rule §43.6: verify-before-claim — diff is computed against LIVE API
state, never against cached / inferred / name-derived data.
"""
from __future__ import annotations

from dataclasses import dataclass

from .client import {{VENDOR_NAME}}Entity
from .registry import EntityRow


@dataclass
class DiffEntry:
    """One row of the reconcile diff."""

    name: str
    slug: str
    declared_state: str
    live_status: str  # "present" | "missing" | "drift"
    detail: str = ""


@dataclass
class DiffReport:
    """Aggregate diff of registry vs live entities."""

    entries: list[DiffEntry]

    @property
    def missing_live(self) -> list[DiffEntry]:
        """Declared live but not present — `--apply` will create."""
        return [
            e
            for e in self.entries
            if e.declared_state == "live" and e.live_status == "missing"
        ]

    @property
    def declared_tbd(self) -> list[DiffEntry]:
        """Declared TBD; orchestrator does NOT auto-create these."""
        return [e for e in self.entries if e.declared_state == "tbd"]

    @property
    def in_sync(self) -> list[DiffEntry]:
        """Declared live, present in {{VENDOR_NAME}} with matching slug."""
        return [
            e
            for e in self.entries
            if e.declared_state == "live" and e.live_status == "present"
        ]

    @property
    def unmanaged(self) -> list[str]:
        """Slugs of live entities not declared in the registry."""
        return [e.slug for e in self.entries if e.live_status == "drift"]


def compute_diff(
    declared: list[EntityRow], live: list[{{VENDOR_NAME}}Entity]
) -> DiffReport:
    """Compare registry against live {{VENDOR_NAME}} entities."""
    live_by_slug = {p.slug: p for p in live}
    declared_slugs = {b.slug for b in declared}

    entries: list[DiffEntry] = []

    for row in declared:
        if row.desired_state == "tbd":
            entries.append(
                DiffEntry(
                    name=row.name,
                    slug=row.slug,
                    declared_state="tbd",
                    live_status=(
                        "present" if row.slug in live_by_slug else "missing"
                    ),
                    detail="awaiting operator-OOB activation",
                )
            )
            continue
        if row.desired_state != "live":
            continue
        if row.slug in live_by_slug:
            live_e = live_by_slug[row.slug]
            entries.append(
                DiffEntry(
                    name=row.name,
                    slug=row.slug,
                    declared_state="live",
                    live_status="present",
                    detail=f"entity_id={live_e.id}",
                )
            )
        else:
            entries.append(
                DiffEntry(
                    name=row.name,
                    slug=row.slug,
                    declared_state="live",
                    live_status="missing",
                    detail="declared live but not present",
                )
            )

    # Surface live entities not tracked in the registry.
    for live_e in live:
        if live_e.slug not in declared_slugs:
            entries.append(
                DiffEntry(
                    name=live_e.name,
                    slug=live_e.slug,
                    declared_state="unmanaged",
                    live_status="drift",
                    detail=f"live entity_id={live_e.id} not in registry",
                )
            )

    return DiffReport(entries=entries)
