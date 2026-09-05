# Arrived — Novelty Engine STANDARD score sheet
seat: cael   mode: STANDARD (bar 70)   date: 2026-09-05
subject: first AIT on BI7, audience=ai-engineer, lang=python, deps=stdlib, difficulty=3

## 1. Executive Summary
Arrived is a CLI whose unit of work is a **hop pair**, not a command. Hop-1 may return exit 0 and print `posted id=15`; that print is parsed for an identifier and becomes a **debt**. Hop-2 is an independent instrument (a log grep, an HTTP GET, a `gh` view). The process exits 0 only when that **same identifier** appears on hop-2 inside the timeout. Silence on hop-2 is failure, not "unknown." The novel claim: **local success is the event that creates the obligation to look elsewhere, not the event that closes the story.**

## 2. Prior Art Landscape
Agent tooling and CI treat the local return code as ontology. The 2026-09-05 IFCH HWM incident is the specimen: `[comms] posted #team-brain id=3` was true locally and false as delivery. Healthchecks wait for *a port*. Receipt verifiers wait for *a signature*. Neither binds "the id I just made" to "the place that id must show up."

## 3. Core Novelty Thesis
A success token that does not name an identifier which has been observed on a second hop is not a success token. It is a syntax error. Arrived makes that grammar executable.

Surprising turn: invert the usual `&&` chain. `cmd && probe` asks "did something else also succeed?" Arrived asks "did **this** id, minted by cmd, **arrive** at probe?" Any other success on hop-2 is irrelevant.

## 4. Full Exposition
Inputs: `--local-cmd`, `--id-regex` (one capturing group), `--remote-cmd` (may contain `{id}`), `--expect` (optional extra needle), `--timeout` seconds, `--interval` seconds. Stdlib only (`subprocess`, `re`, `time`, `argparse`, `sys`). Exit 0 = arrived; 2 = hop-1 failed; 3 = id not parseable; 4 = hop-2 silent/mismatch. stdout is a single machine line: `ARRIVED id=... hop2=...` or `NOT_ARRIVED reason=...`. No `[OK]`.

## 5. Cross-Domain Synthesis Evidence
Primary domain: CLI / agent tooling.

| domain | insight | applied as |
|---|---|---|
| Telephony (ISUP ACM) | call-setup is not "I sent SETUP"; it is "the far end sent ACM" | hop-2 must echo the hop-1 id |
| Two-phase commit | coordinator abort-on-timeout, never abort-on-hope | hop-2 silence = fail, not unknown |
| Double-entry bookkeeping | a debit without a credit is unbalanced, not "probably fine" | local success opens a debit that hop-2 must credit |
| Packet ACK (TCP) | sequence number in the ACK, not "a packet happened" | `{id}` substitution, not a boolean probe |
| Notary public | the stamp is on *this* document | regex capture group is the document |
| Immunology (clonal) | recognition is specific, not "immune system active" | hop-2 match must be the captured id |
| Court evidence | testimony is not the exhibit | hop-1 stdout is testimony; hop-2 is the exhibit |

Structurally integrated: telephony ACM + TCP sequence-numbered ACK (the id must come back) and 2PC abort-on-timeout (silence is no). Synthesis strength: 8/10.

## 6. Adversarial Gauntlet Results
**Primary attack:** "This is wait-for-it with extra flags."
→ Defeated: wait-for-it waits for TCP/open; it cannot fail a green local post whose id never appears in a log. Arrived's fail mode is *wrong id / no id*, not *port closed*.

**Secondary:**
1. "Agents will wrap `sleep 15 && grep`." → That grep is not bound to the minted id; a leftover MIRROR from an earlier post would pass. Arrived interpolates `{id}`.
2. "pipelock already does receipts." → pipelock verifies a signed artifact you already have. Arrived is a *liveness* probe of a hop you do not control, in the seconds after send.
3. "shouldMirror already decided what leaves the box." → that predicate is one instrument. Arrived is the general form so the next silent skip is caught without reading relay source.

Logical consistency: PASS. Falsifiable: run hop-1 that prints `id=N`, withhold hop-2, expect exit 4; then emit `N` on hop-2, expect exit 0.

## 7. Boundary Conditions & Limitations
- If hop-2 cannot be expressed as a command that prints the id (human inbox, air-gapped far side), Arrived cannot help — it will fail closed, which is correct and useless.
- Regex with multiple ids: only the first capturing group is the debt. Callers who need fan-out must run N times.
- Timeout is a clock, not a proof of never-arriving; a late hop-2 after exit 4 is a missed true. Documented; retry is the caller's.
- Does not replace cryptographic receipts. It answers "did it show up," not "did the right party sign it."

## 8. Novelty Scoring Rubric
Honest, no inflation.

| dimension | max | score | why |
|---|---|---|---|
| Core concept absent from prior work | 10 | 8 | hop-pair+id-debt not found in wait-for-it / pipelock / reverify; "wait for condition" exists |
| Combines unrelated ideas | 10 | 7 | ACM + 2PC timeout + double-entry, structurally |
| Surprising path | 10 | 8 | local success as debit, not close |
| Novel arrangement | 15 | 12 | hop-pair as the type; id interpolation as the join |
| Novel methodology | 10 | 7 | fail-on-silence as default grammar |
| Field constraints | 10 | 8 | stdlib CLI, parseable stdout, no `[OK]` |
| Advances field goals | 10 | 8 | agent-ops: present instrument for present claim |
| Survives critique | 10 | 8 | primary attack named and bounded |
| Non-obvious derivation | 5 | 4 | from a real silent-delivery incident, not a brainstorm |
| Cross-domain depth | 10 | 8 | two insights woven into exit codes and `{id}` |
| **TOTAL** | **100** | **78** | GENUINELY NOVEL (70–79) |

No dimension below 60% of max. STANDARD bar 70: PASS.

## 9. Novelty Transparency Manifest
- **Novel:** hop-pair type; local success as debit; `{id}` join; silence=fail as default.
- **Foundational:** subprocess, regex, timeout loop, argparse CLI.
- **Origin of novel parts:** telephony ACM (far-end must speak), 2PC (timeout is no), 2026-09-05 IFCH HWM (local `posted id=3` with no MIRROR).
- **Surprise:** the tool's happy path still looks like `cmd && check`, but a hop-2 success *without the minted id* is a failure. That is the opposite of `&&`.

## Appendix D — Five Lockout Checkpoints
1. **Reject the obvious:** `cmd && grep log` / wait-for-it — insufficient because they do not bind the minted identifier. PASS.
2. **Force synthesis:** ACM + 2PC abort-on-timeout are in the exit grammar. PASS.
3. **Name the cliché:** "healthcheck CLI" / "retry wrapper." Avoided by refusing boolean hop-2. PASS.
4. **Defeat the critic:** primary attack in §6. PASS.
5. **Score ≥ 70:** 78. PASS.

All five pass.
