"""Generate-time uv.lock produce/refresh (FND-003 / REQ-052)."""

from __future__ import annotations

import subprocess
from pathlib import Path


class LockError(Exception):
    error_class: str = "lock"

    def __init__(
        self,
        message: str,
        *,
        code: str = "lock.failed",
        stage_path: str | None = None,
    ) -> None:
        super().__init__(message)
        self.message = message
        self.code = code
        self.stage_path = stage_path


def produce_uv_lock(stage_root: Path) -> Path:
    """Run ``uv lock`` in stage so ``uv.lock`` matches metadata before verify."""
    root = stage_root.resolve()
    pyproject = root / "pyproject.toml"
    if not pyproject.is_file():
        raise LockError(
            f"cannot produce uv.lock: missing pyproject.toml in {root}",
            code="lock.missing_pyproject",
            stage_path=str(root),
        )
    proc = subprocess.run(
        ["uv", "lock"],
        cwd=root,
        capture_output=True,
        text=True,
        check=False,
    )
    if proc.returncode != 0:
        detail = (proc.stderr or proc.stdout or "").strip()
        raise LockError(
            f"uv lock failed in stage: {detail[:500]}",
            code="lock.uv_failed",
            stage_path=str(root),
        )
    lock_path = root / "uv.lock"
    if not lock_path.is_file():
        raise LockError(
            "uv lock completed but uv.lock is missing",
            code="lock.missing_artifact",
            stage_path=str(root),
        )
    return lock_path
