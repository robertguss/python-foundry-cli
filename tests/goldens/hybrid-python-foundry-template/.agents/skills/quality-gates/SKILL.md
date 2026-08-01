---
name: quality-gates
description: Run uv/ruff/ty/pytest quality gates for python-foundry-template
---

# Quality gates

```bash
uv sync --locked
uv run ruff check .
uv run ruff format --check .
uv run ty check
uv run pytest
```

ty is Required in default verify. Do not demote without an explicit DEC.

## Definition of done

`foundry generate` default-verify success (sync + ruff + ty) does **not**
satisfy the agent Definition of Done. After place (or on an existing
Generated Project), do not claim work complete until `pytest` also passes —
**0 tests collected is not success** unless the change is explicitly
docs-only. On conflict with AGENTS.md, AGENTS.md wins.

## With foundry

Prefer `foundry generate --plan plan.json` after reviewing plan JSON.
