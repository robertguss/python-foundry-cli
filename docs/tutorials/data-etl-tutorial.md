# Tutorial: Build a Data/ETL Project

This tutorial creates a data/ETL project using the `data-etl` archetype with the `data-etl` profile for `polars` and `pyarrow`.

## Goals

- Write a `data-etl` Project Spec.
- Generate a project with a starter pipeline.
- Run the starter code and tests.

## Create the spec

Create `my-pipeline.toml`:

```toml
schema = 1
name = "my-pipeline"
description = "A starter data pipeline"
archetype = "data-etl"
destination = "./my-pipeline"
profiles = []
python_version = "3.13"
verify = "strict"
```

This uses the `data-etl` archetype, which creates a `src/my_pipeline/pipeline.py` starter module and a matching test.

## Validate, plan, and generate

```bash
foundry validate --spec my-pipeline.toml
foundry plan   --spec my-pipeline.toml --json > my-pipeline-plan.json
foundry generate --spec my-pipeline.toml --plan my-pipeline-plan.json --dest ./my-pipeline
```

## Inspect the project

```bash
cd my-pipeline
find . -type f | sort
```

```text
my-pipeline/
├── src/
│   └── my_pipeline/
│       ├── __init__.py
│       ├── etl_utils.py
│       └── pipeline.py
├── tests/
│   └── test_pipeline.py
├── .agents/
│   └── skills/
│       ├── add-script/SKILL.md
│       ├── quality-gates/SKILL.md
│       └── secrets-fnox/SKILL.md
├── .github/workflows/ci.yml
├── .gitignore
├── .pre-commit-config.yaml
├── .python-version
├── AGENTS.md
├── fnox.toml
├── pyproject.toml
└── uv.lock
```

The `data-etl` archetype created `src/my_pipeline/pipeline.py` and a matching test.

## Run the pipeline

```bash
cd my-pipeline
uv run python -m my_pipeline.pipeline
```

Or use `uv run` with a script entry point once you add one.

## Explore the starter code

Open `src/my_pipeline/pipeline.py` and `src/my_pipeline/etl_utils.py`. They contain small starter functions using `polars`.

## Run the tests

```bash
cd my-pipeline
uv run pytest
```

## Add the data-etl profile

Add the `data-etl` profile to include `polars` + `pyarrow` and a starter `etl_utils.py`:

```toml
archetype = "data-etl"
profiles = ["data-etl"]
```

Then generate a new project:

```bash
foundry plan --spec my-pipeline.toml --json > my-pipeline-plan.json
foundry generate --spec my-pipeline.toml --plan my-pipeline-plan.json --dest ./my-pipeline-v2
```

Note: the `data-etl` profile depends on `pyarrow`, which may require a working C++ build toolchain on some systems. If `uv lock` or `uv sync` fails, install the system build dependencies for your platform and retry.

## Quality gates

Before finishing work:

```bash
uv run ruff check .
uv run ruff format --check .
uv run ty check
uv run pytest
```

## Next tutorial

- [CLI Tutorial](cli-tutorial.md)
- [Scripts Tutorial](scripts-tutorial.md)
