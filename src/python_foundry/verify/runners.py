"""Verify tier runners executed in stage (PHASE-03)."""

from __future__ import annotations

import subprocess
from dataclasses import dataclass
from pathlib import Path

from python_foundry.spec.models import VerifyMode


class VerifyError(Exception):
    error_class: str = "verify"

    def __init__(
        self,
        message: str,
        *,
        code: str = "verify.failed",
        stage_path: str | None = None,
        verify_mode: str | None = None,
    ) -> None:
        super().__init__(message)
        self.message = message
        self.code = code
        self.stage_path = stage_path
        self.verify_mode = verify_mode


@dataclass(frozen=True, slots=True)
class VerifyResult:
    mode: VerifyMode
    steps_run: tuple[str, ...]
    skipped: bool = False
    warning: str | None = None


# Network disclosure for default/strict (lock + uv sync).
NETWORK_DISCLOSURE = (
    "default/strict verify requires network for `uv lock` / `uv sync --locked` "
    "unless the environment is fully offline with a warm cache."
)


def run_verify(
    stage_root: Path,
    mode: VerifyMode,
    *,
    skip_network_tools: bool = False,
) -> VerifyResult:
    """Run verify tier steps in *stage_root*.

    - default: uv sync --locked + ruff check + ruff format --check + ty check
    - strict: default + pytest
    - none: opt-out with loud warning; no tool proof
    """
    root = stage_root.resolve()
    if mode == "none":
        return VerifyResult(
            mode=mode,
            steps_run=(),
            skipped=True,
            warning=(
                "verify mode is none: no tooling proof; "
                "run quality gates after place (agent DoD)."
            ),
        )

    steps: list[tuple[str, list[str]]] = [
        ("uv_sync_locked", ["uv", "sync", "--locked"]),
        ("ruff_check", ["uv", "run", "ruff", "check", "."]),
        ("ruff_format_check", ["uv", "run", "ruff", "format", "--check", "."]),
        ("ty_check", ["uv", "run", "ty", "check"]),
    ]
    if mode == "strict":
        steps.append(("pytest", ["uv", "run", "pytest"]))

    if skip_network_tools:
        # Offline path: still run pure local tools if lock exists.
        steps = [s for s in steps if s[0] not in {"uv_sync_locked"}]

    ran: list[str] = []
    for name, argv in steps:
        proc = subprocess.run(
            argv,
            cwd=root,
            capture_output=True,
            text=True,
            check=False,
        )
        ran.append(name)
        if proc.returncode != 0:
            detail = (proc.stderr or proc.stdout or "").strip()
            raise VerifyError(
                f"verify step {name!r} failed (exit {proc.returncode}): {detail[:500]}",
                code=f"verify.{name}",
                stage_path=str(root),
                verify_mode=mode,
            )
    return VerifyResult(mode=mode, steps_run=tuple(ran))
