<p align="center">
  <img width="1280" height="850" alt="stay-hero" src="https://github.com/MetaphyKing/Arrived/blob/master/assets/arrived-hero.webp?raw=true"> 
</p>

---

# Arrived

A stdlib Python CLI for AI engineers. **Local success is a debt, not a verdict.**

Hop-1 must print an identifier. Hop-2 (a command and/or a file) must echo **that same identifier**. If hop-2 is silent, Arrived fails. It never prints `[OK]`.

## Install (stranger path)

1. Install Python 3.10 or newer. No pip packages.
2. Copy this folder anywhere. `cd` into it.
3. Run `python arrived.py --help` if you want flags; or copy a command from `EXAMPLES.md`.
4. Run `python -m unittest test_arrived.py` to prove the copy.

```
python arrived.py --local-cmd "python ex_hop1.py" --remote-cmd "python ex_hop2.py {id}"
python arrived.py --local-cmd "python ex_hop1.py" --remote-file far.log
python arrived.py --stream --local-cmd "python ex_hop1.py" --remote-cmd "python ex_hop2.py {id}"
```

## Flags
| flag | meaning |
|---|---|
| `--local-cmd` | required. The hop-1 command. |
| `--remote-cmd` | hop-2 command; `{id}` is replaced with the capture. |
| `--remote-file` | hop-2 file whose contents must contain the id. |
| `--stream` | parse the id from hop-1 stdout before hop-1 exits. |
| `--id-regex` | default `id[=:\s]+(\S+)` — one capturing group. |
| `--expect` | extra needle hop-2 must also contain. |
| `--timeout` / `--interval` | hop-2 poll budget. |

At least one of `--remote-cmd` / `--remote-file` is required.

## Exit codes
0 arrived · 2 hop-1 failed · 3 id unparseable · 4 hop-2 silent · 64 usage

## Test
```
python -m unittest test_arrived.py
```

v1 roads (history, not the shipping interface) live under `builds/v1-A` … `v1-D`.

## Team Brain

After a local post/send/push that prints an id, do not treat that print as delivery. Wrap it:

```
python arrived.py --local-cmd "<the send>" --remote-cmd "<the far-side probe that must print {id}>" --timeout 15
```

Exit 0 means the id showed up on hop-2. Exit 4 means the local hop succeeded and the far side stayed silent — the IFCH `posted id=N` / no-MIRROR case.

Worked examples: `EXAMPLES.md`.

### Artifact/Arrived card (to mint in Task 5)

`Artifact/Arrived` — Hop-pair CLI: local success mints an id-debt; hop-2 (command and/or file) must echo that same id; silence is fail. Stdlib. No `[OK]`.
