# Quickstart

This guide gets you from zero to a generated Python project in a few minutes.

## What you need

- **Python** 3.13 or newer.
- **uv** installed and on your `PATH`.
- A terminal on macOS or Linux.

`foundry` does not support Windows.

## Install

`python-foundry` is a normal Python package. Run it from this repository:

```bash
uv sync
uv run foundry version
```

Once the package is published, you can also install it with:

```bash
uv tool install python-foundry
```

## Create your first Project Spec

A Project Spec is a small TOML file that declares what you want to build. Save this as `my-cli.toml`:

```toml
schema = 1
name = "my-cli"
description = "My first foundry CLI project"
archetype = "cli"
destination = "./my-cli"
profiles = ["http"]
python_version = "3.13"
```

## Validate, plan, and generate

Run the pipeline:

```bash
foundry validate --spec my-cli.toml
foundry plan   --spec my-cli.toml --json > my-cli-plan.json
foundry generate --spec my-cli.toml --plan my-cli-plan.json --dest ./my-cli
```

What happened:

1. `validate` checks that the spec is well-formed and every profile/archetype exists.
2. `plan` builds a Generation Plan (a JSON contract) without touching the filesystem.
3. `generate` writes the project to `./my-cli`, refreshes `uv.lock`, and runs the default verify tier.

## Inspect the result

```bash
cd my-cli
ls -la
```

You will see a complete project: `pyproject.toml`, source package, tests, GitHub Actions, pre-commit config, agent rules, and a committed `uv.lock`.

## Run the generated project

```bash
cd my-cli
uv run ruff check .
uv run pytest
```

Your project is ready to develop.

## Next steps

- Read the full [User Guide](user-guide.md).
- Browse the [example specs](../examples/).
- Learn about each archetype and profile in [Archetypes and Profiles](archetypes-and-profiles.md).
