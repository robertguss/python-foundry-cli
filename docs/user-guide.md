# python-foundry User Guide

**python-foundry** is a CLI tool that turns a small TOML Project Spec into a complete, production-ready Python project.

The workflow is:

```text
validate → plan → generate
```

- `validate` checks your spec.
- `plan` builds a Generation Plan without touching the filesystem.
- `generate` stages the project, refreshes `uv.lock`, runs the selected verify tier, and places the result in the destination directory.

## Table of contents

1. [Installation](#installation)
2. [Core concepts](#core-concepts)
3. [Quickstart](#quickstart)
4. [Project Spec](#project-spec)
5. [The validate-plan-generate workflow](#the-validate-plan-generate-workflow)
6. [Verify tiers](#verify-tiers)
7. [Archetypes and profiles](#archetypes-and-profiles)
8. [Catalog](#catalog)
9. [Examples](#examples)
10. [Troubleshooting](#troubleshooting)

## Installation

Requires Python 3.13+ and [uv](https://docs.astral.sh/uv/).

From this repository:

```bash
uv sync
uv run foundry version
```

Once the package is published, you can also install it with:

```bash
uv tool install python-foundry
```

`foundry` runs on macOS and Linux only.

## Core concepts

### Project Spec

A TOML file describing the project you want to generate. It declares the archetype, optional profiles, Python version, verify tier, and destination.

### Archetype

Exactly one archetype per project. It defines the project shape: `cli`, `scripts`, or `data-etl`.

### Profile

Optional add-ons: `http`, `data-etl`, or `hooks-hk`. You can combine profiles.

### Core

Every generated project receives the same Core: `pyproject.toml`, `uv` tooling, GitHub Actions, Ruff, ty, pytest, pre-commit (or hk), `fnox`/`age` secret policy, and an `AGENTS.md` agent surface.

### Generation Plan

A JSON contract produced by `foundry plan`. It lists every file, dependency, external step, and verify decision. You can save it and bind it with `generate --plan` for a two-phase commit.

## Quickstart

Create a spec:

```toml
schema = 1
name = "my-cli"
description = "My first foundry project"
archetype = "cli"
destination = "./my-cli"
profiles = ["http"]
python_version = "3.13"
```

Run the pipeline:

```bash
foundry validate --spec my-cli.toml
foundry plan   --spec my-cli.toml --json > my-cli-plan.json
foundry generate --spec my-cli.toml --plan my-cli-plan.json --dest ./my-cli
```

Inspect and run the project:

```bash
cd my-cli
uv run ruff check .
uv run pytest
```

## Project Spec

### Required fields

| Field         | Description                              |
| ------------- | ---------------------------------------- |
| `schema`      | Must be `1`.                             |
| `name`        | Project name.                            |
| `archetype`   | `cli`, `scripts`, or `data-etl`.         |
| `destination` | Where to place the generated project.    |
| `profiles`    | Array of profile ids. Use `[]` for none. |

### Optional fields

| Field            | Description                                            |
| ---------------- | ------------------------------------------------------ |
| `description`    | Project description.                                   |
| `python_version` | Python pin. Defaults to `3.13`.                        |
| `verify`         | `default`, `strict`, or `none`. Defaults to `default`. |

### Example specs

Minimal `scripts` project:

```toml
schema = 1
name = "my-tools"
archetype = "scripts"
destination = "./my-tools"
profiles = []
```

`cli` with HTTP support and hk hooks:

```toml
schema = 1
name = "my-cli"
archetype = "cli"
destination = "./my-cli"
profiles = ["http", "hooks-hk"]
python_version = "3.13"
verify = "strict"
```

## The validate-plan-generate workflow

### `foundry validate --spec PATH`

Checks the spec and reports errors. No filesystem writes.

### `foundry plan --spec PATH --json > plan.json`

Builds the Generation Plan. Review `plan.json` to see:

- resolved archetype and profiles in catalog order
- every file that will be written
- dependencies and lock production intent
- external steps (`uv lock`, `uv sync`, quality gates, pytest if `strict`)
- `verify_mode` and `verify_source`
- `plan_sha256`

### `foundry generate --spec PATH [--plan FILE] [--dest PATH] [--verify MODE]`

Generates the project. Without `--plan`, it rebuilds the plan from current inputs. With `--plan`, it binds the saved plan and fails on mismatch.

Behavior:

- Destination must be empty or non-existent.
- Renders files into a sibling staging directory.
- Refreshes `uv.lock`.
- Runs the selected verify tier.
- On success, places the project and removes the stage.
- On failure, preserves the stage and reports `stage_path`.

### Read spec from stdin

```bash
cat my-spec.toml | foundry validate --spec -
cat my-spec.toml | foundry plan --spec - --json
```

## Verify tiers

Effective mode is resolved in this order:

1. `foundry generate --verify MODE`
2. `verify` field in the spec
3. `default`

| Mode      | Steps                                                                    |
| --------- | ------------------------------------------------------------------------ |
| `default` | `uv sync --locked`, `ruff check .`, `ruff format --check .`, `ty check`. |
| `strict`  | All default steps plus `pytest` (and coverage if configured).            |
| `none`    | No pre-place verification. Lock is still attempted.                      |

Use `strict` when you want the generated project to pass its own test suite before it is placed. Use `none` to skip verification (for example, when working offline), then run the gates manually.

## Archetypes and profiles

### Archetypes

| Archetype  | Shape                                                      |
| ---------- | ---------------------------------------------------------- |
| `cli`      | `src/<module>/` package with Typer CLI, tests, CI.         |
| `scripts`  | PEP 723 scripts under `scripts/`, `uv run` workflow.       |
| `data-etl` | `src/<module>/` package with a starter pipeline and tests. |

### Profiles

| Profile    | Adds                                               |
| ---------- | -------------------------------------------------- |
| `http`     | `httpx` dependency and starter HTTP client module. |
| `data-etl` | `polars` + `pyarrow` and starter `etl_utils.py`.   |
| `hooks-hk` | Replaces pre-commit with `hk` hooks (`hk.pkl`).    |

`data-etl` is both an archetype and a profile. In a spec this is unambiguous because they live in different fields:

```toml
archetype = "data-etl"
profiles = ["data-etl"]
```

## Catalog

`foundry` ships with a closed catalog. List it with:

```bash
foundry catalog list
```

Show one unit:

```bash
foundry catalog show archetype/cli
foundry catalog show profile/http --json
```

Refs are kind-qualified: `{kind}/{id}`.

## Examples

Example specs live in the `examples/` directory:

| Spec                           | What it builds                                |
| ------------------------------ | --------------------------------------------- |
| `minimal-cli.toml`             | Smallest valid `cli` project.                 |
| `cli-with-http.toml`           | `cli` plus `http` profile.                    |
| `cli-with-hooks-hk.toml`       | `cli` plus `hooks-hk` profile.                |
| `scripts.toml`                 | `scripts` project.                            |
| `data-etl.toml`                | `data-etl` archetype plus `data-etl` profile. |
| `python-foundry-template.toml` | Frozen public GitHub template cell.           |

Try one:

```bash
foundry validate --spec examples/minimal-cli.toml
foundry plan   --spec examples/minimal-cli.toml --json > plan.json
foundry generate --spec examples/minimal-cli.toml --dest ./out
```

## Tutorials

Step-by-step tutorials are in `docs/tutorials/`:

- [Build a CLI project](tutorials/cli-tutorial.md)
- [Build a scripts project](tutorials/scripts-tutorial.md)
- [Build a data/ETL project](tutorials/data-etl-tutorial.md)

## Troubleshooting

See [Troubleshooting](troubleshooting.md) for common errors and fixes.
