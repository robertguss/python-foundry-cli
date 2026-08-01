# python-foundry-cli

**python-foundry** is an AI-native hybrid foundry for modern Python projects:
`validate` → `plan` → `generate` (CLI + strong Core + GitHub template surface).

This repository is the **product implementation**. Research, specification, and
planning live in [python-foundry](https://github.com/robertguss/python-foundry)
(local sibling: `../python-foundry`).

| | |
| - | - |
| **Package** | `python-foundry` |
| **CLI (provisional)** | `foundry` |
| **Python** | ≥ 3.13 (uv) |
| **Hosts** | Linux required (CI); macOS optional; **no Windows** |
| **Current phase** | v1 delivery complete (PHASE-01..06) |

## Specification authority

Do **not** invent product behavior outside these documents:

| Role | Doc |
| ---- | --- |
| Product law | [`docs/02-definitive-specification-revised.md`](docs/02-definitive-specification-revised.md) |
| Delivery sequence | [`docs/02-implementation-plan-revised.md`](docs/02-implementation-plan-revised.md) |
| Pins / provenance | [`docs/AUTHORITY.md`](docs/AUTHORITY.md) |

Agent rules for this repo: [`AGENTS.md`](AGENTS.md).

## Status

v1 product pipeline is implemented:

- `foundry validate` / `plan` / `catalog list|show` / `version` / `generate`
- Closed catalog Core + archetypes + profiles; exclusive place; generate-time lock

## Quickstart

```bash
# From this repo root
uv sync
uv run foundry version   # stub until PHASE-01 lands
uv run pytest
```

Intended dry-run workflow (once PHASE-01 commands exist):

```bash
foundry validate --spec ./examples/minimal-cli.toml
foundry plan --spec ./examples/minimal-cli.toml
# generate later (PHASE-03+):
# foundry generate --spec ./examples/minimal-cli.toml --dest ./out
```

## Layout

```text
src/python_foundry/   # package (§10.1 of the revised spec)
catalog/              # closed catalog authoring tree (package data)
docs/                 # implementation authority copies
examples/             # Project Spec fixtures
tests/
```

## Development

```bash
uv sync
uv run ruff check .
uv run ruff format --check .
uv run ty check
uv run pytest
```

## Locks (do not reverse without DEC)

- **ty** Required in Core / default verify  
- **fnox + age** for secrets; **no** dotenv secret storage  
- **AGENTS.md** + `.agents/skills/` only; **no** Claude adapters in Core emit  
- Exclusive place; custom engine (not Copier/Cookiecutter runtime)  
- Closed catalog; generate-time `uv.lock`; verify CLI > TOML > `default`  

See the revised specification for full REQs and the revised plan for phase gates.
