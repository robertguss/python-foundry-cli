"""Validated Project Spec model (schema = 1)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

# Closed sets from revised-spec §11.1 / §11.3 (v1).
SUPPORTED_SCHEMA = 1
ARCHETYPES = frozenset({"cli", "scripts", "data-etl"})
PROFILES = frozenset({"http", "hooks-hk", "data-etl"})
VERIFY_MODES = frozenset({"default", "strict", "none"})
DEFAULT_PYTHON_VERSION = "3.13"
PYTHON_FLOOR = (3, 12)
# Pins accepted when python_version is set (≥ floor, documented support window).
SUPPORTED_PYTHON_VERSIONS = frozenset({"3.12", "3.13", "3.14"})

REQUIRED_KEYS = frozenset({"schema", "name", "archetype", "destination", "profiles"})
OPTIONAL_KEYS = frozenset({"description", "python_version", "verify"})
ALLOWED_KEYS = REQUIRED_KEYS | OPTIONAL_KEYS

VerifyMode = Literal["default", "strict", "none"]
Archetype = Literal["cli", "scripts", "data-etl"]


@dataclass(frozen=True, slots=True)
class ProjectSpec:
    """Immutable validated Project Spec (schema = 1)."""

    schema: int
    name: str
    archetype: Archetype
    destination: str
    profiles: tuple[str, ...]
    description: str | None = None
    python_version: str = DEFAULT_PYTHON_VERSION
    verify: VerifyMode | None = None
    source: str = "<string>"
