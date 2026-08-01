"""Validate a decoded Project Spec table (pure; no I/O)."""

from __future__ import annotations

from typing import Any, cast

from python_foundry.spec.errors import SpecValidationError
from python_foundry.spec.models import (
    ALLOWED_KEYS,
    ARCHETYPES,
    DEFAULT_PYTHON_VERSION,
    PROFILES,
    REQUIRED_KEYS,
    SUPPORTED_PYTHON_VERSIONS,
    SUPPORTED_SCHEMA,
    VERIFY_MODES,
    Archetype,
    ProjectSpec,
    VerifyMode,
)
from python_foundry.spec.secrets import find_secret_hint


def validate_raw(data: dict[str, Any], *, source: str = "<string>") -> ProjectSpec:
    """Validate a top-level TOML table and return an immutable ProjectSpec.

    Raises:
        SpecValidationError: on unknown keys, missing/invalid fields, duplicates,
            unknown profiles/archetypes, or secret-looking content.
    """
    if not isinstance(data, dict):
        raise SpecValidationError(
            f"Project Spec root must be a table, got {type(data).__name__}",
            code="spec.root_type",
        )

    unknown = sorted(set(data) - ALLOWED_KEYS)
    if unknown:
        keys = ", ".join(repr(k) for k in unknown)
        raise SpecValidationError(
            f"unknown top-level key(s): {keys}",
            code="spec.unknown_key",
        )

    missing = sorted(REQUIRED_KEYS - set(data))
    if missing:
        keys = ", ".join(repr(k) for k in missing)
        raise SpecValidationError(
            f"missing required field(s): {keys}",
            code="spec.missing_field",
        )

    schema = _require_schema(data["schema"])
    name = _require_nonempty_str(data["name"], field="name")
    archetype = _require_archetype(data["archetype"])
    destination = _require_nonempty_str(data["destination"], field="destination")
    profiles = _require_profiles(data["profiles"])

    description: str | None = None
    if "description" in data:
        description = _require_str(data["description"], field="description")
        _reject_secrets(description, field="description")

    python_version = DEFAULT_PYTHON_VERSION
    if "python_version" in data:
        python_version = _require_python_version(data["python_version"])

    verify: VerifyMode | None = None
    if "verify" in data:
        verify = _require_verify(data["verify"])

    # Scan remaining free-text fields for secret material.
    _reject_secrets(name, field="name")
    _reject_secrets(destination, field="destination")
    for profile_id in profiles:
        _reject_secrets(profile_id, field="profiles")

    return ProjectSpec(
        schema=schema,
        name=name,
        archetype=archetype,
        destination=destination,
        profiles=profiles,
        description=description,
        python_version=python_version,
        verify=verify,
        source=source,
    )


def _require_schema(value: object) -> int:
    if not isinstance(value, int) or isinstance(value, bool):
        raise SpecValidationError(
            f"schema must be integer {SUPPORTED_SCHEMA}, got {value!r}",
            code="spec.schema_type",
        )
    if value != SUPPORTED_SCHEMA:
        raise SpecValidationError(
            f"unsupported schema = {value}; supported set is {{{SUPPORTED_SCHEMA}}}",
            code="spec.unsupported_schema",
        )
    return value


def _require_str(value: object, *, field: str) -> str:
    if not isinstance(value, str):
        raise SpecValidationError(
            f"{field} must be a string, got {type(value).__name__}",
            code="spec.field_type",
        )
    return value


def _require_nonempty_str(value: object, *, field: str) -> str:
    text = _require_str(value, field=field).strip()
    if not text:
        raise SpecValidationError(
            f"{field} must be a non-empty string",
            code="spec.empty_field",
        )
    return text


def _require_archetype(value: object) -> Archetype:
    text = _require_nonempty_str(value, field="archetype")
    if text not in ARCHETYPES:
        allowed = ", ".join(sorted(ARCHETYPES))
        raise SpecValidationError(
            f"unknown archetype {text!r}; must be one of: {allowed}",
            code="spec.unknown_archetype",
        )
    return cast(Archetype, text)


def _require_profiles(value: object) -> tuple[str, ...]:
    if not isinstance(value, list):
        raise SpecValidationError(
            f"profiles must be an array, got {type(value).__name__}",
            code="spec.profiles_type",
        )
    profiles: list[str] = []
    seen: dict[str, int] = {}
    for index, item in enumerate(value):
        if not isinstance(item, str) or not item.strip():
            raise SpecValidationError(
                f"profiles[{index}] must be a non-empty string",
                code="spec.profile_type",
            )
        profile_id = item.strip()
        if profile_id in seen:
            raise SpecValidationError(
                f"profiles lists duplicate ID {profile_id!r} "
                f"at indexes {seen[profile_id]} and {index}",
                code="spec.duplicate_profile",
            )
        seen[profile_id] = index
        if profile_id not in PROFILES:
            allowed = ", ".join(sorted(PROFILES))
            raise SpecValidationError(
                f"unknown profile {profile_id!r}; must be one of: {allowed}",
                code="spec.unknown_profile",
            )
        profiles.append(profile_id)
    return tuple(profiles)


def _require_python_version(value: object) -> str:
    text = _require_nonempty_str(value, field="python_version")
    if text not in SUPPORTED_PYTHON_VERSIONS:
        allowed = ", ".join(sorted(SUPPORTED_PYTHON_VERSIONS))
        raise SpecValidationError(
            f"unsupported python_version {text!r}; must be one of: {allowed}",
            code="spec.python_version",
        )
    return text


def _require_verify(value: object) -> VerifyMode:
    text = _require_nonempty_str(value, field="verify")
    if text not in VERIFY_MODES:
        allowed = ", ".join(sorted(VERIFY_MODES))
        raise SpecValidationError(
            f"verify must be one of: {allowed} (got {text!r})",
            code="spec.verify_mode",
        )
    return cast(VerifyMode, text)


def _reject_secrets(text: str, *, field: str) -> None:
    hint = find_secret_hint(text)
    if hint is not None:
        raise SpecValidationError(
            f"field {field!r} appears to contain secret material ({hint})",
            code="spec.secret_material",
        )
