"""Resolved composition model (pure; no I/O)."""

from __future__ import annotations

from dataclasses import dataclass

from python_foundry.catalog.models import Kind, UnitManifest


@dataclass(frozen=True, slots=True)
class PlannedFile:
    """One output path after composition (owner is kind-qualified)."""

    path: str
    render: str
    source: str
    mode: str
    owner_kind: Kind
    owner_id: str
    override: bool = False

    @property
    def owner_ref(self) -> str:
        return f"{self.owner_kind}/{self.owner_id}"


@dataclass(frozen=True, slots=True)
class ResolvedProject:
    """Immutable resolve result: units in catalog apply order + planned files."""

    archetype: str
    profiles: tuple[str, ...]  # catalog apply order among selected profiles
    units: tuple[UnitManifest, ...]  # core → archetype → profiles (apply order)
    files: tuple[PlannedFile, ...]
    catalog_digest: str
    # Merged unit dependencies (REQ-059/REQ-061), unit apply order, deduped by
    # first occurrence.
    dependencies: tuple[str, ...] = ()
