"""Verify tier runners precedence and real tool failures (python-foundry-cli-o63.3)."""

from __future__ import annotations

from pathlib import Path

import pytest

from python_foundry.generate import generate
from python_foundry.verify import NETWORK_DISCLOSURE, VerifyError, run_verify


def _build_valid_project(tmp_path: Path) -> Path:
    dest = tmp_path / "out"
    spec_path = tmp_path / "cell.toml"
    spec_path.write_text(
        f"""
schema = 1
name = "verify-test"
archetype = "cli"
destination = "{dest}"
profiles = []
""",
        encoding="utf-8",
    )
    generate(spec_path=spec_path, destination=dest, run_verify_tools=False)
    return dest


def test_network_disclosure_mentions_uv() -> None:
    assert "uv" in NETWORK_DISCLOSURE
    assert "network" in NETWORK_DISCLOSURE.lower()


def test_verify_none_skips_with_warning(tmp_path: Path) -> None:
    result = run_verify(tmp_path, "none")
    assert result.skipped is True
    assert result.steps_run == ()
    assert result.warning is not None
    assert "none" in result.warning


def test_default_verify_runs_all_steps(tmp_path: Path) -> None:
    dest = _build_valid_project(tmp_path)
    result = run_verify(dest, "default", skip_network_tools=False)
    assert result.mode == "default"
    assert result.steps_run == (
        "uv_sync_locked",
        "ruff_check",
        "ruff_format_check",
        "ty_check",
    )
    assert not result.skipped
    assert result.warning is None


def test_skip_network_tools_excludes_uv_sync(tmp_path: Path) -> None:
    dest = _build_valid_project(tmp_path)
    result = run_verify(dest, "default", skip_network_tools=True)
    assert "uv_sync_locked" not in result.steps_run
    assert result.steps_run == ("ruff_check", "ruff_format_check", "ty_check")


def test_ruff_check_failure_raises_verify_error(tmp_path: Path) -> None:
    dest = _build_valid_project(tmp_path)
    (dest / "src/verify_test/cli.py").write_text("import os\n", encoding="utf-8")
    with pytest.raises(VerifyError) as excinfo:
        run_verify(dest, "default", skip_network_tools=True)
    err = excinfo.value
    assert err.code == "verify.ruff_check"
    assert err.verify_mode == "default"
    assert err.stage_path == str(dest.resolve())
    assert "ruff_check" in err.message


def test_ty_check_failure_raises_verify_error(tmp_path: Path) -> None:
    dest = _build_valid_project(tmp_path)
    (dest / "src/verify_test/cli.py").write_text('x: int = "hello"\n', encoding="utf-8")
    with pytest.raises(VerifyError) as excinfo:
        run_verify(dest, "default", skip_network_tools=True)
    err = excinfo.value
    assert err.code == "verify.ty_check"
    assert err.verify_mode == "default"
    assert err.stage_path == str(dest.resolve())
    assert "ty_check" in err.message


def test_strict_verify_includes_pytest_step(tmp_path: Path) -> None:
    dest = _build_valid_project(tmp_path)
    (dest / "tests/test_fail.py").write_text(
        'def test_fail():\n    raise AssertionError("deliberate failure")\n',
        encoding="utf-8",
    )
    with pytest.raises(VerifyError) as excinfo:
        run_verify(dest, "strict", skip_network_tools=True)
    err = excinfo.value
    assert err.code == "verify.pytest"
    assert err.verify_mode == "strict"
    assert err.stage_path == str(dest.resolve())
    assert "pytest" in err.message
