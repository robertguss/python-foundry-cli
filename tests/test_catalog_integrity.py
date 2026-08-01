"""Catalog integrity / error-path tests (python-foundry-cli-o63.4)."""

from __future__ import annotations

from importlib.resources.abc import Traversable
from pathlib import Path
from typing import Any, cast

import pytest

import python_foundry.catalog.load as _load_mod
from python_foundry.catalog import (
    CatalogLoadError,
    CatalogLookupError,
    load_catalog_tree,
    load_default_catalog,
)
from python_foundry.catalog.load import _iter_path_files, _iter_regular_files


def _toml_scalar(value: object) -> str:
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, (int, float)):
        return str(value)
    if isinstance(value, str):
        return f'"{value}"'
    raise TypeError(f"unsupported TOML scalar: {type(value)}")


def _make_manifest(
    *,
    kind: str = "core",
    unit_id: str = "core",
    description: object = "unit",
    apply_order: object = 0,
    files: Any | None = None,
    dependencies: list[str] | str | None = None,
) -> str:
    lines = [
        "schema = 1",
        f'id = "{unit_id}"',
        f'kind = "{kind}"',
        f"description = {_toml_scalar(description)}",
        f"apply_order = {_toml_scalar(apply_order)}",
    ]

    if dependencies is not None:
        if isinstance(dependencies, str):
            lines.append(f'dependencies = "{dependencies}"')
        elif len(dependencies) == 0:
            lines.append("dependencies = []")
        else:
            inner = ", ".join(f'"{d}"' for d in dependencies)
            lines.append(f"dependencies = [{inner}]")

    if files is None:
        files = [{"path": "x.txt", "render": "static", "source": "x.static"}]
    if isinstance(files, str):
        lines.append(f'files = "{files}"')
    elif files and not isinstance(files[0], dict):
        inner = ", ".join(_toml_scalar(v) for v in files)
        lines.append(f"files = [{inner}]")
    else:
        for entry in files:
            lines.append("[[files]]")
            for key, value in entry.items():
                lines.append(f"{key} = {_toml_scalar(value)}")
    return "\n".join(lines) + "\n"


def _build_good_catalog(tmp_path: Path) -> Path:
    root = tmp_path / "catalog"
    for kind, unit_id, rel in _load_mod._EXPECTED_MANIFESTS:
        path = root / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(_make_manifest(kind=kind, unit_id=unit_id), encoding="utf-8")
    (root / "versions.toml").write_text("schema = 1\n", encoding="utf-8")
    return root


@pytest.mark.parametrize(
    ("target_rel", "contents", "expected_code"),
    [
        ("versions.toml", None, "catalog.missing_versions"),
        ("core/manifest.toml", "not toml {{{", "catalog.manifest_toml"),
        (
            "core/manifest.toml",
            _make_manifest(unit_id="not-core"),
            "catalog.manifest_id",
        ),
        (
            "core/manifest.toml",
            _make_manifest(kind="not-core"),
            "catalog.manifest_kind",
        ),
        (
            "core/manifest.toml",
            _make_manifest(description=1),
            "catalog.manifest_description",
        ),
        (
            "core/manifest.toml",
            _make_manifest(apply_order="one"),
            "catalog.manifest_order",
        ),
        (
            "core/manifest.toml",
            _make_manifest(files="nope"),
            "catalog.manifest_files",
        ),
        (
            "core/manifest.toml",
            _make_manifest(dependencies="nope"),
            "catalog.manifest_dependencies",
        ),
        (
            "core/manifest.toml",
            _make_manifest(dependencies=[""]),
            "catalog.manifest_dependencies",
        ),
        (
            "core/manifest.toml",
            _make_manifest(files=[1]),  # type: ignore[arg-type]
            "catalog.file_entry",
        ),
        (
            "core/manifest.toml",
            _make_manifest(files=[{}]),
            "catalog.file_entry",
        ),
        (
            "core/manifest.toml",
            _make_manifest(files=[{"path": "", "render": "static", "source": "x"}]),
            "catalog.file_entry",
        ),
        (
            "core/manifest.toml",
            _make_manifest(files=[{"path": "x", "render": "dynamic", "source": "x"}]),
            "catalog.file_render",
        ),
        (
            "core/manifest.toml",
            _make_manifest(
                files=[{"path": "x", "render": "static", "source": "x", "mode": 123}]
            ),
            "catalog.file_mode",
        ),
        (
            "core/manifest.toml",
            _make_manifest(
                files=[
                    {"path": "x", "render": "static", "source": "x", "override": "yes"}
                ]
            ),
            "catalog.file_override",
        ),
    ],
)
def test_catalog_load_integrity_errors(
    tmp_path: Path,
    target_rel: str,
    contents: str | None,
    expected_code: str,
) -> None:
    root = _build_good_catalog(tmp_path)
    target = root / target_rel
    if contents is None:
        target.unlink()
    else:
        target.write_text(contents, encoding="utf-8")
    with pytest.raises(CatalogLoadError) as excinfo:
        load_catalog_tree(root)
    assert excinfo.value.code == expected_code
    assert excinfo.value.error_class == "internal"


def test_expected_manifest_file_missing(tmp_path: Path) -> None:
    root = _build_good_catalog(tmp_path)
    (root / "core/manifest.toml").unlink()
    with pytest.raises(CatalogLoadError) as excinfo:
        load_catalog_tree(root)
    assert excinfo.value.code == "catalog.missing_manifest"


def test_missing_core_unit_defensive_check(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    root = _build_good_catalog(tmp_path)
    patched = tuple(
        entry
        for entry in _load_mod._EXPECTED_MANIFESTS
        if entry[:2] != ("core", "core")
    )
    monkeypatch.setattr(_load_mod, "_EXPECTED_MANIFESTS", patched)
    with pytest.raises(CatalogLoadError) as excinfo:
        load_catalog_tree(root)
    assert excinfo.value.code == "catalog.missing_core"


def test_missing_cli_archetype_defensive_check(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    root = _build_good_catalog(tmp_path)
    patched = tuple(
        entry
        for entry in _load_mod._EXPECTED_MANIFESTS
        if entry[:2] != ("archetype", "cli")
    )
    monkeypatch.setattr(_load_mod, "_EXPECTED_MANIFESTS", patched)
    with pytest.raises(CatalogLoadError) as excinfo:
        load_catalog_tree(root)
    assert excinfo.value.code == "catalog.missing_cli"


def test_manifest_root_not_table(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    root = _build_good_catalog(tmp_path)
    monkeypatch.setattr(_load_mod.tomllib, "loads", lambda _data, **kwargs: [1, 2])
    with pytest.raises(CatalogLoadError) as excinfo:
        load_catalog_tree(root)
    assert excinfo.value.code == "catalog.manifest_root"


@pytest.mark.parametrize("ref", ["", "   "])
def test_catalog_show_empty_ref(ref: str) -> None:
    cat = load_default_catalog()
    with pytest.raises(CatalogLookupError) as excinfo:
        cat.show(ref)
    assert excinfo.value.code == "catalog.empty_ref"


def test_iter_path_files_list_oserror(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    def _bad_iterdir() -> None:
        raise PermissionError("denied")

    monkeypatch.setattr(Path, "iterdir", lambda self: _bad_iterdir())
    with pytest.raises(CatalogLoadError) as excinfo:
        list(_iter_path_files(tmp_path))
    assert excinfo.value.code == "catalog.list"


def test_iter_path_files_read_oserror(tmp_path: Path) -> None:
    (tmp_path / "versions.toml").write_text("schema = 1\n", encoding="utf-8")
    (tmp_path / "core").mkdir()
    (tmp_path / "core" / "manifest.toml").write_bytes(b"schema = 1\n")
    (tmp_path / "core" / "secret.toml").write_bytes(b"x\n")
    secret = tmp_path / "core" / "secret.toml"
    secret.chmod(0o000)
    try:
        with pytest.raises(CatalogLoadError) as excinfo:
            list(_iter_path_files(tmp_path))
        assert excinfo.value.code == "catalog.read"
    finally:
        secret.chmod(0o644)


def test_iter_regular_files_list_oserror(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    class _BadRoot:
        name = "data"

        def iterdir(self) -> None:
            raise PermissionError("denied")

    with pytest.raises(CatalogLoadError) as excinfo:
        list(_iter_regular_files(cast(Traversable, _BadRoot())))
    assert excinfo.value.code == "catalog.list"


class _UnreadableFile:
    name = "broken.toml"

    def is_dir(self) -> bool:
        return False

    def is_file(self) -> bool:
        return True

    def read_bytes(self) -> bytes:
        raise PermissionError("denied")


def test_iter_regular_files_read_oserror() -> None:
    class _RootWithBadFile:
        name = "data"

        def iterdir(self) -> list[_UnreadableFile]:
            return [_UnreadableFile()]

    with pytest.raises(CatalogLoadError) as excinfo:
        list(_iter_regular_files(cast(Traversable, _RootWithBadFile())))
    assert excinfo.value.code == "catalog.read"


def test_load_default_catalog_missing_package_data(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(
        "python_foundry.catalog.load.resources.files",
        lambda pkg: Path("/no/such/package/data"),
    )
    with pytest.raises(CatalogLoadError) as excinfo:
        load_default_catalog()
    assert excinfo.value.code == "catalog.missing_data"
