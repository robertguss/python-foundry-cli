"""Filesystem stage/place errors (error_class=place)."""

from __future__ import annotations


class FsxError(Exception):
    """Base error for stage/place operations."""

    error_class: str = "place"

    def __init__(
        self,
        message: str,
        *,
        code: str = "fsx.error",
        stage_path: str | None = None,
    ) -> None:
        super().__init__(message)
        self.message = message
        self.code = code
        self.stage_path = stage_path

    def __str__(self) -> str:
        return self.message


class StageError(FsxError):
    error_class = "place"

    def __init__(
        self,
        message: str,
        *,
        code: str = "fsx.stage",
        stage_path: str | None = None,
    ) -> None:
        super().__init__(message, code=code, stage_path=stage_path)


class PlaceError(FsxError):
    error_class = "place"

    def __init__(
        self,
        message: str,
        *,
        code: str = "fsx.place",
        stage_path: str | None = None,
    ) -> None:
        super().__init__(message, code=code, stage_path=stage_path)


class PathEscapeError(FsxError):
    error_class = "place"

    def __init__(
        self,
        message: str,
        *,
        code: str = "fsx.path_escape",
        stage_path: str | None = None,
    ) -> None:
        super().__init__(message, code=code, stage_path=stage_path)
