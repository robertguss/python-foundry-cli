"""Text/JSON encoding for success and failure reports."""

from __future__ import annotations

import json
from typing import Any

from python_foundry.plan.canonical import canonical_json_bytes
from python_foundry.plan.models import GenerationPlan
from python_foundry.report.errors import ERROR_CLASSES, ReportError
from python_foundry.spec.models import ProjectSpec


def encode_failure(
    *,
    error_class: str,
    message: str,
    stage_path: str | None = None,
    verify_mode: str | None = None,
    plan_sha256: str | None = None,
    code: str | None = None,
) -> dict[str, Any]:
    """Build a JSON failure object with closed error_class (REQ-091)."""
    if error_class not in ERROR_CLASSES:
        allowed = ", ".join(sorted(ERROR_CLASSES))
        raise ReportError(
            f"unknown error_class {error_class!r}; must be one of: {allowed}"
        )
    body: dict[str, Any] = {
        "ok": False,
        "error_class": error_class,
        "message": message,
    }
    if code is not None:
        body["code"] = code
    if stage_path is not None:
        body["stage_path"] = stage_path
    if verify_mode is not None:
        body["verify_mode"] = verify_mode
    if plan_sha256 is not None:
        body["plan_sha256"] = plan_sha256
    return body


def failure_json(**kwargs: Any) -> str:
    """Canonical compact JSON encoding of a failure report."""
    return canonical_json_bytes(encode_failure(**kwargs)).decode("utf-8")


def plan_json(plan: GenerationPlan) -> str:
    """JSON success encoding for a sealed plan (includes plan_sha256)."""
    body = {"ok": True, "plan": plan.body}
    return canonical_json_bytes(body).decode("utf-8")


def plan_text(plan: GenerationPlan) -> str:
    """Human-readable plan summary for operators (default CLI output)."""
    lines = [
        "foundry plan",
        f"  plan_sha256: {plan.plan_sha256}",
        f"  foundry: {plan.foundry_version}",
        f"  catalog_digest: {plan.catalog_digest}",
        f"  verify: {plan.verify_mode} (source={plan.verify_source})",
        f"  archetype: {plan.body['resolved']['archetype']['kind']}/"
        f"{plan.body['resolved']['archetype']['id']}",
    ]
    profiles = plan.body["resolved"]["profiles"]
    if profiles:
        refs = ", ".join(f"{p['kind']}/{p['id']}" for p in profiles)
        lines.append(f"  profiles: {refs}")
    else:
        lines.append("  profiles: (none)")
    files = plan.body["files"]
    lines.append(f"  files: {len(files)}")
    for entry in files[:20]:
        owner = entry["owner"]
        lines.append(
            f"    - {entry['path']} [{entry['render']}] "
            f"({owner['kind']}/{owner['id']})"
        )
    if len(files) > 20:
        lines.append(f"    … {len(files) - 20} more")
    warnings = plan.body.get("warnings") or []
    if warnings:
        lines.append("  warnings:")
        for w in warnings:
            lines.append(f"    - {w}")
    return "\n".join(lines) + "\n"


def validate_json(spec: ProjectSpec) -> str:
    """JSON success encoding for validate."""
    body = {
        "ok": True,
        "spec": {
            "name": spec.name,
            "archetype": spec.archetype,
            "destination": spec.destination,
            "profiles": list(spec.profiles),
            "python_version": spec.python_version,
            "verify": spec.verify,
        },
    }
    return canonical_json_bytes(body).decode("utf-8")


def validate_text(spec: ProjectSpec) -> str:
    """Human-readable validate success summary."""
    profiles = ", ".join(spec.profiles) if spec.profiles else "(none)"
    return (
        "foundry validate: ok\n"
        f"  name: {spec.name}\n"
        f"  archetype: {spec.archetype}\n"
        f"  destination: {spec.destination}\n"
        f"  profiles: {profiles}\n"
    )


def failure_text(
    *,
    error_class: str,
    message: str,
    code: str | None = None,
) -> str:
    """Human-readable failure line(s)."""
    if error_class not in ERROR_CLASSES:
        allowed = ", ".join(sorted(ERROR_CLASSES))
        raise ReportError(
            f"unknown error_class {error_class!r}; must be one of: {allowed}"
        )
    head = f"foundry error [{error_class}]"
    if code:
        head += f" ({code})"
    return f"{head}: {message}\n"


def dumps_pretty(obj: dict[str, Any]) -> str:
    """Pretty JSON (non-canonical) for debugging only."""
    return json.dumps(obj, indent=2, sort_keys=True) + "\n"
