"""Load the closed catalog from package data (importlib.resources)."""

from __future__ import annotations

import tomllib
from collections.abc import Iterator
from dataclasses import dataclass, field
from importlib import resources
from importlib.resources.abc import Traversable
from pathlib import Path
from typing import Any, cast

from python_foundry.catalog.digest import digest_map
from python_foundry.catalog.errors import CatalogLoadError, CatalogLookupError
from python_foundry.catalog.models import (
    KINDS,
    FileEntry,
    Kind,
    UnitManifest,
    UnitSummary,
)

# Package-data root (authoring tree also exposed at repo-root catalog/ symlink).
_DATA_PACKAGE = "python_foundry.catalog"
_DATA_DIR = "data"

# Expected closed-set layout for v1 (REQ-040 partial; stub inventories OK).
_EXPECTED_MANIFESTS: tuple[tuple[Kind, str, str], ...] = (
    ("core", "core", "core/manifest.toml"),
    ("archetype", "cli", "archetypes/cli/manifest.toml"),
    ("archetype", "scripts", "archetypes/scripts/manifest.toml"),
    ("archetype", "data-etl", "archetypes/data-etl/manifest.toml"),
    ("profile", "http", "profiles/http/manifest.toml"),
    ("profile", "hooks-hk", "profiles/hooks-hk/manifest.toml"),
    ("profile", "data-etl", "profiles/data-etl/manifest.toml"),
)


@dataclass(frozen=True, slots=True)
class Catalog:
    """Immutable closed catalog snapshot with digest and kind-qualified lookup."""

    digest: str
    units: tuple[UnitManifest, ...]
    versions_toml: bytes
    _by_ref: dict[str, UnitManifest] = field(init=False, repr=False, compare=False)
    _by_kind_id: dict[tuple[Kind, str], UnitManifest] = field(
        init=False, repr=False, compare=False
    )

    def __post_init__(self) -> None:
        by_ref = {u.ref: u for u in self.units}
        by_kind_id = {(u.kind, u.id): u for u in self.units}
        object.__setattr__(self, "_by_ref", by_ref)
        object.__setattr__(self, "_by_kind_id", by_kind_id)

    def list_units(self) -> list[UnitSummary]:
        """Return every unit as kind+id summaries (stable sort: kind, then id)."""
        rows = [
            UnitSummary(
                kind=u.kind,
                id=u.id,
                description=u.description,
                manifest_path=u.manifest_path,
            )
            for u in self.units
        ]
        rows.sort(key=lambda r: (r.kind, r.id))
        return rows

    def show(self, ref: str) -> UnitManifest:
        """Show a unit by kind-qualified ref (``archetype/data-etl``) or bare id.

        Bare ids are allowed only when unambiguous (exactly one unit with that id).
        Dual-id ``data-etl`` requires kind qualification.
        """
        ref = ref.strip()
        if not ref:
            raise CatalogLookupError(
                "catalog unit ref is empty",
                code="catalog.empty_ref",
            )

        if "/" in ref:
            unit = self._by_ref.get(ref)
            if unit is None:
                raise self._unknown(ref)
            return unit

        matches = [u for u in self.units if u.id == ref]
        if len(matches) == 1:
            return matches[0]
        if len(matches) > 1:
            kinds = ", ".join(sorted(f"{m.kind}/{m.id}" for m in matches))
            raise CatalogLookupError(
                f"catalog unit id {ref!r} is ambiguous; use kind-qualified ref "
                f"among: {kinds}",
                code="catalog.ambiguous_id",
            )
        raise self._unknown(ref)

    def get(self, kind: Kind, unit_id: str) -> UnitManifest:
        """Lookup by kind + id (fail closed on unknown)."""
        unit = self._by_kind_id.get((kind, unit_id))
        if unit is None:
            raise self._unknown(f"{kind}/{unit_id}")
        return unit

    def has(self, kind: Kind, unit_id: str) -> bool:
        return (kind, unit_id) in self._by_kind_id

    def _unknown(self, requested: str) -> CatalogLookupError:
        available = sorted(u.ref for u in self.units)
        avail_text = "[" + ", ".join(available) + "]" if available else "[]"
        return CatalogLookupError(
            f"catalog unit {requested!r} not found; available units: {avail_text}",
            code="catalog.unknown_unit",
        )


def load_default_catalog() -> Catalog:
    """Load the closed catalog shipped as package data."""
    root = resources.files(_DATA_PACKAGE).joinpath(_DATA_DIR)
    if not root.is_dir():
        raise CatalogLoadError(
            f"embedded catalog data missing at {_DATA_PACKAGE}/{_DATA_DIR}",
            code="catalog.missing_data",
        )
    return load_catalog_tree(root)


def load_catalog_tree(root: Traversable | str | Path) -> Catalog:
    """Load catalog from a Traversable or filesystem path (author override)."""
    if isinstance(root, str | Path):
        files = dict(_iter_path_files(Path(root)))
    else:
        files = dict(_iter_regular_files(root))
    if "versions.toml" not in files:
        raise CatalogLoadError(
            "catalog tree missing versions.toml",
            code="catalog.missing_versions",
        )

    units = tuple(_load_all_manifests(files))
    if not any(u.kind == "core" and u.id == "core" for u in units):
        raise CatalogLoadError(
            "catalog missing required core/core unit",
            code="catalog.missing_core",
        )
    if not any(u.kind == "archetype" and u.id == "cli" for u in units):
        raise CatalogLoadError(
            "catalog missing required archetype/cli unit",
            code="catalog.missing_cli",
        )

    return Catalog(
        digest=digest_map(files),
        units=units,
        versions_toml=files["versions.toml"],
    )


def _load_all_manifests(files: dict[str, bytes]) -> Iterator[UnitManifest]:
    for kind, unit_id, rel in _EXPECTED_MANIFESTS:
        if rel not in files:
            raise CatalogLoadError(
                f"catalog missing manifest {rel}",
                code="catalog.missing_manifest",
            )
        yield _parse_manifest(files[rel], kind=kind, unit_id=unit_id, path=rel)


def _parse_manifest(
    data: bytes,
    *,
    kind: Kind,
    unit_id: str,
    path: str,
) -> UnitManifest:
    try:
        raw = tomllib.loads(data.decode("utf-8"))
    except (UnicodeDecodeError, tomllib.TOMLDecodeError) as exc:
        raise CatalogLoadError(
            f"invalid manifest TOML at {path}: {exc}",
            code="catalog.manifest_toml",
        ) from exc

    if not isinstance(raw, dict):
        raise CatalogLoadError(
            f"manifest {path} root must be a table",
            code="catalog.manifest_root",
        )

    mid = raw.get("id")
    mkind = raw.get("kind")
    if mid != unit_id:
        raise CatalogLoadError(
            f"manifest {path} id {mid!r} does not match expected {unit_id!r}",
            code="catalog.manifest_id",
        )
    if mkind != kind:
        raise CatalogLoadError(
            f"manifest {path} kind {mkind!r} does not match expected {kind!r}",
            code="catalog.manifest_kind",
        )
    if mkind not in KINDS:
        raise CatalogLoadError(
            f"manifest {path} has invalid kind {mkind!r}",
            code="catalog.manifest_kind",
        )

    description = raw.get("description", "")
    if not isinstance(description, str):
        raise CatalogLoadError(
            f"manifest {path} description must be a string",
            code="catalog.manifest_description",
        )

    apply_order = raw.get("apply_order", 0)
    if not isinstance(apply_order, int) or isinstance(apply_order, bool):
        raise CatalogLoadError(
            f"manifest {path} apply_order must be an integer",
            code="catalog.manifest_order",
        )

    files_raw = raw.get("files", [])
    if not isinstance(files_raw, list):
        raise CatalogLoadError(
            f"manifest {path} files must be an array",
            code="catalog.manifest_files",
        )
    entries = [
        _parse_file_entry(item, path=path, index=index)
        for index, item in enumerate(files_raw)
    ]

    return UnitManifest(
        kind=cast(Kind, mkind),
        id=unit_id,
        description=description,
        apply_order=apply_order,
        files=tuple(entries),
        manifest_path=path,
    )


def _parse_file_entry(item: Any, *, path: str, index: int) -> FileEntry:
    if not isinstance(item, dict):
        raise CatalogLoadError(
            f"manifest {path} files[{index}] must be a table",
            code="catalog.file_entry",
        )
    for key in ("path", "render", "source"):
        if key not in item or not isinstance(item[key], str) or not item[key]:
            raise CatalogLoadError(
                f"manifest {path} files[{index}] missing non-empty {key!r}",
                code="catalog.file_entry",
            )
    render = item["render"]
    if render not in ("static", "template"):
        raise CatalogLoadError(
            f"manifest {path} files[{index}] render must be static|template",
            code="catalog.file_render",
        )
    mode = item.get("mode", "0644")
    if not isinstance(mode, str):
        raise CatalogLoadError(
            f"manifest {path} files[{index}] mode must be a string",
            code="catalog.file_mode",
        )
    override = item.get("override", False)
    if not isinstance(override, bool):
        raise CatalogLoadError(
            f"manifest {path} files[{index}] override must be a bool",
            code="catalog.file_override",
        )
    return FileEntry(
        path=item["path"],
        render=render,
        source=item["source"],
        mode=mode,
        override=override,
    )


def _iter_regular_files(
    root: Traversable,
    *,
    prefix: str = "",
) -> Iterator[tuple[str, bytes]]:
    try:
        children = sorted(root.iterdir(), key=lambda c: c.name)
    except (OSError, FileNotFoundError, NotADirectoryError) as exc:
        raise CatalogLoadError(
            f"cannot list catalog tree at {prefix or '.'}: {exc}",
            code="catalog.list",
        ) from exc

    for child in children:
        name = child.name
        if name.startswith("."):
            continue
        rel = f"{prefix}/{name}" if prefix else name
        if child.is_dir():
            yield from _iter_regular_files(child, prefix=rel)
        elif child.is_file():
            try:
                yield rel, child.read_bytes()
            except OSError as exc:
                raise CatalogLoadError(
                    f"cannot read catalog file {rel}: {exc}",
                    code="catalog.read",
                ) from exc


def _iter_path_files(root: Path, *, prefix: str = "") -> Iterator[tuple[str, bytes]]:
    """Filesystem walk for author/dev override paths."""
    try:
        children = sorted(root.iterdir(), key=lambda p: p.name)
    except OSError as exc:
        raise CatalogLoadError(
            f"cannot list catalog tree at {prefix or root}: {exc}",
            code="catalog.list",
        ) from exc

    for child in children:
        name = child.name
        if name.startswith("."):
            continue
        rel = f"{prefix}/{name}" if prefix else name
        if child.is_dir():
            yield from _iter_path_files(child, prefix=rel)
        elif child.is_file():
            try:
                yield rel, child.read_bytes()
            except OSError as exc:
                raise CatalogLoadError(
                    f"cannot read catalog file {rel}: {exc}",
                    code="catalog.read",
                ) from exc
