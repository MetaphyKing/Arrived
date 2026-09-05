#!/usr/bin/env python3
from __future__ import annotations

import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
PY = sys.executable
SCRIPT = HERE / "arrived.py"


def q(p: str) -> str:
    p = str(p)
    if os.name == "nt" and any(c in p for c in ' \t"'):
        return '"' + p.replace('"', '\\"') + '"'
    return p


def cmdline(*parts: object) -> str:
    return " ".join(q(str(p)) for p in parts)


def invoke(args: list[str], timeout: float = 25.0) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [PY, str(SCRIPT), *args],
        capture_output=True, text=True, timeout=timeout,
        encoding="utf-8", errors="replace",
    )


class ArrivedD(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.dir = Path(self.tmp.name)

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def py(self, name: str, body: str) -> Path:
        p = self.dir / name
        p.write_text(body, encoding="utf-8")
        return p

    def test_stream_file(self) -> None:
        remote = self.dir / "far.log"
        remote.write_text("MIRROR id=42\n", encoding="utf-8")
        hop1 = self.py("hop1.py", "import time\nprint('posted id=42', flush=True)\ntime.sleep(0.5)\n")
        r = invoke([
            "--local-cmd", cmdline(PY, hop1),
            "--remote-file", str(remote),
            "--timeout", "8", "--interval", "0.2",
        ])
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertIn("ARRIVED id=42 hop2=file", r.stdout)
        self.assertNotIn("[OK]", r.stdout)

    def test_stale_other_id(self) -> None:
        remote = self.dir / "far.log"
        remote.write_text("MIRROR id=1\n", encoding="utf-8")
        hop1 = self.py("hop1.py", "print('posted id=99', flush=True)\n")
        r = invoke([
            "--local-cmd", cmdline(PY, hop1),
            "--remote-file", str(remote),
            "--timeout", "1.0", "--interval", "0.2",
        ])
        self.assertEqual(r.returncode, 4)

    def test_hop1_fail(self) -> None:
        hop1 = self.py("hop1.py", "raise SystemExit(1)\n")
        r = invoke(["--local-cmd", cmdline(PY, hop1), "--remote-file", str(self.dir / "x")])
        self.assertEqual(r.returncode, 2)

    def test_usage(self) -> None:
        r = invoke([])
        self.assertEqual(r.returncode, 64)


if __name__ == "__main__":
    unittest.main()
