# Arrived v1-A (sequential command)

Stdlib Python CLI. Hop-1 must succeed and print an identifier. Hop-2 is a **command** polled until that **same** id appears. Silence is fail. No `[OK]`.

## Install
Copy this folder. Python 3.10+. No packages.

## Use
```
python arrived.py --local-cmd "python hop1.py" --remote-cmd "python hop2.py {id}" --timeout 15
```

`--id-regex` default `id[=:\s]+(\S+)`. `{id}` in `--remote-cmd` is replaced with the capture.

## Exit codes
0 arrived · 2 hop-1 failed · 3 id unparseable · 4 hop-2 silent · 64 usage

## Test
```
python -m unittest test_arrived.py
```
