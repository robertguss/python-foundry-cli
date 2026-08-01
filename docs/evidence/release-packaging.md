# Release packaging path + version/digest

- Console script: `foundry` → `python_foundry.cli.main:main`
- Version: `python_foundry.__version__`
- `foundry version` prints package version **and** catalog digest
- Build: `uv build` / hatchling via project metadata
