"""Exclusive place: stage → destination; fail if dest non-empty (REQ-030/031)."""

from __future__ import annotations

import os
import shutil
from pathlib import Path

from python_foundry.fsx.errors import PlaceError
from python_foundry.fsx.stage import Stage


def destination_is_nonempty(destination: str | Path) -> bool:
    dest = Path(destination)
    if not dest.exists():
        return False
    if dest.is_file() or dest.is_symlink():
        return True
    if dest.is_dir():
        try:
            next(dest.iterdir())
            return True
        except StopIteration:
            return False
    return True


def assert_destination_placeable(destination: str | Path) -> Path:
    """Fail closed if destination exists and is non-empty (REQ-030)."""
    dest = Path(destination)
    if destination_is_nonempty(dest):
        raise PlaceError(
            f"destination exists and is non-empty: {dest.resolve()}",
            code="fsx.dest_nonempty",
        )
    return dest


def exclusive_place(stage: Stage, destination: str | Path) -> Path:
    """Atomically place stage at destination when possible.

    - Fails if destination exists and is non-empty (REQ-030).
    - Uses ``os.replace`` / rename when dest absent or empty dir removable.
    - On failure: stage is preserved; destination left untouched.
    - Prefer same parent as stage (sibling) for rename place.
    """
    dest = assert_destination_placeable(destination)
    # NOTE: this is a check-then-act sequence. It is acceptable for the current
    # single-user, local CLI with no concurrent writers; if the tool ever runs
    # under concurrent processes, this gap must be revisited.
    dest = dest if dest.is_absolute() else dest.resolve()
    stage_path = stage.path.resolve()

    if not stage_path.is_dir():
        raise PlaceError(
            f"stage is not a directory: {stage_path}",
            code="fsx.place_stage_missing",
            stage_path=str(stage_path),
        )

    # Empty existing directory: remove so rename can succeed.
    if dest.exists() and dest.is_dir() and not destination_is_nonempty(dest):
        dest.rmdir()

    dest.parent.mkdir(parents=True, exist_ok=True)

    try:
        # Same-filesystem rename preferred.
        os.rename(stage_path, dest)
    except OSError:
        # Cross-device fallback: copy tree then remove stage only on success.
        try:
            shutil.copytree(stage_path, dest, symlinks=True)
        except OSError as exc:
            # Leave stage intact; clean partial dest if we created it mid-copy.
            if dest.exists() and dest.is_dir() and dest != stage_path:
                # Only remove if we partially created dest during this call
                # and it wasn't pre-existing non-empty (we already checked empty).
                try:
                    shutil.rmtree(dest)
                except OSError:
                    pass
            raise PlaceError(
                f"cannot place stage at {dest}: {exc}",
                code="fsx.place_failed",
                stage_path=str(stage_path),
            ) from exc
        # Remove stage after successful copytree (success path only).
        shutil.rmtree(stage_path)

    return dest.resolve()
