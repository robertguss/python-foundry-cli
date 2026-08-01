"""Generation Plan model (immutable contract; §9.3)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True, slots=True)
class GenerationPlan:
    """Immutable Generation Plan with sealed plan_sha256."""

    body: dict[str, Any]  # full plan including plan_sha256
    plan_sha256: str
    preimage: bytes  # canonical JSON bytes used for the hash (no plan_sha256)

    @property
    def catalog_digest(self) -> str:
        return str(self.body["catalog_digest"])

    @property
    def foundry_version(self) -> str:
        return str(self.body["foundry"]["version"])

    @property
    def verify_mode(self) -> str:
        return str(self.body["verify_mode"])

    @property
    def verify_source(self) -> str:
        return str(self.body["verify_source"])
