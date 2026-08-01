# MS-004 — hybrid template snapshot CI (public claim)

- **Date:** 2026-08-01
- **REQ:** REQ-081 / FND-010 / REQ-089
- **Spec cell:** `examples/python-foundry-template.toml` (frozen public template)
- **Catalog goldens:** `tests/goldens/hybrid-python-foundry-template/`
- **CI:** `.github/workflows/hybrid-template.yml`
- **Checker:** `python -m python_foundry.hybrid` (`python_foundry.hybrid.snapshot`)

## Acceptance (REQ-081)

| Criterion | Evidence |
| --------- | -------- |
| Frozen public template Project Spec checked in | `examples/python-foundry-template.toml` |
| CI regenerates snapshot from catalog SoT | workflow step runs `python -m python_foundry.hybrid` which calls real `generate` |
| CI **fails on drift** vs catalog goldens | non-empty `compare_trees` findings → exit 1; proven by `tests/test_hybrid_snapshot.py::test_module_cli_exits_nonzero_on_drift` and deliberate content/missing/extra file cases |
| Process forbids hand-edit as second SoT | header comment on frozen spec; this doc; catalog admission notes |

## Drift gate behavior

1. `generate --spec examples/python-foundry-template.toml` into a work dir (lock + default verify).
2. Collect file tree (excluding `.venv` / caches).
3. Diff path set + file bytes against `tests/goldens/hybrid-python-foundry-template/`.
4. Any missing, unexpected, or content-changed path → **hard fail** (`hybrid.drift`).

## Process

- Catalog under `src/python_foundry/catalog/data/` is the **only** SoT.
- The public GitHub template (when published) MUST be this regenerated snapshot.
- **Do not** hand-edit the template repository as a second catalog.
- When catalog content for the frozen cell changes intentionally: regenerate the golden tree and commit it with the catalog change.

## Prerequisites

- MS-005 dogfood evidence recorded: `docs/evidence/MS-005-dogfood.md` (FND-203).

## Commands

```bash
# Match (CI path)
uv run python -m python_foundry.hybrid

# Prove fail-on-drift (local)
# corrupt tests/goldens/hybrid-python-foundry-template/AGENTS.md then re-run;
# or: uv run pytest tests/test_hybrid_snapshot.py -q
```
