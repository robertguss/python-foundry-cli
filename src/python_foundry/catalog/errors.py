"""Catalog load errors (error_class=resolve for unknown units; validation-adjacent)."""

from __future__ import annotations


class CatalogError(Exception):
    """Base error for closed-catalog load and lookup failures."""

    error_class: str = "resolve"

    def __init__(self, message: str, *, code: str = "catalog.error") -> None:
        super().__init__(message)
        self.message = message
        self.code = code

    def __str__(self) -> str:
        return self.message


class CatalogLoadError(CatalogError):
    """Catalog tree could not be loaded or a manifest is invalid."""

    error_class = "internal"

    def __init__(self, message: str, *, code: str = "catalog.load") -> None:
        super().__init__(message, code=code)


class CatalogLookupError(CatalogError):
    """Requested unit id/kind is not in the closed catalog."""

    error_class = "resolve"

    def __init__(self, message: str, *, code: str = "catalog.unknown_unit") -> None:
        super().__init__(message, code=code)
