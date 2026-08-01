"""Filesystem stage + exclusive place (PHASE-02)."""

from __future__ import annotations

from python_foundry.fsx.errors import FsxError, PathEscapeError, PlaceError, StageError
from python_foundry.fsx.paths import confine_path
from python_foundry.fsx.place import (
    assert_destination_placeable,
    destination_is_nonempty,
    exclusive_place,
)
from python_foundry.fsx.stage import (
    STAGE_PREFIX,
    Stage,
    allocate_unique_token,
    create_stage,
    stage_basename,
)

__all__ = [
    "STAGE_PREFIX",
    "FsxError",
    "PathEscapeError",
    "PlaceError",
    "Stage",
    "StageError",
    "allocate_unique_token",
    "assert_destination_placeable",
    "confine_path",
    "create_stage",
    "destination_is_nonempty",
    "exclusive_place",
    "stage_basename",
]
