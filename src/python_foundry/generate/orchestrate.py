"""Generate orchestration: bind/rebuild → stage → render → lock → verify → place."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import cast

from python_foundry.catalog import load_default_catalog
from python_foundry.fsx import create_stage, exclusive_place
from python_foundry.fsx.stage import Stage
from python_foundry.generate.lock import LockError, produce_uv_lock
from python_foundry.plan import (
    GenerationPlan,
    PlanBindError,
    bind_plan,
    rebuild_plan,
)
from python_foundry.render import RenderError, render_plan_into_stage
from python_foundry.spec import load_spec
from python_foundry.spec.models import VerifyMode
from python_foundry.verify import NETWORK_DISCLOSURE, VerifyError, run_verify


@dataclass(slots=True)
class GenerateResult:
    destination: Path
    plan: GenerationPlan
    stage_path: str | None
    verify_mode: str
    verify_source: str
    network_disclosure: str
    placed: bool


class GenerateError(Exception):
    """Generate failure with optional absolute stage_path for reports."""

    def __init__(
        self,
        message: str,
        *,
        error_class: str,
        code: str,
        stage_path: str | None = None,
        verify_mode: str | None = None,
        plan_sha256: str | None = None,
    ) -> None:
        super().__init__(message)
        self.message = message
        self.error_class = error_class
        self.code = code
        self.stage_path = stage_path
        self.verify_mode = verify_mode
        self.plan_sha256 = plan_sha256


def generate(
    *,
    spec_path: str | Path,
    destination: str | Path | None = None,
    plan_path: str | Path | None = None,
    cli_verify: str | None = None,
    run_lock: bool = True,
    run_verify_tools: bool = True,
) -> GenerateResult:
    """Full generate lifecycle (PHASE-03).

    On failure after stage create: stage is preserved; dest untouched; error
    includes absolute stage_path.
    """
    cat = load_default_catalog()
    try:
        spec = load_spec(spec_path)
    except Exception as exc:
        from python_foundry.spec import SpecError

        if isinstance(exc, SpecError):
            raise GenerateError(
                exc.message,
                error_class=exc.error_class,
                code=exc.code,
            ) from exc
        raise

    dest = Path(destination) if destination is not None else Path(spec.destination)
    stage: Stage | None = None
    plan: GenerationPlan | None = None

    try:
        # Plan bind or rebuild (before any stage write).
        if plan_path is not None:
            plan = bind_plan(
                spec=spec,
                catalog=cat,
                plan_artifact=plan_path,
                cli_verify=cli_verify,
            )
        else:
            plan = rebuild_plan(spec=spec, catalog=cat, cli_verify=cli_verify)

        stage = create_stage(dest)
        render_plan_into_stage(plan, spec, stage)

        if run_lock:
            produce_uv_lock(stage.path)

        if run_verify_tools:
            run_verify(stage.path, cast(VerifyMode, plan.verify_mode))
        elif plan.verify_mode != "none":
            # Structural mode for tests: skip heavy tools when requested.
            pass

        placed_path = exclusive_place(stage, dest)
        return GenerateResult(
            destination=placed_path,
            plan=plan,
            stage_path=None,
            verify_mode=plan.verify_mode,
            verify_source=plan.verify_source,
            network_disclosure=NETWORK_DISCLOSURE,
            placed=True,
        )
    except PlanBindError as exc:
        raise GenerateError(
            exc.message,
            error_class=exc.error_class,
            code=exc.code,
            plan_sha256=plan.plan_sha256 if plan else None,
        ) from exc
    except RenderError as exc:
        raise GenerateError(
            exc.message,
            error_class=exc.error_class,
            code=exc.code,
            stage_path=stage.absolute_path if stage else None,
            plan_sha256=plan.plan_sha256 if plan else None,
        ) from exc
    except LockError as exc:
        raise GenerateError(
            exc.message,
            error_class=exc.error_class,
            code=exc.code,
            stage_path=exc.stage_path or (stage.absolute_path if stage else None),
            plan_sha256=plan.plan_sha256 if plan else None,
            verify_mode=plan.verify_mode if plan else None,
        ) from exc
    except VerifyError as exc:
        raise GenerateError(
            exc.message,
            error_class=exc.error_class,
            code=exc.code,
            stage_path=exc.stage_path or (stage.absolute_path if stage else None),
            plan_sha256=plan.plan_sha256 if plan else None,
            verify_mode=exc.verify_mode or (plan.verify_mode if plan else None),
        ) from exc
    except Exception as exc:
        from python_foundry.fsx import FsxError

        if isinstance(exc, FsxError):
            raise GenerateError(
                exc.message,
                error_class=exc.error_class,
                code=exc.code,
                stage_path=exc.stage_path or (stage.absolute_path if stage else None),
                plan_sha256=plan.plan_sha256 if plan else None,
                verify_mode=plan.verify_mode if plan else None,
            ) from exc
        raise GenerateError(
            str(exc),
            error_class="internal",
            code="generate.internal",
            stage_path=stage.absolute_path if stage else None,
            plan_sha256=plan.plan_sha256 if plan else None,
        ) from exc
