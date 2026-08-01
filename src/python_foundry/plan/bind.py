"""Optional ``--plan`` bind API shape (FND-004 / REQ-086) — no stage writes."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from python_foundry.catalog.load import Catalog
from python_foundry.plan.construct import construct
from python_foundry.plan.models import GenerationPlan
from python_foundry.spec.models import ProjectSpec


class PlanBindError(Exception):
    """Bound plan does not match recomputed Construct."""

    error_class: str = "plan_bind"

    def __init__(self, message: str, *, code: str = "plan_bind.mismatch") -> None:
        super().__init__(message)
        self.message = message
        self.code = code

    def __str__(self) -> str:
        return self.message


def load_plan_artifact(path: str | Path) -> dict[str, Any]:
    """Load a plan JSON artifact from disk (read-only).

    Accepts either a bare plan body or ``{"ok": true, "plan": {...}}`` wrapper
    as emitted by ``foundry plan --json``.
    """
    file_path = Path(path)
    try:
        raw = json.loads(file_path.read_text(encoding="utf-8"))
    except OSError as exc:
        raise PlanBindError(
            f"cannot read plan artifact {file_path}: {exc}",
            code="plan_bind.read",
        ) from exc
    except json.JSONDecodeError as exc:
        raise PlanBindError(
            f"invalid plan JSON in {file_path}: {exc}",
            code="plan_bind.json",
        ) from exc

    if not isinstance(raw, dict):
        raise PlanBindError(
            "plan artifact root must be a JSON object",
            code="plan_bind.root",
        )
    if "plan" in raw and isinstance(raw["plan"], dict):
        return raw["plan"]
    return raw


def bind_plan(
    *,
    spec: ProjectSpec,
    catalog: Catalog,
    plan_artifact: dict[str, Any] | str | Path,
    cli_verify: str | None = None,
    foundry_version: str | None = None,
) -> GenerationPlan:
    """Recompute Construct and hard-fail on bind mismatch (no stage writes).

    Compares ``plan_sha256``, foundry version, and catalog digest. On any
    mismatch raises :class:`PlanBindError` with ``error_class=plan_bind``
    **before** any write/stage API is invoked (callers must not create stages
    when this fails).
    """
    if isinstance(plan_artifact, str | Path):
        bound = load_plan_artifact(plan_artifact)
    else:
        bound = plan_artifact

    recomputed = construct(
        spec,
        catalog,
        cli_verify=cli_verify,
        foundry_version=foundry_version,
    )

    bound_sha = bound.get("plan_sha256")
    bound_version = _nested(bound, "foundry", "version")
    bound_digest = bound.get("catalog_digest")

    mismatches: list[str] = []
    if bound_sha != recomputed.plan_sha256:
        mismatches.append(
            f"plan_sha256 bound={bound_sha!r} recomputed={recomputed.plan_sha256!r}"
        )
    if bound_version != recomputed.foundry_version:
        mismatches.append(
            f"foundry.version bound={bound_version!r} "
            f"recomputed={recomputed.foundry_version!r}"
        )
    if bound_digest != recomputed.catalog_digest:
        mismatches.append(
            f"catalog_digest bound={bound_digest!r} "
            f"recomputed={recomputed.catalog_digest!r}"
        )

    if mismatches:
        raise PlanBindError(
            "plan bind mismatch: " + "; ".join(mismatches),
            code="plan_bind.mismatch",
        )

    # Match: return recomputed sealed plan (authoritative Construct).
    return recomputed


def rebuild_plan(
    *,
    spec: ProjectSpec,
    catalog: Catalog,
    cli_verify: str | None = None,
    foundry_version: str | None = None,
) -> GenerationPlan:
    """Unbound path: Construct from current inputs (honest single-step rebuild)."""
    return construct(
        spec,
        catalog,
        cli_verify=cli_verify,
        foundry_version=foundry_version,
    )


def _nested(obj: dict[str, Any], *keys: str) -> Any:
    cur: Any = obj
    for key in keys:
        if not isinstance(cur, dict):
            return None
        cur = cur.get(key)
    return cur
