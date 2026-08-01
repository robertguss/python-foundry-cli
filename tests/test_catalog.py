"""Unit tests for closed catalog load, digest, and kind-qualified UX (p0h)."""

from __future__ import annotations

from pathlib import Path

import pytest

from python_foundry.catalog import (
    Catalog,
    CatalogLookupError,
    digest_map,
    load_catalog_tree,
    load_default_catalog,
)

REPO_ROOT = Path(__file__).resolve().parents[1]
AUTHORING_CATALOG = REPO_ROOT / "catalog"
PACKAGE_DATA = REPO_ROOT / "src" / "python_foundry" / "catalog" / "data"


def test_load_default_catalog_via_importlib_resources() -> None:
    cat = load_default_catalog()
    assert isinstance(cat, Catalog)
    assert len(cat.digest) == 64
    assert all(c in "0123456789abcdef" for c in cat.digest)
    assert cat.versions_toml.startswith(b"#") or b"schema" in cat.versions_toml


def test_authoring_tree_matches_package_data() -> None:
    """Repo-root catalog/ and package data produce the same digest."""
    assert AUTHORING_CATALOG.exists()
    assert PACKAGE_DATA.is_dir()

    def _files(root: Path) -> dict[str, bytes]:
        return {
            p.relative_to(root).as_posix(): p.read_bytes()
            for p in root.rglob("*")
            if p.is_file()
        }

    assert digest_map(_files(AUTHORING_CATALOG)) == digest_map(_files(PACKAGE_DATA))


def test_list_returns_kind_and_id_for_dual_data_etl() -> None:
    cat = load_default_catalog()
    rows = cat.list_units()
    refs = {(r.kind, r.id) for r in rows}
    assert ("archetype", "data-etl") in refs
    assert ("profile", "data-etl") in refs
    # Every row carries kind + id (REQ-087).
    for row in rows:
        assert row.kind in {"core", "archetype", "profile"}
        assert row.id
        assert row.ref == f"{row.kind}/{row.id}"


def test_show_distinguishes_archetype_and_profile_data_etl() -> None:
    cat = load_default_catalog()
    arch = cat.show("archetype/data-etl")
    prof = cat.show("profile/data-etl")
    assert arch.kind == "archetype"
    assert arch.id == "data-etl"
    assert prof.kind == "profile"
    assert prof.id == "data-etl"
    assert arch is not prof
    assert arch.description != prof.description
    assert arch.manifest_path != prof.manifest_path
    assert "archetype" in arch.manifest_path
    assert "profiles" in prof.manifest_path


def test_bare_data_etl_is_ambiguous() -> None:
    cat = load_default_catalog()
    with pytest.raises(CatalogLookupError) as excinfo:
        cat.show("data-etl")
    assert excinfo.value.code == "catalog.ambiguous_id"
    assert "archetype/data-etl" in excinfo.value.message
    assert "profile/data-etl" in excinfo.value.message


def test_unknown_unit_fails() -> None:
    cat = load_default_catalog()
    with pytest.raises(CatalogLookupError) as excinfo:
        cat.show("archetype/nope")
    assert excinfo.value.code == "catalog.unknown_unit"
    assert "not found" in excinfo.value.message
    with pytest.raises(CatalogLookupError):
        cat.get("profile", "missing")


def test_digest_stable_for_fixed_tree() -> None:
    a = load_default_catalog()
    b = load_default_catalog()
    c = load_catalog_tree(PACKAGE_DATA)
    assert a.digest == b.digest == c.digest
    # Deterministic independent recompute of same bytes.
    files = {
        p.relative_to(PACKAGE_DATA).as_posix(): p.read_bytes()
        for p in PACKAGE_DATA.rglob("*")
        if p.is_file()
    }
    assert digest_map(files) == a.digest
    assert digest_map(files) == digest_map(files)


def test_cli_and_core_present_with_file_inventory() -> None:
    cat = load_default_catalog()
    core = cat.get("core", "core")
    cli = cat.get("archetype", "cli")
    assert core.files
    assert cli.files
    for entry in cli.files:
        assert entry.path and entry.source
        assert entry.render in {"static", "template"}


def test_unambiguous_bare_id_show() -> None:
    cat = load_default_catalog()
    assert cat.show("cli").kind == "archetype"
    assert cat.show("http").kind == "profile"
