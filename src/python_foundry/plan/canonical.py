"""Canonical JSON serialization for plan_sha256 (REQ-026 / FND-009)."""

from __future__ import annotations

import hashlib
import json
from typing import Any


def canonical_json_bytes(value: Any) -> bytes:
    """UTF-8 JSON: sorted keys at every level, compact separators, no NaN/Inf."""
    return json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
        allow_nan=False,
    ).encode("utf-8")


def sha256_hex(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def content_digest(payload: bytes) -> str:
    """SHA-256 hex of file content bytes (stub: often empty or source label)."""
    return sha256_hex(payload)
