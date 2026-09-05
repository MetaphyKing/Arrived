# Arrived — worked examples

Run from this folder. Python 3.10+. No packages.

## 1. Hop-2 command echoes the minted id

`ex_hop1.py`:
```python
print("posted id=42")
```

`ex_hop2.py`:
```python
import sys
print("MIRROR id=" + sys.argv[1])
```

Command:
```
python arrived.py --local-cmd "python ex_hop1.py" --remote-cmd "python ex_hop2.py {id}" --timeout 4 --interval 0.2
```

Expected (measured 2026-09-05 on this box):
```
ARRIVED id=42 hop2=command
```
exit 0. No `[OK]`.

## 2. Missing hop-2 file (error, not traceback)

```
python arrived.py --local-cmd "python ex_hop1.py" --remote-file .\no-such-far.log --timeout 0.8 --interval 0.2
```

Expected (measured):
```
NOT_ARRIVED reason=hop2_silent id=42
```
exit 4.

## 3. Hop-1 failed

```
python arrived.py --local-cmd "python -c \"raise SystemExit(1)\"" --remote-cmd "python ex_hop2.py x"
```

Expected (measured):
```
NOT_ARRIVED reason=hop1_exit
```
exit 2.

## 4. Usage (no remotes)

```
python arrived.py
```

Expected (measured):
```
NOT_ARRIVED reason=usage
```
exit 64.
