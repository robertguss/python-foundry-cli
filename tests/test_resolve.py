"""Unit tests for resolve composition (python-foundry-cli-a5m)."""

from __future__ import annotations

import pytest

from python_foundry.catalog import load_default_catalog
from python_foundry.resolve import ResolveError, resolve
from python_foundry.spec import ProjectSpec, parse_spec_text


def _spec(*, archetype: str = "cli", profiles: list[str] | None = None) -> ProjectSpec:
    profiles = profiles if profiles is not None else []
    prof_toml = "[" + ", ".join(f'"{p}"' for p in profiles) + "]"
    text = f"""
schema = 1
name = "demo"
archetype = "{archetype}"
destination = "./demo"
profiles = {prof_toml}
"""
    return parse_spec_text(text)


def test_exactly_one_archetype_cli() -> None:
    cat = load_default_catalog()
    resolved = resolve(_spec(archetype="cli"), cat)
    assert resolved.archetype == "cli"
    kinds = [u.kind for u in resolved.units]
    assert kinds[0] == "core"
    assert kinds[1] == "archetype"
    assert resolved.units[1].id == "cli"


def test_unknown_archetype_fails() -> None:
    # Bypass spec closed-set by constructing ProjectSpec with an invalid archetype.
    from typing import cast

    from python_foundry.spec.models import Archetype

    raw = ProjectSpec(
        schema=1,
        name="demo",
        archetype=cast(Archetype, "web"),
        destination="./demo",
        profiles=(),
    )
    cat = load_default_catalog()
    with pytest.raises(ResolveError) as excinfo:
        resolve(raw, cat)
    assert excinfo.value.error_class == "resolve"
    assert "unknown archetype" in excinfo.value.message


def test_unknown_profile_fails() -> None:
    raw = ProjectSpec(
        schema=1,
        name="demo",
        archetype="cli",
        destination="./demo",
        profiles=("nope",),
    )
    with pytest.raises(ResolveError) as excinfo:
        resolve(raw, load_default_catalog())
    assert excinfo.value.code == "resolve.unknown_profile"


def test_duplicate_profiles_fail() -> None:
    raw = ProjectSpec(
        schema=1,
        name="demo",
        archetype="cli",
        destination="./demo",
        profiles=("http", "http"),
    )
    with pytest.raises(ResolveError) as excinfo:
        resolve(raw, load_default_catalog())
    assert excinfo.value.code == "resolve.duplicate_profile"
    assert excinfo.value.error_class == "resolve"


def test_profile_order_independent_same_membership() -> None:
    """Reordered TOML profiles → identical resolved profile apply order (FND-002)."""
    cat = load_default_catalog()
    a = resolve(_spec(profiles=["data-etl", "http", "hooks-hk"]), cat)
    b = resolve(_spec(profiles=["hooks-hk", "data-etl", "http"]), cat)
    c = resolve(_spec(profiles=["http", "hooks-hk", "data-etl"]), cat)
    assert a.profiles == b.profiles == c.profiles
    # Catalog apply_order: http=20, hooks-hk=30, data-etl=40
    assert a.profiles == ("http", "hooks-hk", "data-etl")
    assert [u.ref for u in a.units] == [u.ref for u in b.units]
    assert a.files == b.files == c.files


def test_empty_profiles_core_and_archetype_only() -> None:
    resolved = resolve(_spec(profiles=[]), load_default_catalog())
    assert resolved.profiles == ()
    assert len(resolved.units) == 2
    assert resolved.files
    assert resolved.catalog_digest


def test_hooks_hk_replace_rule_drops_core_precommit() -> None:
    """hooks-hk replaces Core default pre-commit paths (rule present on stubs)."""
    from python_foundry.catalog.models import FileEntry, UnitManifest
    from python_foundry.resolve.compose import HOOKS_HK_REPLACES, _compose_files

    core = UnitManifest(
        kind="core",
        id="core",
        description="core",
        apply_order=0,
        files=(
            FileEntry(
                path=".pre-commit-config.yaml",
                render="static",
                source="files/pre-commit.static",
            ),
            FileEntry(
                path="AGENTS.md",
                render="template",
                source="files/AGENTS.md.tmpl",
            ),
        ),
        manifest_path="core/manifest.toml",
    )
    hooks = UnitManifest(
        kind="profile",
        id="hooks-hk",
        description="hooks",
        apply_order=30,
        files=(
            FileEntry(
                path="hk.pkl",
                render="static",
                source="files/hk.pkl.static",
            ),
        ),
        manifest_path="profiles/hooks-hk/manifest.toml",
    )
    files = _compose_files((core, hooks), selected_profile_ids={"hooks-hk"})
    paths = {f.path for f in files}
    assert ".pre-commit-config.yaml" not in paths
    assert "AGENTS.md" in paths
    assert "hk.pkl" in paths
    assert HOOKS_HK_REPLACES  # rule constant is non-empty


def test_path_collision_without_override_fails() -> None:
    from python_foundry.catalog.models import FileEntry, UnitManifest
    from python_foundry.resolve.compose import _compose_files

    a = UnitManifest(
        kind="core",
        id="core",
        description="",
        apply_order=0,
        files=(FileEntry(path="x.py", render="static", source="a"),),
        manifest_path="core/manifest.toml",
    )
    b = UnitManifest(
        kind="archetype",
        id="cli",
        description="",
        apply_order=10,
        files=(FileEntry(path="x.py", render="static", source="b", override=False),),
        manifest_path="archetypes/cli/manifest.toml",
    )
    with pytest.raises(ResolveError) as excinfo:
        _compose_files((a, b), selected_profile_ids=set())
    assert excinfo.value.code == "resolve.path_collision"


def test_path_collision_with_override_wins() -> None:
    from python_foundry.catalog.models import FileEntry, UnitManifest
    from python_foundry.resolve.compose import _compose_files

    a = UnitManifest(
        kind="core",
        id="core",
        description="",
        apply_order=0,
        files=(FileEntry(path="x.py", render="static", source="a"),),
        manifest_path="core/manifest.toml",
    )
    b = UnitManifest(
        kind="archetype",
        id="cli",
        description="",
        apply_order=10,
        files=(FileEntry(path="x.py", render="template", source="b", override=True),),
        manifest_path="archetypes/cli/manifest.toml",
    )
    files = _compose_files((a, b), selected_profile_ids=set())
    assert len(files) == 1
    assert files[0].source == "b"
    assert files[0].owner_ref == "archetype/cli"
