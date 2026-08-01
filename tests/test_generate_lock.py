"""Generate-time uv.lock failure-path tests (python-foundry-cli-o63.8)."""

from __future__ import annotations

from pathlib import Path

import pytest

from python_foundry.fsx import create_stage
from python_foundry.generate.lock import LockError, produce_uv_lock


def test_lock_error_fields() -> None:
    err = LockError("boom", code="lock.test", stage_path="/tmp/stage")
    assert err.error_class == "lock"
    assert err.message == "boom"
    assert err.code == "lock.test"
    assert err.stage_path == "/tmp/stage"


def test_produce_uv_lock_fails_without_pyproject(tmp_path: Path) -> None:
    stage = create_stage(tmp_path / "out")
    with pytest.raises(LockError) as excinfo:
        produce_uv_lock(stage.path)
    assert excinfo.value.code == "lock.missing_pyproject"
    assert "pyproject.toml" in excinfo.value.message
    assert excinfo.value.stage_path == stage.absolute_path


def test_produce_uv_lock_fails_when_uv_lock_exits_nonzero(tmp_path: Path) -> None:
    stage = create_stage(tmp_path / "out")
    pyproject = stage.path / "pyproject.toml"
    pyproject.write_text(
        """
[project]
name = "bad-lock"
version = "0.1.0"
dependencies = ["not-a-real-package-xyz==999.0.0"]

[build-system]
requires = ["setuptools"]
build-backend = "setuptools.build_meta"
""",
        encoding="utf-8",
    )
    with pytest.raises(LockError) as excinfo:
        produce_uv_lock(stage.path)
    assert excinfo.value.code == "lock.uv_failed"
    assert excinfo.value.stage_path == stage.absolute_path
    assert "uv lock failed" in excinfo.value.message


def test_produce_uv_lock_fails_when_artifact_missing(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    stage = create_stage(tmp_path / "out")
    pyproject = stage.path / "pyproject.toml"
    pyproject.write_text(
        """
[project]
name = "no-lock-artifact"
version = "0.1.0"
dependencies = []

[build-system]
requires = ["setuptools"]
build-backend = "setuptools.build_meta"
""",
        encoding="utf-8",
    )
    # Force uv lock to report success without writing uv.lock.
    import subprocess

    def _fake_run(
        argv: list[str], **kwargs: object
    ) -> subprocess.CompletedProcess[str]:
        return subprocess.CompletedProcess(
            args=argv, returncode=0, stdout="", stderr=""
        )

    monkeypatch.setattr(subprocess, "run", _fake_run)
    with pytest.raises(LockError) as excinfo:
        produce_uv_lock(stage.path)
    assert excinfo.value.code == "lock.missing_artifact"
    assert excinfo.value.stage_path == stage.absolute_path


def test_produce_uv_lock_success(tmp_path: Path) -> None:
    stage = create_stage(tmp_path / "out")
    pyproject = stage.path / "pyproject.toml"
    pyproject.write_text(
        """
[project]
name = "ok-lock"
version = "0.1.0"
dependencies = []

[build-system]
requires = ["setuptools"]
build-backend = "setuptools.build_meta"
""",
        encoding="utf-8",
    )
    lock_path = produce_uv_lock(stage.path)
    assert lock_path.is_file()
    assert lock_path.name == "uv.lock"
