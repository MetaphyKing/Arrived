#!/usr/bin/env python3
"""Arrived v1-B — sequential file hop-pair.

Hop-1 must exit 0 and mint an id. Hop-2 is a file polled until that
same id appears in its contents. Silence is failure. Stdlib only.
"""
from __future__ import annotations

import argparse
import os
import re
import shlex
import subprocess
import sys
import time
from pathlib import Path

EX_OK, EX_HOP1, EX_PARSE, EX_SILENT, EX_USAGE = 0, 2, 3, 4, 64
DEFAULT_ID_RE = r"id[=:\s]+(\S+)"


def run_cmd(cmd: str, timeout: float | None) -> subprocess.CompletedProcess[str]:
    if os.name == "nt":
        return subprocess.run(
            cmd, shell=True, capture_output=True, text=True,
            timeout=timeout, encoding="utf-8", errors="replace",
        )
    return subprocess.run(
        shlex.split(cmd), capture_output=True, text=True,
        timeout=timeout, encoding="utf-8", errors="replace",
    )


def parse_id(text: str, pattern: str) -> str | None:
    m = re.search(pattern, text)
    if not m or not m.lastindex:
        return None
    ident = m.group(1)
    return ident or None


def file_shows(path: Path, ident: str, extra: str) -> bool:
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return False
    if ident not in text:
        return False
    if extra and extra not in text:
        return False
    return True


def poll(check, timeout: float, interval: float) -> bool:
    deadline = time.monotonic() + timeout
    while True:
        if check():
            return True
        remain = deadline - time.monotonic()
        if remain <= 0:
            return False
        time.sleep(min(interval, remain))


def parse_args(argv: list[str] | None) -> argparse.Namespace | int:
    ap = argparse.ArgumentParser(prog="arrived", exit_on_error=False)
    ap.add_argument("--local-cmd", required=True)
    ap.add_argument("--id-regex", default=DEFAULT_ID_RE)
    ap.add_argument("--remote-file", required=True)
    ap.add_argument("--expect", default="")
    ap.add_argument("--timeout", type=float, default=15.0)
    ap.add_argument("--interval", type=float, default=0.4)
    try:
        return ap.parse_args(argv)
    except (argparse.ArgumentError, SystemExit):
        return EX_USAGE


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    if isinstance(args, int):
        print("NOT_ARRIVED reason=usage")
        return args
    try:
        hop1 = run_cmd(args.local_cmd, timeout=max(args.timeout, 30.0))
    except subprocess.TimeoutExpired:
        print("NOT_ARRIVED reason=hop1_timeout")
        return EX_HOP1
    except (OSError, ValueError):
        print("NOT_ARRIVED reason=hop1_os")
        return EX_HOP1
    if hop1.returncode != 0:
        print("NOT_ARRIVED reason=hop1_exit")
        return EX_HOP1
    ident = parse_id((hop1.stdout or "") + (hop1.stderr or ""), args.id_regex)
    if not ident:
        print("NOT_ARRIVED reason=id_unparseable")
        return EX_PARSE
    path = Path(args.remote_file)
    extra = args.expect
    ok = poll(lambda: file_shows(path, ident, extra), args.timeout, args.interval)
    if not ok:
        print("NOT_ARRIVED reason=hop2_silent id=%s" % ident)
        return EX_SILENT
    print("ARRIVED id=%s hop2=file" % ident)
    return EX_OK


if __name__ == "__main__":
    raise SystemExit(main())
