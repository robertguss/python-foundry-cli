"""Path confinement under a stage root (REQ-032)."""

from __future__ import annotations

from pathlib import Path

from python_foundry.fsx.errors import PathEscapeError


def confine_path(stage_root: Path, relative: str) -> Path:
    """Resolve *relative* under *stage_root* and reject escapes.

    Rejects absolute paths, empty segments that leave the root, ``..``
    escapes, and symlink-resolved targets outside the stage root.
    """
    root = stage_root.resolve()
    if not relative or relative.startswith("/") or relative.startswith("\\"):
        raise PathEscapeError(
            f"path {relative!r} must be relative and non-empty under stage",
            code="fsx.path_escape",
            stage_path=str(root),
        )
    # Lexical reject for .. components before filesystem resolve.
    parts = Path(relative).parts
    if any(p == ".." for p in parts):
        raise PathEscapeError(
            f"path {relative!r} contains parent-directory segments",
            code="fsx.path_escape",
            stage_path=str(root),
        )
    if Path(relative).is_absolute():
        raise PathEscapeError(
            f"path {relative!r} is absolute",
            code="fsx.path_escape",
            stage_path=str(root),
        )

    candidate = (root / relative).resolve()
    try:
        candidate.relative_to(root)
    except ValueError as exc:
        raise PathEscapeError(
            f"path {relative!r} escapes stage root {root}",
            code="fsx.path_escape",
            stage_path=str(root),
        ) from exc
    return candidate
