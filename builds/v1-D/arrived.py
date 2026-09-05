#!/usr/bin/env python3
"""Arrived v1-D — streaming file hop-pair.

Parse id from hop-1 stdout as it arrives; poll a file for that id
before hop-1 exits. Hop-1 must still exit 0. Stdlib only.
"""
from __future__ import annotations

import argparse
import os
import queue
import re
import shlex
import subprocess
import sys
import threading
import time
from pathlib import Path

EX_OK, EX_HOP1, EX_PARSE, EX_SILENT, EX_USAGE = 0, 2, 3, 4, 64
DEFAULT_ID_RE = r"id[=:\s]+(\S+)"


def popen_cmd(cmd: str) -> subprocess.Popen[str]:
    if os.name == "nt":
        return subprocess.Popen(
            cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
            text=True, encoding="utf-8", errors="replace",
        )
    return subprocess.Popen(
        shlex.split(cmd), stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
        text=True, encoding="utf-8", errors="replace",
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


def pump(proc: subprocess.Popen[str], q: queue.Queue[str | None]) -> None:
    try:
        assert proc.stdout is not None
        for line in proc.stdout:
            q.put(line)
    finally:
        q.put(None)


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
        proc = popen_cmd(args.local_cmd)
    except (OSError, ValueError):
        print("NOT_ARRIVED reason=hop1_os")
        return EX_HOP1
    q: queue.Queue[str | None] = queue.Queue()
    threading.Thread(target=pump, args=(proc, q), daemon=True).start()
    deadline = time.monotonic() + max(args.timeout, 0.2)
    acc: list[str] = []
    ident: str | None = None
    hop2_ok = False
    extra = args.expect
    path = Path(args.remote_file)
    ended = False
    while time.monotonic() < deadline:
        try:
            item = q.get(timeout=min(args.interval, 0.2))
        except queue.Empty:
            item = "EMPTY"
        if item is None:
            ended = True
        elif item != "EMPTY":
            acc.append(item)
            if ident is None:
                ident = parse_id("".join(acc), args.id_regex)
        if ident and not hop2_ok:
            hop2_ok = file_shows(path, ident, extra)
        if hop2_ok and proc.poll() is not None:
            break
        if ended and proc.poll() is not None:
            break
    if proc.poll() is None:
        proc.kill()
        proc.wait(timeout=5)
        print("NOT_ARRIVED reason=hop1_timeout")
        return EX_HOP1
    if proc.returncode != 0:
        print("NOT_ARRIVED reason=hop1_exit")
        return EX_HOP1
    if ident is None:
        ident = parse_id("".join(acc), args.id_regex)
    if not ident:
        print("NOT_ARRIVED reason=id_unparseable")
        return EX_PARSE
    if not hop2_ok:
        remain = max(0.0, deadline - time.monotonic())
        t0 = time.monotonic()
        while time.monotonic() - t0 < remain:
            if file_shows(path, ident, extra):
                hop2_ok = True
                break
            time.sleep(args.interval)
    if not hop2_ok:
        print("NOT_ARRIVED reason=hop2_silent id=%s" % ident)
        return EX_SILENT
    print("ARRIVED id=%s hop2=file" % ident)
    return EX_OK


if __name__ == "__main__":
    raise SystemExit(main())
