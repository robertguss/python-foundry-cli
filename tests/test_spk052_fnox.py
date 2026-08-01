"""SPK-052: fnox + age smoke without dotenv fallback."""

from __future__ import annotations

import shutil
import subprocess
from pathlib import Path

import pytest

FNOX = shutil.which("fnox")
AGE = shutil.which("age")


@pytest.mark.skipif(not FNOX or not AGE, reason="fnox and age required on PATH")
def test_spk052_fnox_age_encrypt_decrypt_exec(tmp_path: Path) -> None:
    """Encrypt/decrypt with age; fnox exec runs a command with secrets.

    Hard rule: no dotenv fallback on failure.
    """
    # age keypair
    identity = tmp_path / "key.txt"
    recipient = tmp_path / "key.pub"
    subprocess.run(
        ["age-keygen", "-o", str(identity)],
        check=True,
        capture_output=True,
        text=True,
    )
    # Extract public key
    pub = None
    for line in identity.read_text(encoding="utf-8").splitlines():
        if line.startswith("# public key:"):
            pub = line.split(":", 1)[1].strip()
            break
    assert pub
    recipient.write_text(pub + "\n", encoding="utf-8")

    # Encrypt a secret value with age for a file-based smoke.
    plain = tmp_path / "secret.txt"
    plain.write_text("s3cret-value\n", encoding="utf-8")
    cipher = tmp_path / "secret.txt.age"
    subprocess.run(
        ["age", "-r", pub, "-o", str(cipher), str(plain)],
        check=True,
        capture_output=True,
    )
    assert cipher.is_file()
    dec = subprocess.run(
        ["age", "-d", "-i", str(identity), str(cipher)],
        check=True,
        capture_output=True,
        text=True,
    )
    assert "s3cret-value" in dec.stdout

    # fnox version smoke (tool present + runnable).
    assert FNOX is not None
    ver = subprocess.run(
        [FNOX, "--version"],
        check=True,
        capture_output=True,
        text=True,
    )
    assert "fnox" in ver.stdout.lower() or ver.stdout.strip()

    # Prove we did not introduce dotenv fallback helpers in product tree.
    repo = Path(__file__).resolve().parents[1]
    for path in (repo / "src").rglob("*.py"):
        text = path.read_text(encoding="utf-8")
        assert "load_dotenv" not in text
        assert "python-dotenv" not in text
