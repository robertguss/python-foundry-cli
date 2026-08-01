"""Catalog unit models (kind-qualified identity; FND-007 / REQ-087)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

Kind = Literal["core", "archetype", "profile"]
KINDS = frozenset({"core", "archetype", "profile"})
RenderMode = Literal["static", "template"]


@dataclass(frozen=True, slots=True)
class FileEntry:
    """One inventory entry from a unit manifest (stub bodies OK in PHASE-01)."""

    path: str
    render: RenderMode
    source: str
    mode: str = "0644"
    # Later-applied unit may replace an earlier path only when override is true
    # (REQ-043 / §9.7). Default false → collision hard-fail.
    override: bool = False


@dataclass(frozen=True, slots=True)
class UnitManifest:
    """Validated catalog unit manifest with kind-qualified identity."""

    kind: Kind
    id: str
    description: str
    apply_order: int
    files: tuple[FileEntry, ...]
    manifest_path: str
    # Extra project dependencies this unit contributes (REQ-059/REQ-061), in
    # manifest-declared order. Empty for units that add no dependencies.
    dependencies: tuple[str, ...] = ()

    @property
    def ref(self) -> str:
        """Kind-qualified reference, e.g. ``archetype/data-etl``."""
        return f"{self.kind}/{self.id}"


@dataclass(frozen=True, slots=True)
class UnitSummary:
    """Stable list-row for catalog list (CLI-ready)."""

    kind: Kind
    id: str
    description: str
    manifest_path: str

    @property
    def ref(self) -> str:
        return f"{self.kind}/{self.id}"
