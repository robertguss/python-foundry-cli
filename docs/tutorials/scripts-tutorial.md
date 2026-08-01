# Tutorial: Build a Scripts Project

This tutorial creates a scripts-oriented project that uses PEP 723 inline metadata and `uv run`.

## Goals

- Write a `scripts` Project Spec.
- Generate the project.
- Add and run a new script.

## Create the spec

Create `my-tools.toml`:

```toml
schema = 1
name = "my-tools"
description = "A collection of uv-run scripts"
archetype = "scripts"
destination = "./my-tools"
profiles = []
python_version = "3.13"
verify = "strict"
```

## Validate, plan, and generate

```bash
foundry validate --spec my-tools.toml
foundry plan   --spec my-tools.toml --json > my-tools-plan.json
foundry generate --spec my-tools.toml --plan my-tools-plan.json --dest ./my-tools
```

## Inspect the generated project

```bash
cd my-tools
find . -type f | sort
```

```text
my-tools/
├── scripts/
│   └── hello.py
├── tests/
│   └── test_hello_script.py
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

The `scripts/` directory holds PEP 723 scripts. Each script carries its own dependency metadata in a comment block at the top, so `uv run scripts/hello.py` works without installing the project as a package.

## Run the starter script

```bash
cd my-tools
uv run scripts/hello.py
```

## Add your own script

Create `scripts/fetch.py` with PEP 723 metadata:

```python
# /// script
# dependencies = [
#   "httpx>=0.27,<1",
# ]
# ///

import httpx

url = "https://api.github.com"
response = httpx.get(url)
print(response.status_code)
print(response.json()["current_user_url"])
```

Run it:

```bash
uv run scripts/fetch.py
```

## Write a test

Add a test in `tests/test_fetch_script.py` that imports from the script or tests its behavior. Then run:

```bash
uv run pytest
```

## Quality gates

Before finishing work, run the generated project’s DoD gates:

```bash
uv run ruff check .
uv run ruff format --check .
uv run ty check
uv run pytest
```

## Next tutorial

- [CLI Tutorial](cli-tutorial.md)
- [Data/ETL Tutorial](data-etl-tutorial.md)
