"""Sibling stage identity + unique naming (REQ-031 / REQ-090 / FND-011)."""

from __future__ import annotations

import os
import secrets
from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path

from python_foundry.fsx.errors import StageError

STAGE_PREFIX = ".foundry-stage-"
MAX_STAGE_CREATE_ATTEMPTS = 16
STAGE_MODE = 0o700


def stage_basename(dest_basename: str, unique: str) -> str:
    """Build stage directory basename: ``.foundry-stage-<dest>-<unique>``."""
    safe = dest_basename.strip() or "project"
    # Avoid path separators in basename components.
    safe = safe.replace("/", "-").replace("\\", "-")
    return f"{STAGE_PREFIX}{safe}-{unique}"


def allocate_unique_token() -> str:
    """Return a short unique token for stage naming (no wall-clock dependency)."""
    return secrets.token_hex(8)


@dataclass(slots=True)
class Stage:
    """Created sibling staging directory (always preserved on failure)."""

    path: Path
    name: str
    parent: Path
    dest_basename: str

    @property
    def absolute_path(self) -> str:
        """Absolute stage_path for error reports (FND-011)."""
        return str(self.path.resolve())

    def write_text(self, relative: str, content: str, *, mode: int = 0o644) -> Path:
        """Write a text file confined under the stage root."""
        from python_foundry.fsx.paths import confine_path

        target = confine_path(self.path, relative)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding="utf-8")
        os.chmod(target, mode)
        return target

    def write_bytes(self, relative: str, content: bytes, *, mode: int = 0o644) -> Path:
        from python_foundry.fsx.paths import confine_path

        target = confine_path(self.path, relative)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(content)
        os.chmod(target, mode)
        return target


def create_stage(
    destination: str | Path,
    *,
    unique_factory: Callable[[], str] | None = None,
    max_attempts: int = MAX_STAGE_CREATE_ATTEMPTS,
) -> Stage:
    """Create a unique sibling stage under the destination parent.

    Naming: ``.foundry-stage-<dest-basename>-<unique>``. On name collision,
    allocates a new unique name; never deletes prior stages (FND-011).
    """
    dest = Path(destination)
    dest_basename = dest.name or "project"
    parent = dest.parent if dest.parent != Path("") else Path(".")
    parent = parent.resolve()
    if not parent.is_dir():
        raise StageError(
            f"destination parent is not a directory: {parent}",
            code="fsx.stage_parent",
        )

    factory = unique_factory or allocate_unique_token
    last_err: OSError | None = None
    for _ in range(max_attempts):
        token = factory()
        name = stage_basename(dest_basename, token)
        stage_path = parent / name
        try:
            stage_path.mkdir(mode=STAGE_MODE)
        except FileExistsError as exc:
            last_err = exc
            continue
        except OSError as exc:
            raise StageError(
                f"cannot create stage {stage_path}: {exc}",
                code="fsx.stage_create",
            ) from exc
        # Ensure mode even when umask interfered.
        os.chmod(stage_path, STAGE_MODE)
        return Stage(
            path=stage_path.resolve(),
            name=name,
            parent=parent,
            dest_basename=dest_basename,
        )

    raise StageError(
        f"exhausted {max_attempts} attempts creating unique stage under {parent}"
        + (f": {last_err}" if last_err else ""),
        code="fsx.stage_exhausted",
    )
