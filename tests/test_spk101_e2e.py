"""SPK-101 e2e: stage + exclusive place (PHASE-02 exit)."""

from __future__ import annotations

from pathlib import Path

import pytest

from python_foundry.fsx import (
    PlaceError,
    create_stage,
    exclusive_place,
)


def test_spk101_success_stage_then_place(tmp_path: Path) -> None:
    dest = tmp_path / "generated-app"
    stage = create_stage(dest)
    stage.write_text("README.md", "# demo\n")
    stage.write_text("src/app/__init__.py", '"""app"""\n')
    stage.write_text("pyproject.toml", '[project]\nname="demo"\n')

    assert stage.path.is_dir()
    assert stage.absolute_path.startswith("/")
    assert not dest.exists()

    placed = exclusive_place(stage, dest)
    assert placed == dest.resolve()
    assert (dest / "README.md").read_text(encoding="utf-8") == "# demo\n"
    assert (dest / "src/app/__init__.py").is_file()
    assert not stage.path.exists()


def test_spk101_nonempty_dest_preserves_stage_and_dest(tmp_path: Path) -> None:
    dest = tmp_path / "busy"
    dest.mkdir()
    (dest / "keep.txt").write_text("original\n", encoding="utf-8")

    stage = create_stage(dest)
    stage.write_text("new.txt", "staged\n")
    stage_abs = stage.absolute_path

    with pytest.raises(PlaceError) as excinfo:
        exclusive_place(stage, dest)

    assert excinfo.value.code == "fsx.dest_nonempty"
    # Destination untouched.
    assert (dest / "keep.txt").read_text(encoding="utf-8") == "original\n"
    assert not (dest / "new.txt").exists()
    # Stage preserved with absolute path.
    assert Path(stage_abs).is_dir()
    assert (Path(stage_abs) / "new.txt").read_text(encoding="utf-8") == "staged\n"


def test_spk101_two_failures_two_stages(tmp_path: Path) -> None:
    dest = tmp_path / "proj"
    dest.mkdir()
    (dest / "x").write_text("y", encoding="utf-8")
    s1 = create_stage(dest)
    s2 = create_stage(dest)
    for s in (s1, s2):
        s.write_text("partial.txt", "fail\n")
        with pytest.raises(PlaceError):
            exclusive_place(s, dest)
    assert s1.path.is_dir() and s2.path.is_dir()
    assert s1.name != s2.name
