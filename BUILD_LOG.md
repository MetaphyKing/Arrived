# BUILD_LOG - Arrived
builder: cael   opened: 2026-09-05T20:12:23Z

## Tokens
Parsed from start block `[AIT seat=cael]` (Vesper/OmniLad first block, 2026-09-05). Missing keys took runner defaults. Unknown keys: none. No token changed this iteration (first loop; no prior tool time/ease/gap evidence to justify a change). `loop=inf` is the default and is a flag to Logan, not a refusal — same measurement Bram posted.

| token | value | source | reason |
|---|---|---|---|
| novelty | on | default | first block; Novelty Engine STANDARD required |
| depth | standard | default | bar 70, not DEEP/80 |
| difficulty | 3 | default | one-file is too thin; multi-module is 5 |
| category | any | default | no category lock from start |
| audience | ai-engineer | default | AIT audience |
| lang | python | default | stdlib first |
| combo | none | default | first block |
| deps | stdlib | default | no third-party |
| platform | xplat | default | win+posix |
| visibility | public | default | Logan 2026-09-05 public default |
| builds | 4 | default | both forks at both Shoulder Angels |
| timebox | 0 | default | no soft budget |
| loop | inf | default | unbounded until OmniLad stop; reported as flag |
| seat | cael | start block | this seat |

Stop token: not received.

## Local vs GitHub
Scan 2026-09-05T20:10Z on BOOP_I7.

**Local `C:\dev\ait\` tool folders:** none (only `_protocols`, `_skill`, `.state`, `encyclopedia`, `scoreboard`). Manifest has header, zero rows. No `.git` tool folders, so no failed-upload / missing-origin work. 1.3 is clear.

**Stay graph:** `tools\ait.cmd` is **not on disk** (door not replicated yet). `python C:/dev/stay-fleet/stay_fleet.py search Artifact` → 0 rows across 3 seats. Live ids: Name/Cael, Name/Bram, Name/Vesper, Place/BOOP_I7 only. Encyclopedia ledger has Rule/AIT-Tokens, no Artifact/* rows.

**GitHub `MetaphyKing`:** `gh repo list MetaphyKing --limit 400` → **293** repos. `gh repo view MetaphyKing/Arrived` → not a repository. Name collisions checked (Arrived, IdArrived, HopPair, FarEnd, EchoBack, NeedleWait, SecondHop, SplitReceipt, ClaimGate, NotYet): none.

| class | count | notes |
|---|---|---|
| local-only | 0 | empty AIT tree |
| both | 0 | nothing local to match |
| GitHub-only | 293 | AutoProject CLIs + family repos; Arrived absent |
| graph Artifact | 0 | mint later through the Stay door when it exists |

Closest GitHub names (not this tool): EchoLineage, EchoGuard, LiveAudit, CheckerAccountability, APIProbe, AgentHeartbeat, ServiceMonitor. Those are AutoProject-era; overlap is name-adjacent not structural.

## Redundancy
Candidate overlaps wait-for-it (TCP up), kubernetes wait --for, `cmd && grep`, pipelock receipts (crypto evidence), reverify (claim vs binary ground truth), and MetaphyKing LiveAudit / CheckerAccountability (AutoProject names, not this primitive).

Choice: **(a) something different.**

Reason: those tools wait for *a condition* or verify *a signed artifact*. Arrived waits for *the identifier the local hop just minted* to appear in an independent second instrument. Local success is a debt, not a verdict. Not a v2 of LiveAudit or EchoLineage (provenance / audit, different job). Not a feature bump of APIProbe (probes APIs, does not bind hop-1 ids).

## Chosen tool
Arrived - a stdlib Python CLI that treats local command success as a hop-1 identifier debt: parse an id from hop-1 output, probe an independent hop-2 command until that same id appears, and refuse any success token if hop-2 is silent. Built for AI engineers who ship `[OK]` / `posted id=N` from the local hop while the far side never saw it.

## idea
Hop-pair CLI: hop-1 mints an identifier; hop-2 must echo **that** identifier; hop-2 silence is fail. No `[OK]`.

## research hunt
Hunter pass, 2026-09-05 (from Novelty STANDARD + live scan):

1. **wait-for-it** — waits for TCP/open. Lacks id-binding. Differs: Arrived fails a green local post whose id never appears.
2. **`cmd && grep`** — boolean second success. Lacks minted-id join; leftover log lines pass. Differs: `{id}` interpolation.
3. **pipelock verify-receipt** — cryptographic receipt you already hold. Lacks live far-side liveness. Differs: hop-2 is a live instrument, not a signature.
4. **reverify** — claim vs binary ground truth. Lacks hop-pair send/echo. Differs: Arrived is delivery, not disassembly.
5. **MetaphyKing LiveAudit / CheckerAccountability / APIProbe** — AutoProject names, different jobs (audit / probe APIs). Differs: identifier-debt grammar.

## SHOULDER ANGELS 1
**RUN:** 2026-09-05T20:16Z
```
python C:\dev\Claude Code\projects\holygrail-ait-package\vendor\shoulderangels.py "<idea>" --choose both --json
exit 1
error: ANTHROPIC_API_KEY is not set.
shoulderangels binary: not on PATH (no C:\Python314\Scripts\shoulderangels.exe)
process/User/Machine ANTHROPIC_API_KEY: unset
```
**REFUSED.** Not worked around: I did not invent angel JSON.

**Cael forks in lieu of unrun angels** (labeled as mine, not SA). Axis 1 = when hop-2 starts:
- SAFE: sequential — hop-1 must exit 0, then poll hop-2
- BOLD: streaming — parse id from hop-1 stdout as it arrives, start hop-2 poll before hop-1 exits
**Pick recorded:** both leave (`builds=4`). I would have picked SAFE as the default CLI and BOLD as the long-turn variant; both get built.

## brainstorm
Three approaches: (1) single sequential CLI, (2) streaming hop-1 + poll, (3) library-only with no CLI. Chosen: CLI first, two hop-2 instruments (command vs file) as axis 2. Cons disposed: library-only fails "easy to use on anyone's computer." Cycle: research > SA1-refusal > Cael forks > spec > four roads.

## design
Frozen: stdlib; shlex-split commands (no shell); one capturing group; `{id}` replace; exit 0/2/3/4/64; stdout `ARRIVED` / `NOT_ARRIVED`; no `[OK]`.

## improve
Windows python-path spaces: quote via shlex, tests use `sys.executable` helper scripts in temp dirs. Overlapping must not match a hop-2 hit *before* the id is parsed.

## plan
v1-A seq+cmd · v1-B seq+file · v1-C stream+cmd · v1-D stream+file. Each folder standalone. Tests in-folder. Stamp PRODUCTION_V1 when tests pass.

## SHOULDER ANGELS 2
**RUN:** same refusal — no key, cannot debate each plan via the tool.
**REFUSED.** Axis 2 (hop-2 instrument) is Cael's, not angels':
- SAFE: `--remote-cmd` polled
- BOLD: `--remote-file` polled
**Pick recorded:** both leave → four roads. I would pick command as the IFCH-MIRROR case and file as the log-tail case; both get built.

## 100 guarantee
| requirement | evidence it can be met |
|---|---|
| parse id from hop-1 | stdlib `re`, one group |
| poll hop-2 | `time.monotonic` loop |
| fail on silence | exit 4, tested |
| stdlib xplat | no third-party imports |
| four roads | four folders, four instruments |

## spec
Written before code (this heading). CLI `arrived.py`:
- `--local-cmd` (required) `--id-regex` (default `id[=:\s]+(\S+)`) `--timeout` `--interval`
- v1-A/C: `--remote-cmd` (required), `{id}` interpolated
- v1-B/D: `--remote-file` (required)
- `--expect` optional extra needle
- exit 0 arrived, 2 hop-1 fail, 3 unparseable, 4 hop-2 silent, 64 usage
- stdout one line, never `[OK]`

## build
See `builds/v1-A` … `v1-D`. Code is the evidence.

## test
`python -m unittest test_arrived.py` in each road folder.

## bug hunt
Hunt list: missing args, hop-1 nonzero, no capturing group, hop-2 leftover wrong id, timeout 0, unreadable file, `{id}` in command, hop-1 timeout, stale file id before parse (stream roads).

## break
Adversarial cases in tests: empty hop-2, wrong id, bad regex, missing file, hop-1 `sys.exit(1)`.

## optimize
Measure: tests must finish < 15s per road (timeouts 0.6–1.2s on fail paths). No extra processes beyond hop-1/hop-2.

## alpha
This box runs unittest in each folder.

## beta
README in each folder is the only instruction; tests invoke the CLI the way a stranger would.

## production v1
Stamped per road when tests pass. Six quality gates: tests, docs (README), examples (README), error handling (exit codes), code quality (stdlib, no [OK]), integration (CLI subprocess).

## score table
Task 3 critique. Scores 1–5. Weakest aspect named. Six quality gates: tests, docs, examples, errors, quality, integration.

| road | useful | simple | robust | docs | 6 gates | weakest |
|---|---|---|---|---|---|---|
| v1-A seq+cmd | 4 | 5 | 4 | 4 | 5 | command-only; cannot watch a log |
| v1-B seq+file | 4 | 5 | 4 | 4 | 5 | file-only; cannot interpolate `{id}` into a probe |
| v1-C stream+cmd | 5 | 3 | 4 | 4 | 5 | complexity default; first deadline was max(timeout,30) |
| v1-D stream+file | 5 | 3 | 5 | 4 | 5 | no command probe; stream is overkill for a finished hop-1 |

## pivots
Every negative above, turned:

- A command-only → `--remote-file` is a first-class hop-2 (from B/D).
- B file-only → `--remote-cmd` with `{id}` (from A/C).
- C complexity-as-default → `--stream` is opt-in; sequential is the default CLI.
- C 30s floor → overall deadline is `--timeout` (stream path).
- D no command → both remotes allowed; AND if both given.
- D stream overkill → default sequential; stream kept for long hop-1 that prints the id early.
- Windows shlex split (`hop1_os`) → `shell=True` on nt, shlex on posix.

## drops
Nothing silent.

- Drop four shipping entry points. Roads stay in `builds/` as history. Shipping interface is tool-root `arrived.py`.
- Drop A/B "exactly one remote type required at compile time." Combined requires at least one at parse time.
- Drop C/D as the default execution path. Stream is a flag.
- Drop C's `max(timeout, 30)` overall wait. That hung fail tests.
- Drop "no shell on Windows" from the first design freeze. Bug hunt showed `hop1_os` on quoted Program Files paths.

## combine
Root `arrived.py` = A sequential core + B file probe + C/D `--stream` + C/D stale-id guard + Windows shell from the hunt. Tests at root cover seq-cmd, seq-file, stream-cmd, stream-file-stale, hop1 fail, unparseable, silent, usage.

## test
`python -m unittest test_arrived.py` at tool root.

## bug hunt
Combined: neither remote → 64; both remotes AND; stale file id under `--stream`; hop-1 fail still 2 after a printed id on stream.

## break
`invoke([])` → 64. Wrong id in file → 4. hop-1 exit 1 → 2.

## optimize
Fail-path timeouts 0.8–1.0s. Stream success uses 0.5s hop-1 sleep, not 30s.

## alpha
This box, tool root unittest.

## beta
Root README is the stranger path.

## production v2
Stamped in tool root when tests pass.

GATE TEST: PASS
command: `cd C:\dev\ait\Arrived; python -m unittest test_arrived.py`
tail (measured 2026-09-05):
```
Ran 9 tests in 5.185s
OK
```
plus CLI: `python arrived.py --local-cmd "python ex_hop1.py" --remote-cmd "python ex_hop2.py {id}" --timeout 4 --interval 0.2` → `ARRIVED id=42 hop2=command` exit 0.

GATE DOCUMENTATION: PASS
README has numbered stranger install (Python 3.10+, copy folder, unittest, three commands). Beta is that path. Team Brain section added.

GATE EXAMPLES: PASS
`EXAMPLES.md` holds four measured runs (success, missing file, hop-1 fail, usage) with expected stdout and exit codes from this box.

GATE ERROR HANDLING: PASS
Missing file → `NOT_ARRIVED reason=hop2_silent id=42` exit 4, no traceback.
Bad/missing args → `NOT_ARRIVED reason=usage` exit 64, no traceback.
Hop-1 fail → `NOT_ARRIVED reason=hop1_exit` exit 2, no traceback.
No network: hop-2 is local; a missing hop-2 command is OSError caught in `cmd_shows` → silent/fail 4, not a stack.
Wrong platform: nt uses `shell=True`, posix uses `shlex.split`; no machine-absolute paths.

GATE CODE QUALITY: PASS
stdlib only; names `sequential`/`streaming`/`hop2_ok`; no secrets; no `C:\Users\...` in `arrived.py`; no dead `[OK]` printer. v1 roads kept under `builds/` as history, not shipped as the interface.

GATE INTEGRATION: PASS
README § Team Brain: wrap a local send so exit 0 means the minted id appeared on hop-2. Artifact card text: `Artifact/Arrived` — Hop-pair CLI: local success mints an id-debt; hop-2 (command and/or file) must echo that same id; silence is fail. Stdlib. No `[OK]`.

## close
2026-09-05 Task 5. Repo https://github.com/MetaphyKing/Arrived PUBLIC, origin/master clean. Minted Artifact/Arrived/a-8582 (card kept; volume not pasted). `tools\ait.cmd` was missing; minted via `stay_seat.py` with STAY_ROOT=`C:\dev\ait\encyclopedia` (same door), then wrote `C:\dev\ait\tools\ait.cmd`. Session log: Memory Core `SESSION_Arrived_2026-09-05.md`. Manifest row Uploaded / cael. Chat transcript not exportable from this runtime; BUILD_LOG is the record.
