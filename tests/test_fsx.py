"""Filesystem stage + place tests (PHASE-02 beads)."""

from __future__ import annotations

from pathlib import Path
from typing import cast

import pytest

from python_foundry.fsx import (
    STAGE_PREFIX,
    PathEscapeError,
    PlaceError,
    Stage,
    StageError,
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


def test_path_confinement_rejects_symlink_escape(tmp_path: Path) -> None:
    """REQ-032: a symlink inside the stage pointing outside MUST fail."""
    outside = tmp_path / "outside"
    outside.mkdir()
    stage = create_stage(tmp_path / "app")
    escape_link = stage.path / "escape"
    escape_link.symlink_to(outside, target_is_directory=True)
    with pytest.raises(PathEscapeError):
        confine_path(stage.path, "escape/evil.txt")


def test_render_path_with_malicious_spec_value_is_still_confined(
    tmp_path: Path,
) -> None:
    """REQ-032: rendered {{name}}-style paths cannot escape the stage root.

    render_path() itself does not validate; confinement is enforced at write
    time by Stage.write_text/write_bytes (belt-and-suspenders check here).
    """
    stage = create_stage(tmp_path / "app")
    malicious = "../../../etc/passwd"
    with pytest.raises(PathEscapeError):
        stage.write_text(malicious, "pwned")


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


def test_create_stage_fails_when_parent_is_not_directory(tmp_path: Path) -> None:
    parent_file = tmp_path / "not-a-dir"
    parent_file.write_text("i am a file\n", encoding="utf-8")
    with pytest.raises(StageError) as excinfo:
        create_stage(parent_file / "out")
    assert excinfo.value.code == "fsx.stage_parent"


def test_create_stage_exhausts_unique_names(tmp_path: Path) -> None:
    dest = tmp_path / "cell"
    (tmp_path / ".foundry-stage-cell-collision").mkdir()

    def _factory() -> str:
        return "collision"

    with pytest.raises(StageError) as excinfo:
        create_stage(dest, unique_factory=_factory, max_attempts=3)
    assert excinfo.value.code == "fsx.stage_exhausted"
    assert "3 attempts" in excinfo.value.message


def test_exclusive_place_rejects_symlink_destination(tmp_path: Path) -> None:
    target = tmp_path / "target"
    target.mkdir()
    dest = tmp_path / "out-link"
    dest.symlink_to(target)
    stage = create_stage(tmp_path / "real-out")
    stage.write_text("a.txt", "a\n")
    with pytest.raises(PlaceError) as excinfo:
        exclusive_place(stage, dest)
    assert excinfo.value.code == "fsx.dest_nonempty"
    assert dest.is_symlink()
    assert stage.path.is_dir()


def test_exclusive_place_rejects_missing_stage(tmp_path: Path) -> None:
    class _FakeStage:
        path = tmp_path / "missing-stage"

    with pytest.raises(PlaceError) as excinfo:
        exclusive_place(cast(Stage, _FakeStage()), tmp_path / "out")
    assert excinfo.value.code == "fsx.place_stage_missing"
    assert "stage is not a directory" in excinfo.value.message


def test_destination_is_nonempty_detects_symlink(tmp_path: Path) -> None:
    target = tmp_path / "target"
    target.mkdir()
    link = tmp_path / "link"
    link.symlink_to(target)
    assert destination_is_nonempty(link) is True


def test_two_failed_places_preserve_distinct_stages(tmp_path: Path) -> None:
    """Migrated from SPK-101: two consecutive failures leave two stages."""
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


def test_exclusive_place_success_empty_or_missing(tmp_path: Path) -> None:
    dest = tmp_path / "placed"
    stage = create_stage(dest)
    stage.write_text("README.md", "hello\n")
    result = exclusive_place(stage, dest)
    assert result == dest.resolve()
    assert dest.is_dir()
    assert (dest / "README.md").read_text(encoding="utf-8") == "hello\n"
    assert not stage.path.exists()  # renamed away


def test_exclusive_place_cross_device_fallback(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    import errno

    dest = tmp_path / "out"
    stage = create_stage(dest)
    stage.write_text("a.txt", "a\n")

    def _fake_rename(src: str, dst: str) -> None:
        raise OSError(errno.EXDEV, "cross-device")

    monkeypatch.setattr("python_foundry.fsx.place.os.rename", _fake_rename)
    placed = exclusive_place(stage, dest)
    assert placed == dest.resolve()
    assert (dest / "a.txt").read_text(encoding="utf-8") == "a\n"
    assert not stage.path.exists()


def test_exclusive_place_cleans_partial_copy_on_copytree_failure(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    import errno
    import shutil

    dest = tmp_path / "out"
    stage = create_stage(dest)
    stage.write_text("a.txt", "a\n")

    def _fake_rename(src: str, dst: str) -> None:
        raise OSError(errno.EXDEV, "cross-device")

    def _fake_copytree(src: str, dst: str, **kwargs: object) -> None:
        Path(dst).mkdir(parents=True)
        (Path(dst) / "partial.txt").write_bytes(b"x")
        raise OSError("copy failed")

    monkeypatch.setattr("python_foundry.fsx.place.os.rename", _fake_rename)
    monkeypatch.setattr(shutil, "copytree", _fake_copytree)

    with pytest.raises(PlaceError) as excinfo:
        exclusive_place(stage, dest)
    assert excinfo.value.code == "fsx.place_failed"
    assert not dest.exists()  # partial dest removed
    assert stage.path.is_dir()  # stage preserved


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
