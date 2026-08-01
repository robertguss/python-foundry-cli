"""Direct and subprocess tests for python_foundry.hybrid.__main__."""

from __future__ import annotations

import subprocess
from pathlib import Path

import pytest

from python_foundry.hybrid.__main__ import main

REPO = Path(__file__).resolve().parents[1]
SPEC = REPO / "examples" / "python-foundry-template.toml"
GOLDEN = REPO / "tests" / "goldens" / "hybrid-python-foundry-template"


def test_main_help_exits_zero() -> None:
    with pytest.raises(SystemExit) as excinfo:
        main(["--help"])
    assert excinfo.value.code == 0


def test_main_default_paths_match_golden(tmp_path: Path) -> None:
    assert main(["--work-dir", str(tmp_path / "work")]) == 0


def test_main_without_work_dir_uses_temp_and_cleans_up() -> None:
    result = main(["--skip-verify"])
    assert result == 0


def test_main_skip_verify_matches_golden(tmp_path: Path) -> None:
    assert (
        main(
            [
                "--spec",
                str(SPEC),
                "--golden",
                str(GOLDEN),
                "--work-dir",
                str(tmp_path / "work"),
                "--skip-verify",
            ]
        )
        == 0
    )


def test_main_missing_spec_exits_nonzero(tmp_path: Path) -> None:
    missing = tmp_path / "missing.toml"
    assert (
        main(
            [
                "--spec",
                str(missing),
                "--golden",
                str(GOLDEN),
                "--work-dir",
                str(tmp_path / "work"),
            ]
        )
        == 1
    )


def test_main_missing_golden_exits_nonzero(tmp_path: Path) -> None:
    missing = tmp_path / "missing-golden"
    assert (
        main(
            [
                "--spec",
                str(SPEC),
                "--golden",
                str(missing),
                "--work-dir",
                str(tmp_path / "work"),
            ]
        )
        == 1
    )


def test_module_invocation_help() -> None:
    proc = subprocess.run(
        ["uv", "run", "python", "-m", "python_foundry.hybrid", "--help"],
        cwd=REPO,
        capture_output=True,
        text=True,
        check=False,
    )
    assert proc.returncode == 0
    assert "--spec" in proc.stdout
    assert "--golden" in proc.stdout
