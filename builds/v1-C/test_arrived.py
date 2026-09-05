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


class ArrivedC(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.dir = Path(self.tmp.name)

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def py(self, name: str, body: str) -> Path:
        p = self.dir / name
        p.write_text(body, encoding="utf-8")
        return p

    def test_stream_then_arrive(self) -> None:
        hop1 = self.py("hop1.py", "import sys, time\nprint('posted id=42', flush=True)\ntime.sleep(0.6)\n")
        hop2 = self.py("hop2.py", "import sys; print('MIRROR id=' + sys.argv[1])\n")
        r = invoke([
            "--local-cmd", cmdline(PY, hop1),
            "--remote-cmd", cmdline(PY, hop2) + " {id}",
            "--timeout", "8", "--interval", "0.2",
        ])
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertIn("ARRIVED id=42", r.stdout)

    def test_hop1_fail_after_print(self) -> None:
        hop1 = self.py("hop1.py", "print('posted id=42', flush=True)\nraise SystemExit(1)\n")
        hop2 = self.py("hop2.py", "import sys; print('MIRROR id=' + sys.argv[1])\n")
        r = invoke([
            "--local-cmd", cmdline(PY, hop1),
            "--remote-cmd", cmdline(PY, hop2) + " {id}",
            "--timeout", "6",
        ])
        self.assertEqual(r.returncode, 2)

    def test_silent(self) -> None:
        hop1 = self.py("hop1.py", "print('posted id=9', flush=True)\n")
        hop2 = self.py("hop2.py", "print('nope')\n")
        r = invoke([
            "--local-cmd", cmdline(PY, hop1),
            "--remote-cmd", cmdline(PY, hop2),
            "--timeout", "1.0", "--interval", "0.2",
        ])
        self.assertEqual(r.returncode, 4)

    def test_usage(self) -> None:
        r = invoke([])
        self.assertEqual(r.returncode, 64)


if __name__ == "__main__":
    unittest.main()
