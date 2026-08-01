"""Custom render engine + stage materialization (PHASE-03)."""

from __future__ import annotations

from python_foundry.render.engine import render_path, render_template
from python_foundry.render.stage_render import (
    RenderError,
    build_context,
    load_unit_source,
    render_plan_into_stage,
)

__all__ = [
    "RenderError",
    "build_context",
    "load_unit_source",
    "render_path",
    "render_plan_into_stage",
    "render_template",
]
