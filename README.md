# python-foundry

`python-foundry` is a CLI tool that turns a small TOML Project Spec into a complete, production-ready Python project.

The workflow is:

```text
foundry validate → foundry plan → foundry generate
```

- `validate` checks your spec without writing anything.
- `plan` builds a Generation Plan (a JSON contract) without touching the filesystem.
- `generate` stages the project, refreshes `uv.lock`, runs the selected verify tier, and places the result in the destination directory.

|             |                                |
| ----------- | ------------------------------ |
| **Package** | `python-foundry`               |
| **CLI**     | `foundry`                      |
| **Python**  | 3.13+                          |
| **Hosts**   | macOS + Linux only; no Windows |

## Install

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

## Quickstart

Create `my-cli.toml`:

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

Then use the generated project:

```bash
cd my-cli
uv run ruff check .
uv run pytest
```

See the [full User Guide](docs/user-guide.md) for details.

## Project Spec

A Project Spec is a TOML file that declares what you want to build.

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

Minimal example:

```toml
schema = 1
name = "my-tools"
archetype = "scripts"
destination = "./my-tools"
profiles = []
```

Full reference: [docs/spec-reference.md](docs/spec-reference.md)

## Archetypes and profiles

### Archetypes (choose exactly one)

| Archetype  | Shape                                                      |
| ---------- | ---------------------------------------------------------- |
| `cli`      | `src/<module>/` package with Typer CLI, tests, CI.         |
| `scripts`  | PEP 723 scripts under `scripts/`, `uv run` workflow.       |
| `data-etl` | `src/<module>/` package with a starter pipeline and tests. |

### Profiles (choose any subset)

| Profile    | Adds                                               |
| ---------- | -------------------------------------------------- |
| `http`     | `httpx` dependency and starter HTTP client module. |
| `data-etl` | `polars` + `pyarrow` and starter `etl_utils.py`.   |
| `hooks-hk` | Replaces pre-commit with `hk` hooks (`hk.pkl`).    |

`data-etl` is both an archetype and a profile id. In a spec this is unambiguous because they live in different fields:

```toml
archetype = "data-etl"
profiles = ["data-etl"]
```

Details: [docs/archetypes-and-profiles.md](docs/archetypes-and-profiles.md)

## The validate-plan-generate workflow

### `foundry validate --spec PATH`

Checks the spec. No filesystem writes.

### `foundry plan --spec PATH --json > plan.json`

Builds the Generation Plan. Review `plan.json` to see every file, dependency, external step, and the `plan_sha256`.

### `foundry generate --spec PATH [--plan FILE] [--dest PATH] [--verify MODE]`

Generates the project:

- Destination must be empty or non-existent.
- Files are rendered into a sibling staging directory.
- `uv.lock` is refreshed to match the resolved dependencies.
- The selected verify tier runs in the stage.
- On success, the project is placed and the stage is removed.
- On failure, the stage is preserved and the JSON report includes the absolute `stage_path`.

With `--plan`, `generate` binds the saved plan and fails if the spec, catalog digest, or foundry version changed.

Read from stdin:

```bash
cat my-spec.toml | foundry validate --spec -
```

Command reference: [docs/commands.md](docs/commands.md)

## Verify tiers

Effective mode is resolved in this order:

1. `foundry generate --verify MODE`
2. `verify` field in the spec
3. `default`

| Mode      | Steps                                                                    |
| --------- | ------------------------------------------------------------------------ |
| `default` | `uv sync --locked`, `ruff check .`, `ruff format --check .`, `ty check`. |
| `strict`  | All default steps plus `pytest`.                                         |
| `none`    | No pre-place verification. Lock is still attempted.                      |

Use `strict` to ensure the generated project passes its own tests before it is placed.

## Catalog

`foundry` ships with a closed catalog. List it with:

```bash
foundry catalog list
```

Show one unit by kind-qualified reference:

```bash
foundry catalog show archetype/cli
foundry catalog show profile/http --json
```

Catalog reference: [docs/catalog.md](docs/catalog.md)

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

- [Build a CLI project](docs/tutorials/cli-tutorial.md)
- [Build a scripts project](docs/tutorials/scripts-tutorial.md)
- [Build a data/ETL project](docs/tutorials/data-etl-tutorial.md)

## Troubleshooting

See [docs/troubleshooting.md](docs/troubleshooting.md) for common errors and fixes.

## Documentation index

| Doc                                                                | Purpose                        |
| ------------------------------------------------------------------ | ------------------------------ |
| [docs/user-guide.md](docs/user-guide.md)                           | Canonical full user guide.     |
| [docs/quickstart.md](docs/quickstart.md)                           | Short getting-started guide.   |
| [docs/commands.md](docs/commands.md)                               | CLI command reference.         |
| [docs/spec-reference.md](docs/spec-reference.md)                   | Project Spec field reference.  |
| [docs/archetypes-and-profiles.md](docs/archetypes-and-profiles.md) | Archetype and profile details. |
| [docs/catalog.md](docs/catalog.md)                                 | Catalog usage.                 |
| [docs/troubleshooting.md](docs/troubleshooting.md)                 | Common issues.                 |
| [examples/](examples/)                                             | Runnable Project Specs.        |
