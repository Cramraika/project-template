"""{{VENDOR_NAME}} API client — thin REST wrapper.

Universal rules:
- §27.5 closure-claim live-probe — every mutating call returns the live API
  response shape (caller logs evidence).
- §43.6 verify-before-claim — caller MUST inspect return value.
- §43.7 names-not-evidence — slug-to-id resolution is API-driven, not inferred.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Optional

import requests


@dataclass
class {{VENDOR_NAME}}Entity:
    """One {{ENTITY_NAME}} returned by the {{VENDOR_NAME}} API."""

    id: int
    slug: str
    name: str
    raw: Optional[dict[str, Any]] = None


class {{VENDOR_NAME}}Client:
    """REST client for the {{VENDOR_NAME}} API.

    Auth: Bearer API token.
    """

    def __init__(
        self,
        base_url: str,
        api_token: str,
        timeout: float = 10.0,
    ) -> None:
        self.base_url = base_url.rstrip("/")
        self.api_token = api_token
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update(
            {
                "Authorization": f"Bearer {api_token}",
                "Content-Type": "application/json",
                "User-Agent": "{{ORCHESTRATOR_NAME}}/0.1.0 (registry-as-IaC; ADR-068)",
            }
        )

    # ---- read paths -----------------------------------------------------

    def list_entities(self) -> list[{{VENDOR_NAME}}Entity]:
        """GET /api/{{ENTITY_API_PATH}}/  — returns all visible entities."""
        url = f"{self.base_url}/api/{{ENTITY_API_PATH}}/"
        resp = self.session.get(url, timeout=self.timeout)
        resp.raise_for_status()
        return [
            {{VENDOR_NAME}}Entity(
                id=int(item["id"]),
                slug=item["slug"],
                name=item.get("name", item["slug"]),
                raw=item,
            )
            for item in resp.json()
        ]

    # ---- mutating paths -------------------------------------------------

    def create_entity(self, slug: str, name: Optional[str] = None) -> {{VENDOR_NAME}}Entity:
        """POST /api/{{ENTITY_API_PATH}}/  — create a new {{ENTITY_NAME}}.

        Returns:
            The created (or pre-existing) entity row.

        Raises:
            requests.HTTPError on non-2xx other than 409 (already-exists).
        """
        url = f"{self.base_url}/api/{{ENTITY_API_PATH}}/"
        payload: dict[str, Any] = {"slug": slug, "name": name or slug}
        resp = self.session.post(url, json=payload, timeout=self.timeout)
        if resp.status_code == 409:
            # Already exists — fetch and return.
            for entity in self.list_entities():
                if entity.slug == slug:
                    return entity
            raise RuntimeError(
                f"create_entity returned 409 but slug {slug!r} "
                "not in list_entities() result"
            )
        resp.raise_for_status()
        item = resp.json()
        return {{VENDOR_NAME}}Entity(
            id=int(item["id"]),
            slug=item["slug"],
            name=item.get("name", item["slug"]),
            raw=item,
        )
