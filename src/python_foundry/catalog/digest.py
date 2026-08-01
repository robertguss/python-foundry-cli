"""Deterministic catalog digest (REQ-041).

Canonical form (stable under path separators and map iteration), matching the
go-foundry transfer pattern adapted for Python:

    for each path in lexicographic order (forward-slash, cleaned):
      write uint64be(len(path)) || path_bytes || uint64be(len(content)) || content

Digest = lowercase hex SHA-256 of that concatenation.
"""

from __future__ import annotations

import hashlib
import struct
from collections.abc import Mapping


def digest_map(files: Mapping[str, bytes]) -> str:
    """Compute catalog digest from an in-memory path → content map."""
    normalized: dict[str, bytes] = {}
    for raw_path, content in files.items():
        path = _normalize_path(raw_path)
        if path not in normalized:
            normalized[path] = content

    paths = sorted(normalized)
    hasher = hashlib.sha256()
    for path in paths:
        content = normalized[path]
        path_bytes = path.encode("utf-8")
        hasher.update(struct.pack(">Q", len(path_bytes)))
        hasher.update(path_bytes)
        hasher.update(struct.pack(">Q", len(content)))
        hasher.update(content)
    return hasher.hexdigest()


def _normalize_path(path: str) -> str:
    cleaned = path.replace("\\", "/").strip("/")
    parts = [p for p in cleaned.split("/") if p and p != "."]
    return "/".join(parts)
