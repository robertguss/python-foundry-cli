"""Generate orchestration error-branch tests (python-foundry-cli-o63.5)."""

from __future__ import annotations

from pathlib import Path

import pytest

from python_foundry.generate import GenerateError, generate
from python_foundry.generate.lock import LockError
from python_foundry.generate.orchestrate import _purge_build_artifacts
from python_foundry.render import RenderError
from python_foundry.verify import VerifyError


def _minimal_spec(tmp_path: Path, destination: Path) -> Path:
    spec_path = tmp_path / "cell.toml"
    spec_path.write_text(
        f'''
schema = 1
name = "orch-test"
archetype = "cli"
destination = "{destination}"
profiles = []
verify = "none"
''',
        encoding="utf-8",
    )
    return spec_path


def test_generate_render_error_preserves_stage_and_dest(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    dest = tmp_path / "out"
    spec_path = _minimal_spec(tmp_path, dest)
    stage_path = tmp_path / "stage-marker"

    def _fake_render(*args: object, **kwargs: object) -> None:
        stage_path.touch()
        raise RenderError("render boom", code="render.missing_source")

    monkeypatch.setattr(
        "python_foundry.generate.orchestrate.render_plan_into_stage", _fake_render
    )

    with pytest.raises(GenerateError) as excinfo:
        generate(spec_path=spec_path, destination=dest)
    err = excinfo.value
    assert err.error_class == "render"
    assert err.code == "render.missing_source"
    assert err.stage_path is not None
    assert Path(err.stage_path).is_absolute()
    assert Path(err.stage_path).is_dir()
    assert not dest.exists()


def test_generate_lock_error_preserves_stage_and_dest(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    dest = tmp_path / "out"
    spec_path = _minimal_spec(tmp_path, dest)

    def _fake_lock(*args: object, **kwargs: object) -> None:
        raise LockError("lock boom", code="lock.uv_failed")

    monkeypatch.setattr(
        "python_foundry.generate.orchestrate.produce_uv_lock", _fake_lock
    )

    with pytest.raises(GenerateError) as excinfo:
        generate(spec_path=spec_path, destination=dest)
    err = excinfo.value
    assert err.error_class == "lock"
    assert err.code == "lock.uv_failed"
    assert err.stage_path is not None
    assert Path(err.stage_path).is_dir()
    assert not dest.exists()


def test_generate_verify_error_preserves_stage_and_dest(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    dest = tmp_path / "out"
    spec_path = _minimal_spec(tmp_path, dest)

    def _fake_verify(*args: object, **kwargs: object) -> None:
        raise VerifyError(
            "verify boom",
            code="verify.ruff_check",
            verify_mode="default",
        )

    monkeypatch.setattr("python_foundry.generate.orchestrate.run_verify", _fake_verify)

    with pytest.raises(GenerateError) as excinfo:
        generate(spec_path=spec_path, destination=dest)
    err = excinfo.value
    assert err.error_class == "verify"
    assert err.code == "verify.ruff_check"
    assert err.verify_mode == "default"
    assert err.stage_path is not None
    assert Path(err.stage_path).is_dir()
    assert not dest.exists()


def test_generate_fsx_error_parent_not_directory(tmp_path: Path) -> None:
    parent_file = tmp_path / "not-a-dir"
    parent_file.write_text("i am a file\n", encoding="utf-8")
    dest = parent_file / "out"
    spec_path = _minimal_spec(tmp_path, dest)

    with pytest.raises(GenerateError) as excinfo:
        generate(spec_path=spec_path, destination=dest)
    err = excinfo.value
    assert err.error_class == "place"
    assert err.code == "fsx.stage_parent"
    assert err.stage_path is None
    assert not dest.exists()


def test_generate_internal_error_wraps_unexpected_exception(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    dest = tmp_path / "out"
    spec_path = _minimal_spec(tmp_path, dest)

    def _fake_render(*args: object, **kwargs: object) -> None:
        raise ValueError("unexpected boom")

    monkeypatch.setattr(
        "python_foundry.generate.orchestrate.render_plan_into_stage", _fake_render
    )

    with pytest.raises(GenerateError) as excinfo:
        generate(spec_path=spec_path, destination=dest)
    err = excinfo.value
    assert err.error_class == "internal"
    assert err.code == "generate.internal"
    assert err.stage_path is not None
    assert Path(err.stage_path).is_dir()
    assert not dest.exists()


def test_purge_build_artifacts_preserves_symlinks(tmp_path: Path) -> None:
    stage_root = tmp_path / "stage"
    stage_root.mkdir()
    real_venv = tmp_path / "real-venv"
    real_venv.mkdir()
    venv_link = stage_root / ".venv"
    venv_link.symlink_to(real_venv, target_is_directory=True)

    nested = stage_root / "src" / "pkg"
    nested.mkdir(parents=True)
    (nested / "__pycache__").mkdir()
    (nested / "__pycache__" / "foo.cpython-313.pyc").write_bytes(b"x")

    _purge_build_artifacts(stage_root)

    assert venv_link.is_symlink()
    assert venv_link.resolve() == real_venv
    assert not (nested / "__pycache__").exists()


def test_generate_success_purges_build_artifacts_from_destination(
    tmp_path: Path,
) -> None:
    dest = tmp_path / "out"
    spec_path = tmp_path / "cell.toml"
    spec_path.write_text(
        f'''
schema = 1
name = "purge-test"
archetype = "cli"
destination = "{dest}"
profiles = []
''',
        encoding="utf-8",
    )
    result = generate(spec_path=spec_path, destination=dest)
    assert result.placed
    assert dest.is_dir()
    assert not (dest / ".venv").exists()
    assert not (dest / "__pycache__").exists()
    assert not any(p.suffix == ".egg-info" for p in dest.rglob("*"))
