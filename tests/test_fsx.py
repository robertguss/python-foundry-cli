"""Filesystem stage + place tests (PHASE-02 beads)."""

from __future__ import annotations

from pathlib import Path

import pytest

from python_foundry.fsx import (
    STAGE_PREFIX,
    PathEscapeError,
    PlaceError,
    confine_path,
    create_stage,
    destination_is_nonempty,
    exclusive_place,
)


def test_create_stage_naming_and_absolute_path(tmp_path: Path) -> None:
    dest = tmp_path / "my-app"
    stage = create_stage(dest)
    assert stage.name.startswith(f"{STAGE_PREFIX}my-app-")
    assert stage.path.is_dir()
    assert stage.path.is_absolute()
    assert stage.absolute_path == str(stage.path.resolve())
    assert stage.parent == tmp_path.resolve()
    assert stage.path.parent == tmp_path.resolve()


def test_two_consecutive_stages_are_distinct(tmp_path: Path) -> None:
    """Two consecutive failures leave two distinct stages (6vu AC)."""
    dest = tmp_path / "proj"
    a = create_stage(dest)
    b = create_stage(dest)
    assert a.name != b.name
    assert a.path != b.path
    assert a.path.is_dir()
    assert b.path.is_dir()
    # Prior stages never deleted.
    assert a.path.exists()
    assert b.path.exists()


def test_collision_allocates_new_name(tmp_path: Path) -> None:
    dest = tmp_path / "cell"
    tokens = iter(["fixedtoken", "fixedtoken", "otherone1"])

    def factory() -> str:
        return next(tokens)

    first = create_stage(dest, unique_factory=factory)
    second = create_stage(dest, unique_factory=factory)
    assert first.name != second.name
    assert "fixedtoken" in first.name
    assert "otherone1" in second.name


def test_path_confinement_rejects_escape(tmp_path: Path) -> None:
    stage = create_stage(tmp_path / "app")
    ok = confine_path(stage.path, "src/pkg/main.py")
    assert ok == (stage.path / "src/pkg/main.py").resolve()
    with pytest.raises(PathEscapeError) as excinfo:
        confine_path(stage.path, "../escape.txt")
    assert excinfo.value.error_class == "place"
    assert excinfo.value.stage_path == stage.absolute_path
    with pytest.raises(PathEscapeError):
        confine_path(stage.path, "/etc/passwd")


def test_stage_write_confined(tmp_path: Path) -> None:
    stage = create_stage(tmp_path / "app")
    path = stage.write_text("hello.txt", "hi\n")
    assert path.read_text(encoding="utf-8") == "hi\n"
    with pytest.raises(PathEscapeError):
        stage.write_text("../outside.txt", "nope")


def test_fail_nonempty_destination(tmp_path: Path) -> None:
    dest = tmp_path / "out"
    dest.mkdir()
    (dest / "existing.txt").write_text("keep\n", encoding="utf-8")
    stage = create_stage(dest)
    stage.write_text("new.txt", "staged\n")
    with pytest.raises(PlaceError) as excinfo:
        exclusive_place(stage, dest)
    assert excinfo.value.code == "fsx.dest_nonempty"
    # Destination untouched; stage preserved.
    assert (dest / "existing.txt").read_text(encoding="utf-8") == "keep\n"
    assert not (dest / "new.txt").exists()
    assert stage.path.is_dir()
    assert (stage.path / "hello.txt").exists() is False
    assert (stage.path / "new.txt").read_text(encoding="utf-8") == "staged\n"


def test_exclusive_place_success_empty_or_missing(tmp_path: Path) -> None:
    dest = tmp_path / "placed"
    stage = create_stage(dest)
    stage.write_text("README.md", "hello\n")
    result = exclusive_place(stage, dest)
    assert result == dest.resolve()
    assert dest.is_dir()
    assert (dest / "README.md").read_text(encoding="utf-8") == "hello\n"
    assert not stage.path.exists()  # renamed away


def test_empty_destination_dir_is_placeable(tmp_path: Path) -> None:
    dest = tmp_path / "empty-dest"
    dest.mkdir()
    assert destination_is_nonempty(dest) is False
    stage = create_stage(dest)
    stage.write_text("a.py", "x=1\n")
    exclusive_place(stage, dest)
    assert (dest / "a.py").is_file()


def test_place_failure_reports_absolute_stage_path(tmp_path: Path) -> None:
    dest = tmp_path / "blocked"
    dest.mkdir()
    (dest / "x").write_text("y", encoding="utf-8")
    stage = create_stage(dest)
    with pytest.raises(PlaceError) as excinfo:
        exclusive_place(stage, dest)
    # REQ-090 / el2: absolute stage_path available for failure reports.
    assert stage.absolute_path.startswith("/")
    assert Path(stage.absolute_path).is_dir()
    # PlaceError for nonempty does not require stage_path field, but stage still
    # absolute via Stage API for report layer.
    assert excinfo.value.code == "fsx.dest_nonempty"
