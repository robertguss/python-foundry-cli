# Tutorial: Build a CLI Project

This tutorial walks through creating a Typer-based CLI project with `foundry`, reviewing the plan, and binding it at generate time.

## Goals

- Write a Project Spec for a CLI project.
- Validate it and review the Generation Plan.
- Generate the project with plan binding.
- Inspect the generated files.

## Create the spec

Create `my-greeter.toml`:

```toml
schema = 1
name = "my-greeter"
description = "A small CLI greeter"
archetype = "cli"
destination = "./my-greeter"
profiles = ["http"]
python_version = "3.13"
verify = "strict"
```

This selects the `cli` archetype and adds the `http` profile so the project includes `httpx` and a starter HTTP client.

## Validate and plan

```bash
foundry validate --spec my-greeter.toml
foundry plan   --spec my-greeter.toml --json > my-greeter-plan.json
```

Open `my-greeter-plan.json`. It contains:

- The resolved archetype and profiles.
- Every file that will be written.
- The external steps `generate` will run: `uv lock`, `uv sync --locked`, `ruff check .`, `ruff format --check .`, `ty check`, and `pytest` (because `verify = "strict"`).
- The `plan_sha256` digest.

## Generate with plan binding

```bash
foundry generate --spec my-greeter.toml --plan my-greeter-plan.json --dest ./my-greeter
```

Because `--plan` is provided, `generate` hard-fails if the spec, catalog digest, or foundry version changed since you created the plan.

## Inspect the result

```bash
cd my-greeter
find . -type f | sort
```

You should see:

```text
my-greeter/
├── src/
│   └── my_greeter/
│       ├── __init__.py
│       ├── cli.py
│       └── http_client.py
├── tests/
│   └── test_version.py
├── .agents/
│   └── skills/
│       ├── add-cli-command/SKILL.md
│       ├── quality-gates/SKILL.md
│       └── secrets-fnox/SKILL.md
├── .github/
│   └── workflows/
│       └── ci.yml
├── .gitignore
├── .pre-commit-config.yaml
├── .python-version
├── AGENTS.md
├── fnox.toml
├── pyproject.toml
└── uv.lock
```

## Run the project

The generated `pyproject.toml` declares a console script named after the project. For `name = "my-greeter"`, the command is:

```bash
cd my-greeter
uv run my-greeter --help
uv run pytest
```

## Adding a command

Open `src/my_greeter/cli.py` and add a new `typer` command. Then run the quality gates:

```bash
uv run ruff check .
uv run ruff format --check .
uv run ty check
uv run pytest
```

## Next tutorial

- [Scripts Tutorial](scripts-tutorial.md)
- [Data/ETL Tutorial](data-etl-tutorial.md)
