#!/usr/bin/env python3
"""Arrived v2 — hop-pair CLI (combined).

Hop-1 must mint an identifier. Hop-2 (a command and/or a file) must
echo that same identifier. Silence is failure. Stdlib only. No [OK].

--remote-cmd and --remote-file: at least one required.
--stream: parse id from hop-1 stdout before hop-1 exits (v1-C/D).
Default is sequential (v1-A/B).
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
    return m.group(1) or None


def cmd_shows(cmd: str, ident: str, extra: str) -> bool:
    try:
        p = run_cmd(cmd.replace("{id}", ident), timeout=30)
    except (subprocess.TimeoutExpired, OSError, ValueError):
        return False
    out = (p.stdout or "") + (p.stderr or "")
    if ident not in out:
        return False
    return (not extra) or extra in out


def file_shows(path: Path, ident: str, extra: str) -> bool:
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return False
    if ident not in text:
        return False
    return (not extra) or extra in text


def hop2_ok(args: argparse.Namespace, ident: str) -> bool:
    extra = args.expect
    checks = []
    if args.remote_cmd:
        checks.append(cmd_shows(args.remote_cmd, ident, extra))
    if args.remote_file:
        checks.append(file_shows(Path(args.remote_file), ident, extra))
    return bool(checks) and all(checks)


def poll(check, timeout: float, interval: float) -> bool:
    deadline = time.monotonic() + timeout
    while True:
        if check():
            return True
        remain = deadline - time.monotonic()
        if remain <= 0:
            return False
        time.sleep(min(interval, remain))


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
    ap.add_argument("--remote-cmd", default="")
    ap.add_argument("--remote-file", default="")
    ap.add_argument("--expect", default="")
    ap.add_argument("--timeout", type=float, default=15.0)
    ap.add_argument("--interval", type=float, default=0.4)
    ap.add_argument("--stream", action="store_true")
    try:
        args = ap.parse_args(argv)
    except (argparse.ArgumentError, SystemExit):
        return EX_USAGE
    if not args.remote_cmd and not args.remote_file:
        return EX_USAGE
    return args


def hop2_label(args: argparse.Namespace) -> str:
    parts = []
    if args.remote_cmd:
        parts.append("command")
    if args.remote_file:
        parts.append("file")
    return "+".join(parts) or "none"


def sequential(args: argparse.Namespace) -> int:
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
    if not poll(lambda: hop2_ok(args, ident), args.timeout, args.interval):
        print("NOT_ARRIVED reason=hop2_silent id=%s" % ident)
        return EX_SILENT
    print("ARRIVED id=%s hop2=%s" % (ident, hop2_label(args)))
    return EX_OK


def streaming(args: argparse.Namespace) -> int:
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
    seen = False
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
        if ident and not seen:
            seen = hop2_ok(args, ident)
        if seen and proc.poll() is not None:
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
    if not seen:
        remain = max(0.0, deadline - time.monotonic())
        seen = poll(lambda: hop2_ok(args, ident), remain, args.interval)
    if not seen:
        print("NOT_ARRIVED reason=hop2_silent id=%s" % ident)
        return EX_SILENT
    print("ARRIVED id=%s hop2=%s" % (ident, hop2_label(args)))
    return EX_OK


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    if isinstance(args, int):
        print("NOT_ARRIVED reason=usage")
        return args
    return streaming(args) if args.stream else sequential(args)


if __name__ == "__main__":
    raise SystemExit(main())
