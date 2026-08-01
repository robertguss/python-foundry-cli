# MS-005 — full foundry dogfood (before hybrid claim)

- **Date:** 2026-08-01
- **Host:** Linux

## Observable acceptance (FND-204)

1. **Product CI:** `.github/workflows/ci.yml` runs `uv sync --locked`, ruff, ty, pytest.
2. **Product AGENTS.md** governs this product repo; research-program skills are not emitted into Generated Projects (catalog templates only ship Generated Core skills).
3. **Commands run (this record):**

```bash
uv sync --locked
uv run ruff check .
uv run ty check
uv run pytest
uv run foundry version
uv run foundry validate --spec examples/minimal-cli.toml
uv run foundry plan --spec examples/minimal-cli.toml --json
```

4. **Core alignment:** foundry itself uses uv, ruff, ty, pytest; Generated Projects inherit the same toolchain via catalog Core.
5. **Surface separation:** no research `AGENTS.md` skills packaged under `catalog/` for emit; product rules stay in product `AGENTS.md`.

Recorded **before** MS-004 public hybrid claim (FND-203).
