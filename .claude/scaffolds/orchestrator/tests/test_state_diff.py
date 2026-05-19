"""State-diff unit tests — declared vs live state comparison."""
from __future__ import annotations

from {{ORCHESTRATOR_PKG}}.lib.client import {{VENDOR_NAME}}Entity
from {{ORCHESTRATOR_PKG}}.lib.registry import EntityRow
from {{ORCHESTRATOR_PKG}}.lib.state_diff import compute_diff


def _row(slug: str, state: str = "live", eid: int | None = None) -> EntityRow:
    return EntityRow(name=slug, slug=slug, desired_state=state, entity_id=eid)


def _live(slug: str, eid: int) -> {{VENDOR_NAME}}Entity:
    return {{VENDOR_NAME}}Entity(id=eid, slug=slug, name=slug)


def test_in_sync_when_all_present():
    declared = [_row("a", eid=1), _row("b", eid=2)]
    live = [_live("a", 1), _live("b", 2)]
    report = compute_diff(declared, live)
    assert len(report.in_sync) == 2
    assert len(report.missing_live) == 0
    assert len(report.unmanaged) == 0


def test_missing_when_declared_but_not_live():
    declared = [_row("a"), _row("missing")]
    live = [_live("a", 1)]
    report = compute_diff(declared, live)
    assert {e.name for e in report.missing_live} == {"missing"}
    assert {e.name for e in report.in_sync} == {"a"}


def test_tbd_does_not_trigger_apply_missing():
    declared = [_row("a"), _row("tbd-thing", state="tbd")]
    live = [_live("a", 1)]
    report = compute_diff(declared, live)
    assert all(e.declared_state != "tbd" for e in report.missing_live)
    assert len(report.declared_tbd) == 1
    assert report.declared_tbd[0].live_status == "missing"


def test_tbd_present_in_live_is_noted():
    declared = [_row("tbd-thing", state="tbd")]
    live = [_live("tbd-thing", 99)]
    report = compute_diff(declared, live)
    tbd_entry = report.declared_tbd[0]
    assert tbd_entry.live_status == "present"


def test_unmanaged_drift_surfaces_unknown_live():
    declared = [_row("a")]
    live = [_live("a", 1), _live("orphan", 42)]
    report = compute_diff(declared, live)
    assert "orphan" in report.unmanaged


def test_compute_diff_is_pure():
    declared = [_row("a", eid=1), _row("b", eid=2)]
    live = [_live("a", 1), _live("b", 2)]
    r1 = compute_diff(declared, live)
    r2 = compute_diff(declared, live)
    assert len(r1.entries) == len(r2.entries)
    assert {e.slug for e in r1.entries} == {e.slug for e in r2.entries}
