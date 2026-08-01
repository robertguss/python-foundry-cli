"""Load Project Spec from path, stdin, or in-memory text (read-only I/O)."""

from __future__ import annotations

import sys
import tomllib
from pathlib import Path
from typing import BinaryIO, TextIO

from python_foundry.spec.errors import SpecParseError
from python_foundry.spec.models import ProjectSpec
from python_foundry.spec.validate import validate_raw

# Sentinel / documented form for stdin (REQ-023).
STDIN_SPEC = "-"


def parse_spec_bytes(data: bytes, *, source: str = "<string>") -> ProjectSpec:
    """Parse and validate a Project Spec from TOML bytes."""
    try:
        raw = tomllib.loads(data.decode("utf-8"))
    except UnicodeDecodeError as exc:
        raise SpecParseError(
            f"Project Spec is not valid UTF-8: {exc}",
            code="spec.encoding",
        ) from exc
    except tomllib.TOMLDecodeError as exc:
        raise SpecParseError(
            f"invalid TOML in Project Spec: {exc}",
            code="spec.toml",
        ) from exc

    if not isinstance(raw, dict):
        raise SpecParseError(
            f"Project Spec root must be a table, got {type(raw).__name__}",
            code="spec.root_type",
        )
    return validate_raw(raw, source=source)


def parse_spec_text(text: str, *, source: str = "<string>") -> ProjectSpec:
    """Parse and validate a Project Spec from a Unicode string."""
    return parse_spec_bytes(text.encode("utf-8"), source=source)


def load_spec(path: str | Path, *, encoding: str = "utf-8") -> ProjectSpec:
    """Load a Project Spec from a filesystem path or stdin.

    Pass ``path="-"`` (or :data:`STDIN_SPEC`) to read the entire stdin stream
    (REQ-023). Only reads; never writes.
    """
    path_str = str(path)
    if path_str == STDIN_SPEC:
        return load_spec_stream(sys.stdin.buffer, source="<stdin>")

    file_path = Path(path_str)
    try:
        data = file_path.read_bytes()
    except OSError as exc:
        raise SpecParseError(
            f"cannot read Project Spec {file_path}: {exc}",
            code="spec.read",
        ) from exc
    return parse_spec_bytes(data, source=str(file_path))


def load_spec_stream(
    stream: BinaryIO | TextIO,
    *,
    source: str = "<stream>",
) -> ProjectSpec:
    """Read all bytes/text from *stream* and parse as a Project Spec."""
    try:
        payload = stream.read()
    except OSError as exc:
        raise SpecParseError(
            f"cannot read Project Spec from {source}: {exc}",
            code="spec.read",
        ) from exc

    if isinstance(payload, str):
        return parse_spec_text(payload, source=source)
    if isinstance(payload, bytes | bytearray):
        return parse_spec_bytes(bytes(payload), source=source)
    raise SpecParseError(
        f"stream {source} returned unsupported type {type(payload).__name__}",
        code="spec.stream_type",
    )
