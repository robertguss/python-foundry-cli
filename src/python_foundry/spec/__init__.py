"""Project Spec parse + validate (pure; no filesystem writes).

Public surface for PHASE-01:

* :func:`parse_spec_text` / :func:`parse_spec_bytes` — in-memory
* :func:`load_spec` — path or ``-`` (stdin) per REQ-023
* :class:`ProjectSpec` — immutable validated model
* :class:`SpecError` hierarchy with ``error_class = \"validation\"``
"""

from __future__ import annotations

from python_foundry.spec.errors import SpecError, SpecParseError, SpecValidationError
from python_foundry.spec.models import (
    ALLOWED_KEYS,
    ARCHETYPES,
    DEFAULT_PYTHON_VERSION,
    PROFILES,
    REQUIRED_KEYS,
    SUPPORTED_PYTHON_VERSIONS,
    SUPPORTED_SCHEMA,
    VERIFY_MODES,
    ProjectSpec,
)
from python_foundry.spec.parse import (
    STDIN_SPEC,
    load_spec,
    load_spec_stream,
    parse_spec_bytes,
    parse_spec_text,
)
from python_foundry.spec.validate import validate_raw

__all__ = [
    "ALLOWED_KEYS",
    "ARCHETYPES",
    "DEFAULT_PYTHON_VERSION",
    "PROFILES",
    "REQUIRED_KEYS",
    "STDIN_SPEC",
    "SUPPORTED_PYTHON_VERSIONS",
    "SUPPORTED_SCHEMA",
    "VERIFY_MODES",
    "ProjectSpec",
    "SpecError",
    "SpecParseError",
    "SpecValidationError",
    "load_spec",
    "load_spec_stream",
    "parse_spec_bytes",
    "parse_spec_text",
    "validate_raw",
]
