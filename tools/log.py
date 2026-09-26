#!/usr/bin/env python3
"""The verified price log: append a translation's section F rows to a CSV,
but only after the checker has passed it.

  python tools/log.py OUTPUT.md [--truth TRUTH.txt] [--log PATH] [--force]

The output is checked first with verify/check.py and the default codebook
(translator/reference/codebook.md). Nothing is written unless trace,
coverage and shape pass; fidelity must pass too when --truth is given, and
is recorded as `not checked` when it is not. A `not translated` output has
nothing to log and is refused.

On a pass, every section F row is appended to the log (default
prices/prices.csv at the repo root; the folder and header are created when
missing). Values are written exactly as F shows them, sentinels included.
The columns are logged_at, receipt_key, then F's own columns in snake_case
(date, store, as_printed, qty, unit_price, amount, price_note, tracker_name,
category), then source_file and fidelity. receipt_key is B's Date, Time,
Store name and Total without citations, joined with '|'; a receipt whose
key is already in the log is refused unless --force is given.

The log is private shopping history: prices/ is in .gitignore.

Standard library only, Python 3.8+, offline.

Exit codes: 0 rows appended, 1 refused (a gate failed, not translated,
already logged, or the log's header does not match), 2 usage error or
unreadable file.
"""

import argparse
import csv
import importlib.util
import re
import sys
from datetime import datetime
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
CHECK_PATH = REPO / "verify" / "check.py"
DEFAULT_LOG = REPO / "prices" / "prices.csv"

KEY_FIELDS = ("Date", "Time", "Store name", "Total")   # B fields that identify one receipt
LEAD_COLS = ["logged_at", "receipt_key"]
TAIL_COLS = ["source_file", "fidelity"]


def load_checker():
    spec = importlib.util.spec_from_file_location("receipt_check", str(CHECK_PATH))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def snake(name):
    return re.sub(r"[^a-z0-9]+", "_", name.lower()).strip("_")


def read_header_and_keys(log_path):
    """(header, set of receipt keys) of an existing log, or (None, set())."""
    if not log_path.exists():
        return None, set()
    with log_path.open("r", encoding="utf-8-sig", newline="") as f:
        reader = csv.reader(f)
        header = next(reader, None)
        if header is None:
            return None, set()
        k = header.index("receipt_key") if "receipt_key" in header else None
        keys = {row[k] for row in reader if k is not None and len(row) > k}
    return header, keys


def main(argv=None, codebook=None):
    """Run the CLI. `codebook` overrides the default codebook (tests only)."""
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    p = argparse.ArgumentParser(
        description="Append a checked translation's section F rows to the price log.")
    p.add_argument("output", help="the translator output (markdown)")
    p.add_argument("--truth", help="ground-truth transcript; when given, fidelity must pass too")
    p.add_argument("--log", help="the log CSV (default: prices/prices.csv at the repo root)")
    p.add_argument("--force", action="store_true", help="log a receipt whose key is already in the log")
    args = p.parse_args(argv)

    try:
        check = load_checker()
    except (OSError, SyntaxError) as e:
        print("ERROR: cannot load the checker %s: %s" % (CHECK_PATH, e))
        return 2
    truth = Path(args.truth) if args.truth else None
    try:
        schema = check.Schema(check.SCHEMA_PATH)
        res = check.run_checks(Path(args.output), truth, Path(codebook) if codebook else check.DEFAULT_CODEBOOK,
                               schema)
        out = check.Output(Path(args.output), schema)
    except (check.ContractError, OSError, UnicodeDecodeError) as e:
        print("ERROR: %s" % e)
        return 2

    for gate in check.GATES:
        print(check.gate_line(gate, res[gate]))

    # Fidelity is SKIP when no ground truth is given; with one, it must pass.
    need = ["trace", "coverage", "shape"] + (["fidelity"] if truth else [])
    failed = [g for g in need if res[g][0] != "PASS"]
    if failed:
        print("REFUSED: %s did not pass; nothing was logged." % ", ".join(failed))
        return 1

    first_head = out.heads[0][0] if out.heads else len(out.lines)
    status = next((l for l in out.lines[1:first_head] if l.strip()), "")
    if status not in schema.translated_statuses:
        print("REFUSED: the output says '%s'; there are no rows to log." % status)
        return 1

    b, f = out.tables[check.FIELDS], out.tables[check.SHEET]
    fields = {row[0]: row[1] for row in b.rows if len(row) > 1}
    gone = [name for name in KEY_FIELDS if name not in fields]
    if gone:
        print("ERROR: section B has no %s field; tools/log.py builds the receipt key from %s"
              % (", ".join(gone), ", ".join(KEY_FIELDS)))
        return 2
    key = "|".join(check.uncite(fields[name], schema.multi.get(name, False)) for name in KEY_FIELDS)
    header = LEAD_COLS + [snake(c) for c in schema.columns[check.SHEET]] + TAIL_COLS

    log_path = Path(args.log) if args.log else DEFAULT_LOG
    try:
        existing, keys = read_header_and_keys(log_path)
    except (OSError, UnicodeDecodeError, csv.Error) as e:
        print("ERROR: cannot read the log %s: %s" % (log_path, e))
        return 2
    if existing is not None and existing != header:
        print("REFUSED: the log %s has columns %s, but this output would write %s; nothing was logged."
              % (log_path, existing, header))
        return 1
    if key in keys and not args.force:
        print("REFUSED: receipt %s is already in %s; nothing was logged (use --force to log it again)."
              % (key, log_path))
        return 1

    logged_at = datetime.now().isoformat(timespec="seconds")
    fidelity = "checked" if truth else "not checked"
    rows = [[logged_at, key] + list(r) + [args.output, fidelity] for r in f.rows]

    try:
        log_path.parent.mkdir(parents=True, exist_ok=True)
        if existing is None:
            # The header carries a byte-order mark so Excel reads the file as UTF-8.
            with log_path.open("w", encoding="utf-8-sig", newline="") as fh:
                csv.writer(fh).writerow(header)
        with log_path.open("a", encoding="utf-8", newline="") as fh:
            csv.writer(fh).writerows(rows)
    except OSError as e:
        print("ERROR: cannot write the log %s: %s" % (log_path, e))
        return 2

    sheet_cols = schema.columns[check.SHEET]
    tracker_col = sheet_cols.index(check.TRACKER) if check.TRACKER in sheet_cols else None
    unmapped = sum(1 for r in f.rows if tracker_col is not None and r[tracker_col] == check.NOT_IN_CODEBOOK)
    print("LOGGED: %d row%s appended to %s (receipt %s, fidelity %s); %d row%s %s '%s'."
          % (len(rows), "" if len(rows) == 1 else "s", log_path, key, fidelity,
             unmapped, "" if unmapped == 1 else "s", "is" if unmapped == 1 else "are", check.NOT_IN_CODEBOOK))
    return 0


if __name__ == "__main__":
    sys.exit(main())
