# Agent rules — python-foundry (product)

This is the **product** repository. Research methodology and stage machinery
live in the sibling research repo (`python-foundry`), not here.

## Authority (read before coding)

1. [`docs/02-definitive-specification-revised.md`](docs/02-definitive-specification-revised.md) — **product law**
2. [`docs/02-implementation-plan-revised.md`](docs/02-implementation-plan-revised.md) — **delivery sequence**
3. [`docs/AUTHORITY.md`](docs/AUTHORITY.md) — pinned source commits
4. This file — product workflow only

Do not invent REQs, demote locks, or treat chat history as authority.

## Current delivery position

- **Phase:** PHASE-01 — pure pipeline (write-free)
- **Exit spike:** SPK-100 / milestone **MS-001** (golden plan for minimal `cli`)
- **Not yet:** stage/place (PHASE-02), real `generate` (PHASE-03), full catalog
  content (PHASE-04), hybrid template (PHASE-05)

## Package layout (revised-spec §10.1)

```text
src/python_foundry/
  cli/       # Typer wiring only
  spec/      # parse + validate (pure)
  catalog/   # load manifests, digests
  resolve/   # archetype/profile resolution (pure)
  plan/      # Construct plan (pure)
  report/    # text/JSON encoding
  render/    # later
  fsx/       # later (PHASE-02)
  generate/  # later (PHASE-03)
  verify/    # later (PHASE-03)
catalog/     # authoring tree (packaged as data)
```

**Purity rule:** `plan` MUST NOT import `fsx`, `generate`, or `cli`.

## Product locks (never silently undo)

- ty Required; fnox+age; no dotenv secrets
- AGENTS.md + `.agents/skills/` only for Generated Projects; no Claude adapters
- Exclusive place; custom engine; closed catalog
- Generate-time `uv.lock`; verify CLI > TOML > `default`
- Optional `generate --plan` bind; unbound generate rebuilds honestly
- macOS + Linux only; no Windows

## Foundry vs Generated surfaces

Research-program skills and research `AGENTS.md` rules must **not** ship into
Generated Project emit (REQ-076). Keep product-agent docs and Generated Core
agent surface separate.

## Commands

```bash
uv sync
uv run foundry …
uv run pytest
uv run ruff check .
uv run ty check
```

## Definition of done (local)

- Tests green; no purity violations
- Phase exit criteria from the revised plan before claiming a milestone
- No secret material in Project Specs or goldens
