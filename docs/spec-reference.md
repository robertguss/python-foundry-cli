# Project Spec Reference

A Project Spec is a TOML file that tells `foundry` what kind of Python project to generate.

## Example

```toml
schema = 1
name = "my-project"
description = "My generated project"
archetype = "cli"
destination = "./my-project"
profiles = ["http"]
python_version = "3.13"
verify = "default"
```

## Fields

| Field | Required | Description |
| ----- | -------- | ----------- |
| `schema` | Yes | Schema version. Must be `1`. |
| `name` | Yes | Project name. Used in `pyproject.toml` and file paths. |
| `description` | No | Free-text description. Included in `pyproject.toml`. |
| `archetype` | Yes | Exactly one of `cli`, `scripts`, or `data-etl`. |
| `destination` | Yes | Directory where the project will be placed. The basename should usually match `name`. |
| `profiles` | Yes | Array of profile ids. May be `[]`. Duplicates are an error. |
| `python_version` | No | Python version pin, e.g. `3.13`. If omitted, defaults to `3.13`. Must be `>= 3.12`. |
| `verify` | No | Verify tier for `generate`: `default`, `strict`, or `none`. If omitted, effective mode is `default`. |

## Rules

- `foundry` hard-fails on unknown keys.
- `profiles` is treated as a set. Duplicate ids cause an error.
- Profile apply order is determined by the catalog, not by array order.
- Do not put secrets or credentials in a Project Spec.

## Archetypes

Exactly one archetype is required. It defines the primary project shape.

| Archetype | Project shape |
| --------- | ------------- |
| `cli` | Package under `src/`, Typer entrypoint, CLI tests. |
| `scripts` | PEP 723 scripts under `scripts/`, `uv run` workflow, no mandatory `src` package. |
| `data-etl` | `src/` package with a starter pipeline module and tests. |

## Profiles

Profiles add dependencies, files, or tooling. Choose any subset of the closed catalog.

| Profile | Adds |
| ------- | ---- |
| `http` | `httpx` dependency and a starter HTTP client module. |
| `data-etl` | `polars` + `pyarrow` and a starter `etl_utils` module. |
| `hooks-hk` | Replaces the default pre-commit config with `hk` hooks (`hk.pkl`). |

Profiles can be combined. For example, a `cli` project with HTTP support and `hk` hooks:

```toml
archetype = "cli"
profiles = ["http", "hooks-hk"]
```

## Verify modes

The `verify` field controls how much checking `generate` runs before placing the project.

| Mode | What it does |
| ---- | ------------ |
| `default` | `uv sync --locked`, `ruff check .`, `ruff format --check .`, `ty check`. |
| `strict` | Everything in `default` plus `pytest` (and coverage if configured). |
| `none` | No pre-place verification. Use with care; the generated project still includes tooling. |

Effective mode is resolved in this order:

1. `foundry generate --verify MODE`
2. `verify` field in the Project Spec
3. `default`

## Minimal valid spec

```toml
schema = 1
name = "hello"
archetype = "scripts"
destination = "./hello"
profiles = []
```

## Read from stdin

Every `--spec` option also accepts `-`:

```bash
cat my-spec.toml | foundry validate --spec -
```
