"""Compose archetype + profile set into apply-ordered units and planned files."""

from __future__ import annotations

from python_foundry.catalog.load import Catalog
from python_foundry.catalog.models import UnitManifest
from python_foundry.resolve.errors import ResolveError
from python_foundry.resolve.models import PlannedFile, ResolvedProject
from python_foundry.spec.models import ARCHETYPES, ProjectSpec

# Paths that hooks-hk replaces rather than dual-shipping with Core defaults
# (REQ-043). Present as a rule even when Core stubs omit the files today.
HOOKS_HK_REPLACES = frozenset(
    {
        ".pre-commit-config.yaml",
        ".pre-commit-hooks.yaml",
    }
)


def resolve(spec: ProjectSpec, catalog: Catalog) -> ResolvedProject:
    """Resolve Project Spec against the closed catalog (pure; no I/O).

    - Exactly one archetype from the closed set (REQ-042).
    - profiles is a set: duplicates fail; TOML order ignored (FND-002 / REQ-043).
    - Apply order = catalog total order restricted to selected set:
      core → archetype → profiles (by apply_order, then kind, then id).
    - Path collisions fail unless the later entry sets override=true.
    - hooks-hk drops Core default pre-commit paths it replaces.
    """
    if spec.archetype not in ARCHETYPES:
        raise ResolveError(
            f"unknown archetype {spec.archetype!r}; "
            f"must be one of: {', '.join(sorted(ARCHETYPES))}",
            code="resolve.unknown_archetype",
        )
    if not catalog.has("archetype", spec.archetype):
        raise ResolveError(
            f"archetype {spec.archetype!r} not present in catalog",
            code="resolve.unknown_archetype",
        )

    selected_profiles = _selected_profiles(spec.profiles, catalog)

    core = catalog.get("core", "core")
    archetype = catalog.get("archetype", spec.archetype)
    profile_units = [catalog.get("profile", pid) for pid in selected_profiles]

    # Apply order among selected profiles = catalog apply_order (not TOML order).
    profile_units.sort(key=lambda u: (u.apply_order, u.id))
    ordered_profiles = tuple(u.id for u in profile_units)

    units: tuple[UnitManifest, ...] = (core, archetype, *profile_units)
    files = _compose_files(units, selected_profile_ids=set(ordered_profiles))

    return ResolvedProject(
        archetype=spec.archetype,
        profiles=ordered_profiles,
        units=units,
        files=files,
        catalog_digest=catalog.digest,
    )


def _selected_profiles(
    requested: tuple[str, ...],
    catalog: Catalog,
) -> list[str]:
    seen: dict[str, int] = {}
    for index, profile_id in enumerate(requested):
        if profile_id in seen:
            raise ResolveError(
                f"profiles lists duplicate ID {profile_id!r} "
                f"at indexes {seen[profile_id]} and {index}",
                code="resolve.duplicate_profile",
            )
        seen[profile_id] = index
        if not catalog.has("profile", profile_id):
            available = sorted(
                u.id for u in catalog.units if u.kind == "profile"
            )
            raise ResolveError(
                f"unknown profile {profile_id!r}; available: {available}",
                code="resolve.unknown_profile",
            )
    return list(seen)


def _compose_files(
    units: tuple[UnitManifest, ...],
    *,
    selected_profile_ids: set[str],
) -> tuple[PlannedFile, ...]:
    """Walk units in apply order; enforce override rules; apply hooks-hk replace."""
    hooks_hk = "hooks-hk" in selected_profile_ids
    planned: dict[str, PlannedFile] = {}

    for unit in units:
        for entry in unit.files:
            path = entry.path
            # hooks-hk replaces Core default pre-commit emit (REQ-043).
            if (
                hooks_hk
                and unit.kind == "core"
                and path in HOOKS_HK_REPLACES
            ):
                continue

            new = PlannedFile(
                path=path,
                render=entry.render,
                source=entry.source,
                mode=entry.mode,
                owner_kind=unit.kind,
                owner_id=unit.id,
                override=entry.override,
            )
            if path in planned:
                if not entry.override:
                    prev = planned[path]
                    raise ResolveError(
                        f"path collision on {path!r}: owned by "
                        f"{prev.owner_ref} and {new.owner_ref} "
                        f"(later entry lacks override=true)",
                        code="resolve.path_collision",
                    )
            planned[path] = new

    # Stable path order for deterministic plan bodies.
    return tuple(planned[p] for p in sorted(planned))
