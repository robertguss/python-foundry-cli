"""MS-004 / REQ-081: hybrid snapshot regenerate + fail-on-drift."""

from __future__ import annotations

import subprocess
from pathlib import Path
from typing import cast

import pytest

from python_foundry.generate import GenerateError
from python_foundry.hybrid.snapshot import (
    HybridSnapshotError,
    assert_no_drift,
    check_hybrid_snapshot,
    collect_tree,
    compare_trees,
    write_tree,
)

REPO = Path(__file__).resolve().parents[1]
SPEC = REPO / "examples" / "python-foundry-template.toml"
GOLDEN = REPO / "tests" / "goldens" / "hybrid-python-foundry-template"


def test_golden_tree_checked_in() -> None:
    assert SPEC.is_file()
    assert GOLDEN.is_dir()
    files = collect_tree(GOLDEN)
    assert "pyproject.toml" in files
    assert "AGENTS.md" in files
    assert "uv.lock" in files
    assert "src/python_foundry_template/cli.py" in files
    # Forbidden paths must not be in the golden snapshot.
    assert "CLAUDE.md" not in files
    assert ".env" not in files


def test_compare_trees_detects_deliberate_content_drift() -> None:
    expected = collect_tree(GOLDEN)
    actual = dict(expected)
    # Bit-flip a tracked file (drives real compare_trees, not a stub).
    target = "AGENTS.md"
    assert target in actual
    actual[target] = actual[target] + b"\n# deliberate drift\n"
    findings = compare_trees(actual, expected)
    assert findings, "expected non-empty drift findings"
    assert any(target in f for f in findings)
    with pytest.raises(HybridSnapshotError) as excinfo:
        assert_no_drift(findings)
    assert excinfo.value.code == "hybrid.drift"
    assert "drifted" in excinfo.value.message


def test_compare_trees_detects_missing_and_extra_files() -> None:
    expected = collect_tree(GOLDEN)
    actual = dict(expected)
    del actual["AGENTS.md"]
    actual["EXTRA_DRIFT.txt"] = b"nope\n"
    findings = compare_trees(actual, expected)
    assert any("missing" in f and "AGENTS.md" in f for f in findings)
    assert any("unexpected" in f and "EXTRA_DRIFT.txt" in f for f in findings)


def test_regenerated_snapshot_matches_golden(tmp_path: Path) -> None:
    """Real generate path must match checked-in catalog golden tree."""
    findings = check_hybrid_snapshot(
        spec_path=SPEC,
        golden_dir=GOLDEN,
        work_dir=tmp_path,
        run_verify_tools=True,
    )
    assert findings == []


def test_module_cli_exits_nonzero_on_drift(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """``python -m python_foundry.hybrid`` must exit 1 when goldens drift."""
    # Corrupt a temporary golden so regenerate fails the diff (real CLI entry).
    bad_golden = tmp_path / "bad-golden"
    write_tree(bad_golden, collect_tree(GOLDEN))
    agents = bad_golden / "AGENTS.md"
    agents.write_bytes(agents.read_bytes() + b"\n# CI must fail on this\n")

    proc = subprocess.run(
        [
            "uv",
            "run",
            "python",
            "-m",
            "python_foundry.hybrid",
            "--spec",
            str(SPEC),
            "--golden",
            str(bad_golden),
            "--work-dir",
            str(tmp_path / "work"),
        ],
        cwd=REPO,
        capture_output=True,
        text=True,
        check=False,
    )
    assert proc.returncode != 0, proc.stdout + proc.stderr
    assert "drift" in (proc.stderr + proc.stdout).lower()


def test_collect_tree_rejects_missing_root(tmp_path: Path) -> None:
    with pytest.raises(HybridSnapshotError) as excinfo:
        collect_tree(tmp_path / "missing")
    assert excinfo.value.code == "hybrid.missing_root"


def test_write_tree_replaces_existing_root(tmp_path: Path) -> None:
    root = tmp_path / "root"
    root.mkdir()
    (root / "old.txt").write_bytes(b"old")
    write_tree(root, {"new.txt": b"new"})
    assert (root / "new.txt").read_bytes() == b"new"
    assert not (root / "old.txt").exists()


def test_check_hybrid_snapshot_wraps_generate_error(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    def _fake_generate(**kwargs: object) -> None:
        raise GenerateError("boom", error_class="internal", code="generate.internal")

    monkeypatch.setattr("python_foundry.generate.generate", _fake_generate)

    with pytest.raises(HybridSnapshotError) as excinfo:
        check_hybrid_snapshot(
            spec_path=SPEC,
            golden_dir=GOLDEN,
            work_dir=tmp_path / "work",
            run_verify_tools=False,
        )
    assert excinfo.value.code == "hybrid.generate"
    assert "boom" in excinfo.value.message


def test_check_hybrid_snapshot_clears_existing_destination(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    def _fake_generate(**kwargs: object) -> None:
        dest = cast(Path, kwargs["destination"])
        dest.mkdir(parents=True, exist_ok=True)
        (dest / "fresh.txt").write_bytes(b"fresh")

    monkeypatch.setattr("python_foundry.generate.generate", _fake_generate)
    dest = tmp_path / "work" / "python-foundry-template"
    dest.mkdir(parents=True)
    (dest / "stale.txt").write_bytes(b"stale")

    check_hybrid_snapshot(
        spec_path=SPEC,
        golden_dir=GOLDEN,
        work_dir=tmp_path / "work",
        run_verify_tools=False,
    )
    assert (dest / "fresh.txt").read_bytes() == b"fresh"
    assert not (dest / "stale.txt").exists()


def test_module_cli_exits_zero_on_match(tmp_path: Path) -> None:
    proc = subprocess.run(
        [
            "uv",
            "run",
            "python",
            "-m",
            "python_foundry.hybrid",
            "--spec",
            str(SPEC),
            "--golden",
            str(GOLDEN),
            "--work-dir",
            str(tmp_path / "work"),
        ],
        cwd=REPO,
        capture_output=True,
        text=True,
        check=False,
    )
    assert proc.returncode == 0, proc.stderr
    assert "ok" in proc.stdout.lower()
