"""Custom template engine (not Copier/Cookiecutter) — simple ``{{key}}`` fill."""

from __future__ import annotations

import re
from collections.abc import Mapping

_PLACEHOLDER = re.compile(r"\{\{\s*([a-zA-Z_][a-zA-Z0-9_]*)\s*\}\}")


def render_template(text: str, context: Mapping[str, str]) -> str:
    """Replace ``{{key}}`` placeholders; unknown keys left unchanged."""

    def repl(match: re.Match[str]) -> str:
        key = match.group(1)
        if key in context:
            return context[key]
        return match.group(0)

    return _PLACEHOLDER.sub(repl, text)


def render_path(path_template: str, context: Mapping[str, str]) -> str:
    """Render a planned path that may contain ``{{name}}`` tokens."""
    return render_template(path_template, context)
