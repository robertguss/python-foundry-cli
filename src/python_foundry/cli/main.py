"""Console entrypoint for the provisional ``foundry`` binary."""

from __future__ import annotations

from typing import Annotated, NoReturn

import typer

from python_foundry import __version__
from python_foundry.catalog import CatalogLookupError, load_default_catalog
from python_foundry.plan import construct
from python_foundry.plan.canonical import canonical_json_bytes
from python_foundry.report import (
    failure_json,
    failure_text,
    plan_json,
    plan_text,
    validate_json,
    validate_text,
)
from python_foundry.resolve import ResolveError
from python_foundry.spec import ProjectSpec, SpecError, load_spec

app = typer.Typer(
    name="foundry",
    help="python-foundry — validate / plan / generate (PHASE-01 pure pipeline).",
    no_args_is_help=True,
)

catalog_app = typer.Typer(help="Inspect the closed catalog (kind-qualified).")
app.add_typer(catalog_app, name="catalog")


def _emit_failure(
    *,
    error_class: str,
    message: str,
    code: str | None = None,
    as_json: bool,
    exit_code: int = 1,
) -> NoReturn:
    if as_json:
        typer.echo(
            failure_json(
                error_class=error_class,
                message=message,
                code=code,
            )
        )
    else:
        typer.echo(
            failure_text(error_class=error_class, message=message, code=code),
            err=True,
        )
    raise typer.Exit(exit_code)


def _load_spec_or_fail(spec: str, *, as_json: bool) -> ProjectSpec:
    try:
        return load_spec(spec)
    except SpecError as exc:
        _emit_failure(
            error_class=exc.error_class,
            message=exc.message,
            code=exc.code,
            as_json=as_json,
        )


@app.command("version")
def version_cmd() -> None:
    """Print package version and catalog digest."""
    cat = load_default_catalog()
    typer.echo(f"foundry {__version__}")
    typer.echo(f"catalog_digest {cat.digest}")


@app.command("validate")
def validate_cmd(
    spec: Annotated[
        str,
        typer.Option("--spec", help="Project Spec path, or '-' for stdin."),
    ],
    json_out: Annotated[
        bool,
        typer.Option("--json", help="Machine-readable JSON report."),
    ] = False,
) -> None:
    """Validate a Project Spec (no filesystem writes beyond reading the spec)."""
    project = _load_spec_or_fail(spec, as_json=json_out)
    if json_out:
        typer.echo(validate_json(project))
    else:
        typer.echo(validate_text(project), nl=False)


@app.command("plan")
def plan_cmd(
    spec: Annotated[
        str,
        typer.Option("--spec", help="Project Spec path, or '-' for stdin."),
    ],
    json_out: Annotated[
        bool,
        typer.Option("--json", help="Emit sealed plan JSON."),
    ] = False,
    verify: Annotated[
        str | None,
        typer.Option(
            "--verify",
            help="CLI verify override: default | strict | none (FND-001).",
        ),
    ] = None,
) -> None:
    """Construct and print a Generation Plan (write-free)."""
    project = _load_spec_or_fail(spec, as_json=json_out)
    try:
        cat = load_default_catalog()
        plan = construct(project, cat, cli_verify=verify)
    except ResolveError as exc:
        _emit_failure(
            error_class=exc.error_class,
            message=exc.message,
            code=exc.code,
            as_json=json_out,
        )
    except Exception as exc:  # noqa: BLE001 — map unexpected pure failures
        _emit_failure(
            error_class="internal",
            message=str(exc),
            code="internal.error",
            as_json=json_out,
        )
    if json_out:
        typer.echo(plan_json(plan))
    else:
        typer.echo(plan_text(plan), nl=False)


@catalog_app.command("list")
def catalog_list_cmd(
    json_out: Annotated[
        bool,
        typer.Option("--json", help="Machine-readable JSON list."),
    ] = False,
) -> None:
    """List closed catalog units with kind + id (REQ-087)."""
    cat = load_default_catalog()
    rows = cat.list_units()
    if json_out:
        payload = {
            "ok": True,
            "units": [
                {
                    "kind": r.kind,
                    "id": r.id,
                    "description": r.description,
                    "ref": r.ref,
                }
                for r in rows
            ],
        }
        typer.echo(canonical_json_bytes(payload).decode("utf-8"))
        return
    for row in rows:
        typer.echo(f"{row.kind}/{row.id}\t{row.description}")


@catalog_app.command("show")
def catalog_show_cmd(
    ref: Annotated[
        str,
        typer.Argument(help="Kind-qualified unit ref, e.g. archetype/data-etl."),
    ],
    json_out: Annotated[
        bool,
        typer.Option("--json", help="Machine-readable JSON unit."),
    ] = False,
) -> None:
    """Show one catalog unit by kind-qualified reference."""
    cat = load_default_catalog()
    try:
        unit = cat.show(ref)
    except CatalogLookupError as exc:
        _emit_failure(
            error_class=exc.error_class,
            message=exc.message,
            code=exc.code,
            as_json=json_out,
        )
    if json_out:
        payload = {
            "ok": True,
            "unit": {
                "kind": unit.kind,
                "id": unit.id,
                "description": unit.description,
                "apply_order": unit.apply_order,
                "manifest_path": unit.manifest_path,
                "files": [
                    {
                        "path": f.path,
                        "render": f.render,
                        "source": f.source,
                        "mode": f.mode,
                        "override": f.override,
                    }
                    for f in unit.files
                ],
            },
        }
        typer.echo(canonical_json_bytes(payload).decode("utf-8"))
        return
    typer.echo(f"{unit.kind}/{unit.id}")
    typer.echo(f"  description: {unit.description}")
    typer.echo(f"  apply_order: {unit.apply_order}")
    typer.echo(f"  manifest: {unit.manifest_path}")
    typer.echo(f"  files: {len(unit.files)}")
    for entry in unit.files:
        typer.echo(f"    - {entry.path} [{entry.render}]")


@app.command("generate")
def generate_cmd(
    spec: Annotated[
        str,
        typer.Option("--spec", help="Project Spec path, or '-' for stdin."),
    ],
    dest: Annotated[
        str | None,
        typer.Option("--dest", help="Override destination path."),
    ] = None,
    plan: Annotated[
        str | None,
        typer.Option("--plan", help="Optional plan JSON to bind before stage writes."),
    ] = None,
    verify: Annotated[
        str | None,
        typer.Option("--verify", help="CLI verify override: default|strict|none."),
    ] = None,
    json_out: Annotated[
        bool,
        typer.Option("--json", help="Machine-readable JSON report."),
    ] = False,
) -> None:
    """Stage → lock → verify → exclusive place (PHASE-03)."""
    from python_foundry.generate import GenerateError, generate
    from python_foundry.report import failure_json, failure_text
    from python_foundry.verify import NETWORK_DISCLOSURE

    try:
        result = generate(
            spec_path=spec,
            destination=dest,
            plan_path=plan,
            cli_verify=verify,
        )
    except GenerateError as exc:
        if json_out:
            typer.echo(
                failure_json(
                    error_class=exc.error_class,
                    message=exc.message,
                    code=exc.code,
                    stage_path=exc.stage_path,
                    verify_mode=exc.verify_mode,
                    plan_sha256=exc.plan_sha256,
                )
            )
        else:
            msg = failure_text(
                error_class=exc.error_class,
                message=exc.message,
                code=exc.code,
            )
            if exc.stage_path:
                msg += f"stage_path: {exc.stage_path}\n"
            typer.echo(msg, err=True)
        raise typer.Exit(1) from exc

    if json_out:
        payload = {
            "ok": True,
            "destination": str(result.destination),
            "plan_sha256": result.plan.plan_sha256,
            "verify_mode": result.verify_mode,
            "verify_source": result.verify_source,
            "network_disclosure": result.network_disclosure,
        }
        typer.echo(canonical_json_bytes(payload).decode("utf-8"))
    else:
        typer.echo("foundry generate: ok")
        typer.echo(f"  destination: {result.destination}")
        typer.echo(f"  plan_sha256: {result.plan.plan_sha256}")
        typer.echo(f"  verify: {result.verify_mode} (source={result.verify_source})")
        typer.echo(f"  network: {NETWORK_DISCLOSURE}")


@app.callback()
def _root() -> None:
    """Root callback."""


def main() -> None:
    # Ensure non-interactive default (REQ-013): no prompts from Typer.
    app(standalone_mode=True)


if __name__ == "__main__":
    main()
