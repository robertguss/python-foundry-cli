"""Render planned files into a stage (no place to final destination)."""

from __future__ import annotations

import json
from collections.abc import Mapping, Sequence
from importlib import resources
from pathlib import Path

from python_foundry.fsx.stage import Stage
from python_foundry.plan.models import GenerationPlan
from python_foundry.render.engine import render_path, render_template
from python_foundry.spec.models import ProjectSpec

_DATA_PACKAGE = "python_foundry.catalog"
_DATA_DIR = "data"


class RenderError(Exception):
    error_class: str = "render"

    def __init__(self, message: str, *, code: str = "render.error") -> None:
        super().__init__(message)
        self.message = message
        self.code = code


def build_context(
    spec: ProjectSpec, dependencies: Sequence[str] = ()
) -> dict[str, str]:
    # Project name may be kebab-case; importable package path needs underscores.
    module = spec.name.replace("-", "_")
    return {
        "name": spec.name,
        "module": module,
        "description": spec.description or "",
        "archetype": spec.archetype,
        "python_version": spec.python_version,
        "destination": spec.destination,
        # Resolved archetype/profile dependency additions (REQ-059/REQ-061),
        # rendered as a TOML/Python-compatible array-of-strings literal.
        "dependencies_toml": _dependencies_toml(dependencies),
    }


def _dependencies_toml(dependencies: Sequence[str]) -> str:
    if not dependencies:
        return "[]"
    return "[" + ", ".join(json.dumps(dep) for dep in dependencies) + "]"


def load_unit_source(owner_kind: str, owner_id: str, source: str) -> bytes:
    """Load a catalog unit source file from package data."""
    if owner_kind == "core":
        rel = f"core/{source}"
    elif owner_kind == "archetype":
        rel = f"archetypes/{owner_id}/{source}"
    elif owner_kind == "profile":
        rel = f"profiles/{owner_id}/{source}"
    else:
        raise RenderError(
            f"unknown owner kind {owner_kind!r}",
            code="render.owner_kind",
        )
    root = resources.files(_DATA_PACKAGE).joinpath(_DATA_DIR)
    path = root.joinpath(*rel.split("/"))
    if not path.is_file():
        raise RenderError(
            f"catalog source missing: {rel}",
            code="render.missing_source",
        )
    return path.read_bytes()


def render_plan_into_stage(
    plan: GenerationPlan,
    spec: ProjectSpec,
    stage: Stage,
    *,
    context: Mapping[str, str] | None = None,
) -> list[Path]:
    """Render all planned files into *stage*. Does not place to destination."""
    if context is not None:
        ctx = dict(context)
    else:
        deps = [str(d) for d in plan.body.get("dependencies", [])]
        ctx = build_context(spec, deps)
    written: list[Path] = []
    for entry in plan.body["files"]:
        path_tmpl = str(entry["path"])
        out_rel = render_path(path_tmpl, ctx)
        owner = entry["owner"]
        source = _source_for_entry(plan, entry)
        raw = load_unit_source(owner["kind"], owner["id"], source)
        mode = int(str(entry.get("mode", "0644")), 8)
        if entry["render"] == "template":
            text = render_template(raw.decode("utf-8"), ctx)
            path = stage.write_text(out_rel, text, mode=mode)
        else:
            path = stage.write_bytes(out_rel, raw, mode=mode)
        written.append(path)
    return written


def _source_for_entry(plan: GenerationPlan, entry: dict) -> str:
    """Map planned path back to catalog source via owner unit inventory.

    Plan files carry path/render/mode/owner but content_digest only. Look up
    source from the sealed plan's resolved units by re-reading catalog is
    cleaner — store source in plan files instead.

    PHASE-03: plan Construct already embeds owner; we re-resolve source from
    the planned path by matching against construct-time planned files if
    present, else derive from owner file inventory via package data manifests.
    """
    # Prefer explicit source if Construct starts recording it later.
    if "source" in entry:
        return str(entry["source"])
    # Recover from owner inventory in package data.
    from python_foundry.catalog import load_default_catalog

    cat = load_default_catalog()
    unit = cat.get(entry["owner"]["kind"], entry["owner"]["id"])
    # Match by rendered path template equality to inventory path.
    path_tmpl = entry["path"]
    for inv in unit.files:
        if inv.path == path_tmpl:
            return inv.source
    raise RenderError(
        f"no inventory source for {path_tmpl!r} owned by "
        f"{entry['owner']['kind']}/{entry['owner']['id']}",
        code="render.source_lookup",
    )
