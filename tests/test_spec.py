"""Unit tests for pure Project Spec parse + validate (python-foundry-cli-hvt)."""

from __future__ import annotations

import io
from pathlib import Path

import pytest

from python_foundry.spec import (
    DEFAULT_PYTHON_VERSION,
    STDIN_SPEC,
    ProjectSpec,
    SpecError,
    SpecParseError,
    SpecValidationError,
    load_spec,
    load_spec_stream,
    parse_spec_text,
)

REPO_ROOT = Path(__file__).resolve().parents[1]
MINIMAL_CLI = REPO_ROOT / "examples" / "minimal-cli.toml"


def _minimal(**overrides: object) -> str:
    """Build a minimal-cli-shaped TOML body with optional overrides."""
    fields: dict[str, object] = {
        "schema": 1,
        "name": "example-cli",
        "description": "Minimal cli cell for validate/plan goldens",
        "archetype": "cli",
        "destination": "./example-cli",
        "profiles": [],
    }
    fields.update(overrides)
    lines: list[str] = []
    for key, value in fields.items():
        if value is _MISSING:
            continue
        lines.append(_toml_assign(key, value))
    return "\n".join(lines) + "\n"


class _Missing:
    pass


_MISSING = _Missing()


def _toml_assign(key: str, value: object) -> str:
    if isinstance(value, bool):
        return f"{key} = {'true' if value else 'false'}"
    if isinstance(value, int):
        return f"{key} = {value}"
    if isinstance(value, str):
        escaped = value.replace("\\", "\\\\").replace('"', '\\"')
        return f'{key} = "{escaped}"'
    if isinstance(value, list):
        inner = ", ".join(
            f'"{item}"' if isinstance(item, str) else str(item) for item in value
        )
        return f"{key} = [{inner}]"
    raise TypeError(f"unsupported TOML test value type: {type(value)!r}")


# ---------------------------------------------------------------------------
# Happy path
# ---------------------------------------------------------------------------


def test_parse_minimal_cli_example_fixture() -> None:
    """Ship examples/minimal-cli.toml must validate as the PHASE-01 golden cell."""
    text = MINIMAL_CLI.read_text(encoding="utf-8")
    spec = parse_spec_text(text, source=str(MINIMAL_CLI))
    assert isinstance(spec, ProjectSpec)
    assert spec.schema == 1
    assert spec.name == "example-cli"
    assert spec.archetype == "cli"
    assert spec.destination == "./example-cli"
    assert spec.profiles == ()
    assert spec.python_version == DEFAULT_PYTHON_VERSION
    assert spec.verify is None
    assert "Minimal" in (spec.description or "")


def test_load_spec_from_path() -> None:
    spec = load_spec(MINIMAL_CLI)
    assert spec.name == "example-cli"
    assert spec.source == str(MINIMAL_CLI)


def test_load_spec_from_stream() -> None:
    data = MINIMAL_CLI.read_bytes()
    spec = load_spec_stream(io.BytesIO(data), source="<mem>")
    assert spec.archetype == "cli"
    assert spec.source == "<mem>"


def test_load_spec_stdin_dash(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    """REQ-023: path '-' reads the entire stdin stream."""
    payload = MINIMAL_CLI.read_bytes()
    monkeypatch.setattr(
        "python_foundry.spec.parse.sys.stdin",
        io.TextIOWrapper(io.BytesIO(payload), encoding="utf-8"),
    )
    # load_spec uses sys.stdin.buffer — provide a BinaryIO stand-in.
    monkeypatch.setattr(
        "python_foundry.spec.parse.sys.stdin",
        type("S", (), {"buffer": io.BytesIO(payload)})(),
    )
    spec = load_spec(STDIN_SPEC)
    assert spec.name == "example-cli"
    assert spec.source == "<stdin>"
    # No interactive prompts; stdout should stay quiet for pure load.
    captured = capsys.readouterr()
    assert captured.out == ""


def test_optional_fields_and_profiles() -> None:
    text = _minimal(
        profiles=["http", "hooks-hk"],
        python_version="3.12",
        verify="strict",
    )
    spec = parse_spec_text(text)
    assert spec.profiles == ("http", "hooks-hk")
    assert spec.python_version == "3.12"
    assert spec.verify == "strict"


def test_error_class_is_validation() -> None:
    with pytest.raises(SpecError) as excinfo:
        parse_spec_text(_minimal(schema=2))
    assert excinfo.value.error_class == "validation"


# ---------------------------------------------------------------------------
# Invalid suite
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    ("body", "code_substr", "msg_substr"),
    [
        pytest.param(
            _minimal(extra_key="nope") if False else 'schema = 1\nname = "x"\n'
            'archetype = "cli"\ndestination = "./x"\nprofiles = []\nunknown = 1\n',
            "unknown_key",
            "unknown",
            id="unknown_key",
        ),
        pytest.param(
            _minimal(archetype="web-app"),
            "unknown_archetype",
            "archetype",
            id="bad_archetype",
        ),
        pytest.param(
            _minimal(profiles=["http", "http"]),
            "duplicate_profile",
            "duplicate",
            id="duplicate_profiles",
        ),
        pytest.param(
            _minimal(profiles=["not-a-profile"]),
            "unknown_profile",
            "unknown profile",
            id="unknown_profile",
        ),
        pytest.param(
            'name = "x"\narchetype = "cli"\ndestination = "./x"\nprofiles = []\n',
            "missing_field",
            "schema",
            id="missing_schema",
        ),
        pytest.param(
            'schema = 1\narchetype = "cli"\ndestination = "./x"\nprofiles = []\n',
            "missing_field",
            "name",
            id="missing_name",
        ),
        pytest.param(
            _minimal(name=""),
            "empty_field",
            "name",
            id="empty_name",
        ),
        pytest.param(
            _minimal(schema=2),
            "unsupported_schema",
            "supported",
            id="unsupported_schema",
        ),
        pytest.param(
            _minimal(verify="turbo"),
            "verify_mode",
            "verify",
            id="bad_verify",
        ),
        pytest.param(
            _minimal(python_version="3.10"),
            "python_version",
            "python_version",
            id="python_below_floor",
        ),
        pytest.param(
            _minimal(profiles="http"),
            "profiles_type",
            "array",
            id="profiles_not_array",
        ),
        pytest.param(
            "schema = 1\nthis is not valid toml {{{\n",
            "toml",
            "TOML",
            id="invalid_toml",
        ),
    ],
)
def test_invalid_suite(body: str, code_substr: str, msg_substr: str) -> None:
    with pytest.raises(SpecError) as excinfo:
        parse_spec_text(body)
    err = excinfo.value
    assert isinstance(err, SpecParseError | SpecValidationError)
    assert code_substr in err.code
    assert msg_substr.lower() in err.message.lower()


def test_secret_material_in_description_rejected() -> None:
    """REQ-022: secrets-looking content in free-text fields hard-fails."""
    pem = (
        "-----BEGIN PRIVATE KEY-----\\n"
        "MIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQC\\n"
        "-----END PRIVATE KEY-----"
    )
    body = _minimal(description=f"leaked key {pem}")
    with pytest.raises(SpecValidationError) as excinfo:
        parse_spec_text(body)
    assert excinfo.value.code == "spec.secret_material"
    assert "secret" in excinfo.value.message.lower()


def test_secret_api_key_assignment_rejected() -> None:
    body = _minimal(description="api_key = sk-abcdefghijklmnopqrstuvwxyz123456")
    with pytest.raises(SpecValidationError) as excinfo:
        parse_spec_text(body)
    assert excinfo.value.code == "spec.secret_material"


def test_missing_path_raises_parse_error(tmp_path: Path) -> None:
    missing = tmp_path / "nope.toml"
    with pytest.raises(SpecParseError) as excinfo:
        load_spec(missing)
    assert excinfo.value.code == "spec.read"


def test_load_spec_does_not_write(tmp_path: Path) -> None:
    """No FS side effects beyond reading the spec path."""
    spec_path = tmp_path / "cell.toml"
    spec_path.write_text(_minimal(), encoding="utf-8")
    before = {p.name: p.stat().st_mtime_ns for p in tmp_path.iterdir()}
    load_spec(spec_path)
    after = {p.name: p.stat().st_mtime_ns for p in tmp_path.iterdir()}
    assert before == after
    assert list(tmp_path.iterdir()) == [spec_path]
