"""Registry loader + writeback unit tests."""
from __future__ import annotations

from pathlib import Path

import pytest
import yaml

from {{ORCHESTRATOR_PKG}}.lib.registry import EntityRow, Registry


def _write_registry(tmp_path: Path, entities: list[dict]) -> Path:
    payload = {
        "schema_version": 1,
        "base_url": "{{API_BASE_URL}}",
        "{{ENTITY_NAME_PLURAL}}": entities,
    }
    p = tmp_path / "registry.yml"
    p.write_text(yaml.safe_dump(payload, sort_keys=False))
    return p


def test_load_minimal_registry(tmp_path):
    p = _write_registry(
        tmp_path,
        [
            {"name": "a", "slug": "a", "desired_state": "live"},
            {"name": "b", "slug": "b", "desired_state": "tbd"},
        ],
    )
    reg = Registry.load(p)
    assert reg.schema_version == 1
    assert reg.base_url == "{{API_BASE_URL}}"
    assert len(reg.entities) == 2
    assert reg.live()[0].name == "a"
    assert reg.tbd()[0].name == "b"


def test_unsupported_schema_version_rejected(tmp_path):
    payload = {
        "schema_version": 99,
        "base_url": "x",
        "{{ENTITY_NAME_PLURAL}}": [],
    }
    p = tmp_path / "registry.yml"
    p.write_text(yaml.safe_dump(payload))
    with pytest.raises(ValueError):
        Registry.load(p)


def test_save_creates_backup_and_persists_writeback(tmp_path):
    p = _write_registry(
        tmp_path,
        [{"name": "a", "slug": "a", "desired_state": "live"}],
    )
    reg = Registry.load(p)
    reg.entities[0].entity_id = 42
    reg.entities[0].last_reconciled = "2026-05-19T00:00:00+00:00"
    reg.save(p)

    bak = p.with_suffix(p.suffix + ".bak")
    assert bak.exists(), "writeback must produce .bak"

    reloaded = Registry.load(p)
    assert reloaded.entities[0].entity_id == 42
    assert reloaded.entities[0].last_reconciled == "2026-05-19T00:00:00+00:00"


def test_unknown_keys_preserved_as_extras(tmp_path):
    p = _write_registry(
        tmp_path,
        [
            {
                "name": "a",
                "slug": "a",
                "desired_state": "live",
                "custom_field": "value-x",
            }
        ],
    )
    reg = Registry.load(p)
    row: EntityRow = reg.entities[0]
    assert row.extras.get("custom_field") == "value-x"


def test_missing_file_raises(tmp_path):
    with pytest.raises(FileNotFoundError):
        Registry.load(tmp_path / "nope.yml")
