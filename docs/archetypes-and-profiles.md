# Archetypes and Profiles

`foundry` builds a project from two pieces:

- **One archetype** — the project shape.
- **Zero or more profiles** — optional capabilities layered on top.

Every generated project also includes the **Core** unit: tooling, layout, CI, secrets policy, and agent rules.

## Archetypes

### `cli`

A conventional package-style CLI project.

Generated structure (partial):

```text
my-cli/
├── src/
│   └── my_cli/
│       ├── __init__.py
│       └── cli.py
├── tests/
│   └── test_version.py
├── pyproject.toml
├── uv.lock
└── .github/workflows/ci.yml
```

- Entrypoint console script wired in `pyproject.toml`.
- Uses [Typer](https://typer.tiangolo.com/) for the CLI starter.
- Includes a starter skill at `.agents/skills/add-cli-command/SKILL.md`.

Example spec:

```toml
schema = 1
name = "my-cli"
archetype = "cli"
destination = "./my-cli"
profiles = []
```

### `scripts`

A scripts-oriented project that uses PEP 723 inline metadata and `uv run`.

Generated structure (partial):

```text
my-scripts/
├── scripts/
│   └── hello.py
├── tests/
│   └── test_hello_script.py
├── pyproject.toml
└── uv.lock
```

- No mandatory `src/` package.
- Each script carries its own dependency metadata.
- Includes a starter skill at `.agents/skills/add-script/SKILL.md`.

Example spec:

```toml
schema = 1
name = "my-scripts"
archetype = "scripts"
destination = "./my-scripts"
profiles = []
```

### `data-etl`

A `src/` package project with a starter data pipeline.

Generated structure (partial):

```text
my-etl/
├── src/
│   └── my_etl/
│       ├── __init__.py
│       ├── pipeline.py
│       └── etl_utils.py   # when profile/data-etl is selected
├── tests/
│   └── test_pipeline.py
├── pyproject.toml
└── uv.lock
```

- Designed for data/ETL work.
- Combines cleanly with the `data-etl` profile for `polars` + `pyarrow`.

Example spec:

```toml
schema = 1
name = "my-etl"
archetype = "data-etl"
destination = "./my-etl"
profiles = ["data-etl"]
```

## Profiles

Profiles are optional. Add them to the `profiles` array in any order; the catalog decides the apply order.

### `http`

Adds an `httpx` dependency and a starter `http_client.py` module under the package.

Use with `cli` or `data-etl` archetypes.

```toml
profiles = ["http"]
```

### `data-etl`

Adds `polars` and `pyarrow` dependencies plus a starter `etl_utils.py` module.

Note: `data-etl` is both an archetype and a profile id. The spec is unambiguous because archetypes go in `archetype` and profiles go in `profiles`.

```toml
archetype = "data-etl"
profiles = ["data-etl"]
```

`pyarrow` may require a working C++ build toolchain on some systems. If `uv lock` fails, install the system build dependencies for your platform and retry.

### `hooks-hk`

Replaces the default `.pre-commit-config.yaml` with an `hk.pkl` configuration for the [hk](https://github.com/jdx/hk) hooks runner.

```toml
profiles = ["hooks-hk"]
```

## Combining profiles

You can select multiple profiles. This example uses `http` and `hooks-hk` with a `cli` project:

```toml
schema = 1
name = "my-cli"
archetype = "cli"
destination = "./my-cli"
profiles = ["http", "hooks-hk"]
python_version = "3.13"
```

Run `foundry catalog list` to see the current closed set of archetypes and profiles.
