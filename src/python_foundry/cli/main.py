"""Console entrypoint for the provisional `foundry` binary."""

from __future__ import annotations

import typer

from python_foundry import __version__

app = typer.Typer(
    name="foundry",
    help="python-foundry — validate / plan / generate (PHASE-01 scaffold).",
    no_args_is_help=True,
)


@app.command("version")
def version_cmd() -> None:
    """Print package version (catalog digest lands in PHASE-01)."""
    typer.echo(f"foundry {__version__}")


@app.callback()
def _root() -> None:
    """Root callback."""


def main() -> None:
    app()


if __name__ == "__main__":
    main()
