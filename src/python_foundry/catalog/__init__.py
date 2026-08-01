"""Closed catalog load, digest, and kind-qualified list/show (PHASE-01).

Catalog authoring tree lives at package data ``python_foundry.catalog.data``
(repo-root ``catalog/`` is a symlink to that tree for authoring convenience).
"""

from __future__ import annotations

from python_foundry.catalog.digest import digest_map
from python_foundry.catalog.errors import (
    CatalogError,
    CatalogLoadError,
    CatalogLookupError,
)
from python_foundry.catalog.load import Catalog, load_catalog_tree, load_default_catalog
from python_foundry.catalog.models import FileEntry, Kind, UnitManifest, UnitSummary

__all__ = [
    "Catalog",
    "CatalogError",
    "CatalogLoadError",
    "CatalogLookupError",
    "FileEntry",
    "Kind",
    "UnitManifest",
    "UnitSummary",
    "digest_map",
    "load_catalog_tree",
    "load_default_catalog",
]
