"""Client unit tests — HTTP layer mocked.

These tests verify the client's request shape + response parsing without
hitting the real {{VENDOR_NAME}} API.
"""
from __future__ import annotations

from unittest.mock import MagicMock

from {{ORCHESTRATOR_PKG}}.lib.client import {{VENDOR_NAME}}Client, {{VENDOR_NAME}}Entity


def _client(monkeypatch_session: MagicMock) -> {{VENDOR_NAME}}Client:
    c = {{VENDOR_NAME}}Client(base_url="https://api.example.test", api_token="tok")
    c.session = monkeypatch_session
    return c


def test_list_entities_parses_response():
    session = MagicMock()
    resp = MagicMock()
    resp.json.return_value = [
        {"id": 1, "slug": "a", "name": "A"},
        {"id": 2, "slug": "b", "name": "B"},
    ]
    resp.raise_for_status.return_value = None
    session.get.return_value = resp

    c = _client(session)
    entities = c.list_entities()
    assert len(entities) == 2
    assert entities[0].id == 1
    assert entities[0].slug == "a"
    assert entities[1].name == "B"


def test_create_entity_handles_409_by_lookup():
    session = MagicMock()
    create_resp = MagicMock()
    create_resp.status_code = 409
    create_resp.raise_for_status.return_value = None
    list_resp = MagicMock()
    list_resp.json.return_value = [{"id": 7, "slug": "dup", "name": "dup"}]
    list_resp.raise_for_status.return_value = None
    session.post.return_value = create_resp
    session.get.return_value = list_resp

    c = _client(session)
    entity = c.create_entity(slug="dup")
    assert entity.id == 7
    assert entity.slug == "dup"


def test_create_entity_returns_201_payload():
    session = MagicMock()
    resp = MagicMock()
    resp.status_code = 201
    resp.json.return_value = {"id": 42, "slug": "new", "name": "New"}
    resp.raise_for_status.return_value = None
    session.post.return_value = resp

    c = _client(session)
    entity = c.create_entity(slug="new", name="New")
    assert entity.id == 42
    assert isinstance(entity, {{VENDOR_NAME}}Entity)
