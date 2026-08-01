# SPK-002 — Practical Core ty config freeze

- **Phase:** PHASE-04
- **Date:** 2026-08-01

## Frozen defaults

Core `pyproject.toml` template includes:

```toml
[tool.ty.environment]
python-version = "{{python_version}}"
```

- ty remains **Required** in default verify (`uv run ty check` step).
- Demoting ty requires an accepted DEC (not residual-accept).
- Residual: advanced ty rule keys deferred; pin notes in `catalog/.../versions.toml`.
