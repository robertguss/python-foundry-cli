"""Construct an immutable Generation Plan (pure; no FS / clock / random)."""

from __future__ import annotations

import json
from typing import Any

from python_foundry import __version__
from python_foundry.catalog.load import Catalog
from python_foundry.plan.canonical import (
    canonical_json_bytes,
    content_digest,
    sha256_hex,
)
from python_foundry.plan.models import GenerationPlan
from python_foundry.resolve.compose import resolve
from python_foundry.resolve.verify import resolve_effective_verify
from python_foundry.spec.models import ProjectSpec

PLAN_SCHEMA = 1


def construct(
    spec: ProjectSpec,
    catalog: Catalog,
    *,
    cli_verify: str | None = None,
    foundry_version: str | None = None,
    warnings: list[str] | None = None,
) -> GenerationPlan:
    """Build a sealed Generation Plan from pure inputs (REQ-024..026).

    Purity: does not import or call fsx / generate / cli. No wall-clock or
    random values enter the plan body (RSK-100).
    """
    version = foundry_version if foundry_version is not None else __version__
    resolved = resolve(spec, catalog)
    effective = resolve_effective_verify(
        cli_verify=cli_verify,
        toml_verify=spec.verify,
    )

    # Membership list is sorted so TOML profile array order cannot affect the
    # plan body (FND-002). Resolved profiles remain catalog apply order.
    membership = tuple(sorted(spec.profiles))

    files: list[dict[str, Any]] = []
    for planned in resolved.files:
        # Stub content identity: digest of owner-qualified source path until
        # real template bodies land (PHASE-03/04). Deterministic, no I/O.
        stub_payload = f"{planned.owner_ref}:{planned.source}".encode()
        files.append(
            {
                "path": planned.path,
                "mode": planned.mode,
                "render": planned.render,
                "content_digest": content_digest(stub_payload),
                "owner": {"kind": planned.owner_kind, "id": planned.owner_id},
            }
        )
    files.sort(key=lambda f: str(f["path"]))

    body_without_hash: dict[str, Any] = {
        "schema": PLAN_SCHEMA,
        "foundry": {"version": version},
        "catalog_digest": catalog.digest,
        "specification": {
            "name": spec.name,
            "description": spec.description,
            "archetype": spec.archetype,
            "destination": spec.destination,
            "profiles": list(membership),
            "python_version": spec.python_version,
            "verify": spec.verify,
        },
        "resolved": {
            "archetype": {"kind": "archetype", "id": resolved.archetype},
            "profiles": [
                {"kind": "profile", "id": pid} for pid in resolved.profiles
            ],
            "units": [
                {"kind": u.kind, "id": u.id} for u in resolved.units
            ],
        },
        "files": files,
        "dependencies": [],
        "lock": {
            "produce": True,
            "tool": "uv",
            "artifact": "uv.lock",
        },
        "external_steps": _external_steps_for(effective.mode),
        "verify_mode": effective.mode,
        "verify_source": effective.source,
        "warnings": list(warnings or ()),
    }

    preimage = canonical_json_bytes(body_without_hash)
    digest = sha256_hex(preimage)

    full_body = dict(body_without_hash)
    full_body["plan_sha256"] = digest
    # Re-canonicalize full body for stable on-disk / equality encoding.
    full_bytes = canonical_json_bytes(full_body)
    sealed: dict[str, Any] = json.loads(full_bytes.decode("utf-8"))

    return GenerationPlan(
        body=sealed,
        plan_sha256=digest,
        preimage=preimage,
    )


def _external_steps_for(mode: str) -> list[dict[str, Any]]:
    """Declare intended verify/lock steps (runners execute later)."""
    steps: list[dict[str, Any]] = [
        {
            "id": "uv_lock",
            "argv": ["uv", "lock"],
            "when": "always",
        },
    ]
    if mode == "none":
        return steps
    steps.extend(
        [
            {
                "id": "uv_sync_locked",
                "argv": ["uv", "sync", "--locked"],
                "when": "default_or_strict",
            },
            {
                "id": "ruff_check",
                "argv": ["uv", "run", "ruff", "check", "."],
                "when": "default_or_strict",
            },
            {
                "id": "ruff_format_check",
                "argv": ["uv", "run", "ruff", "format", "--check", "."],
                "when": "default_or_strict",
            },
            {
                "id": "ty_check",
                "argv": ["uv", "run", "ty", "check"],
                "when": "default_or_strict",
            },
        ]
    )
    if mode == "strict":
        steps.append(
            {
                "id": "pytest",
                "argv": ["uv", "run", "pytest"],
                "when": "strict",
            }
        )
    return steps
