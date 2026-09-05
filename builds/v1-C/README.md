# Arrived v1-C (streaming command)

Stdlib Python CLI. Parses the id from hop-1 **as stdout arrives**, then polls a **command** for that id **before hop-1 exits**. Hop-1 must still exit 0. No `[OK]`.

## Install
Copy this folder. Python 3.10+. No packages.

## Use
```
python arrived.py --local-cmd "python hop1.py" --remote-cmd "python hop2.py {id}" --timeout 15
```

Use this when hop-1 prints the id early and then keeps working.

## Exit codes
0 arrived · 2 hop-1 failed · 3 id unparseable · 4 hop-2 silent · 64 usage

## Test
```
python -m unittest test_arrived.py
```
