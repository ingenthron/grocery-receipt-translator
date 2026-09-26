"""Tests for tools/log.py, the verified price log.

Run from the repo root:
  python -m unittest discover -s tests -p "test_*.py" -v

Uses the checker fixtures (a synthetic receipt and its synthetic codebook)
and writes every log into a temporary folder, never into prices/.
"""

import contextlib
import csv
import importlib.util
import io
import shutil
import tempfile
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
FIXTURES = REPO / "tests" / "fixtures"
CODEBOOK = FIXTURES / "codebook.md"
CLEAN = FIXTURES / "clean"

_spec = importlib.util.spec_from_file_location("price_log", str(REPO / "tools" / "log.py"))
price_log = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(price_log)

CLEAN_KEY = "09/20/26|14:32|PRAIRIE FRSH MKT #0412|7.46"
HEADER = ["logged_at", "receipt_key", "date", "store", "as_printed", "qty", "unit_price", "amount",
          "price_note", "tracker_name", "category", "source_file", "fidelity"]


def f_rows(output_path):
    """Section F's rows, read straight from the markdown."""
    lines = Path(output_path).read_text(encoding="utf-8").splitlines()
    start = lines.index("## F. Spreadsheet rows") + 1
    end = next((i for i in range(start, len(lines)) if lines[i].startswith("## ")), len(lines))
    table = [l for l in lines[start:end] if l.startswith("|")]
    return [[c.strip() for c in l.strip()[1:-1].split("|")] for l in table[2:]]


class LogTest(unittest.TestCase):

    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.log = self.tmp / "sub" / "prices.csv"

    def tearDown(self):
        shutil.rmtree(str(self.tmp), ignore_errors=True)

    def run_log(self, output, *extra):
        argv = [str(output), "--log", str(self.log)] + list(extra)
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            code = price_log.main(argv, codebook=CODEBOOK)
        return code, buf.getvalue()

    def read_log(self):
        with self.log.open("r", encoding="utf-8-sig", newline="") as f:
            return list(csv.reader(f))

    def test_pass_appends_rows(self):
        code, text = self.run_log(CLEAN / "output.md", "--truth", str(CLEAN / "truth.txt"))
        self.assertEqual(code, 0, text)
        for gate in ("PASS fidelity", "PASS trace", "PASS coverage", "PASS shape"):
            self.assertIn(gate, text)
        self.assertIn("5 rows appended", text)
        self.assertIn("4 rows are 'not in codebook'", text)
        self.assertTrue(self.log.read_bytes().startswith(b"\xef\xbb\xbf"), "header must carry a BOM for Excel")
        rows = self.read_log()
        self.assertEqual(rows[0], HEADER)
        want = f_rows(CLEAN / "output.md")
        self.assertEqual(len(rows) - 1, len(want))
        for got, f in zip(rows[1:], want):
            self.assertRegex(got[0], r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}$")
            self.assertEqual(got[1], CLEAN_KEY)
            self.assertEqual(got[2:11], f)           # values exactly as in F, sentinels included
            self.assertEqual(got[11], str(CLEAN / "output.md"))
            self.assertEqual(got[12], "checked")
        notes = [r[8] for r in rows[1:]]
        self.assertIn("$2.49 lmt 4, $3.29 ea ; YOU SAVED $1.60", notes)
        self.assertIn("not in source", notes)

    def test_failing_output_writes_nothing(self):
        code, text = self.run_log(FIXTURES / "invented-total" / "output.md")
        self.assertEqual(code, 1, text)
        self.assertIn("FAIL trace", text)
        self.assertIn("REFUSED", text)
        self.assertFalse(self.log.exists())
        self.assertFalse(self.log.parent.exists(), "a refused run must not even create the folder")

        # With a log already there, a refused run leaves it byte for byte.
        self.assertEqual(self.run_log(CLEAN / "output.md")[0], 0)
        before = self.log.read_bytes()
        for fixture, extra in (("misread-digit", ["--truth", str(FIXTURES / "misread-digit" / "truth.txt")]),
                               ("todo-proposes-name", []), ("dropped-line", []), ("shape-drift", [])):
            code, text = self.run_log(FIXTURES / fixture / "output.md", *extra)
            self.assertEqual(code, 1, "%s: %s" % (fixture, text))
            self.assertEqual(self.log.read_bytes(), before, fixture)

    def test_duplicate_refused_then_allowed_with_force(self):
        self.assertEqual(self.run_log(CLEAN / "output.md")[0], 0)
        before = self.log.read_bytes()
        code, text = self.run_log(CLEAN / "output.md")
        self.assertEqual(code, 1, text)
        self.assertIn("already in", text)
        self.assertEqual(self.log.read_bytes(), before)

        code, text = self.run_log(CLEAN / "output.md", "--force")
        self.assertEqual(code, 0, text)
        rows = self.read_log()
        self.assertEqual(rows.count(HEADER), 1, "the header is written once")
        self.assertEqual(len(rows), 1 + 2 * 5)
        self.assertEqual(self.log.read_bytes().count(b"\xef\xbb\xbf"), 1, "only the header carries a BOM")

    def test_not_translated_refused(self):
        out = self.tmp / "not-a-receipt.md"
        sections = ["## A. Source lines", "## B. Receipt fields", "## C. Taxes", "## D. Items",
                    "## E. Coverage ledger", "## F. Spreadsheet rows", "## G. Codebook to-do"]
        out.write_text("# Receipt translation\n\nStatus: not translated (not-a-receipt)\n\n"
                       + "".join("%s\n\nnone\n\n" % h for h in sections), encoding="utf-8")
        code, text = self.run_log(out)
        self.assertEqual(code, 1, text)
        self.assertIn("PASS shape", text)          # a well-formed refusal, refused for having nothing to log
        self.assertIn("no rows to log", text)
        self.assertFalse(self.log.exists())

    def test_fidelity_skip_recorded_as_not_checked(self):
        code, text = self.run_log(CLEAN / "output.md")
        self.assertEqual(code, 0, text)
        self.assertIn("SKIP fidelity", text)
        rows = self.read_log()
        self.assertEqual({r[12] for r in rows[1:]}, {"not checked"})

    def test_mismatched_log_header_refused(self):
        self.log.parent.mkdir(parents=True)
        self.log.write_text("logged_at,receipt_key,date\n", encoding="utf-8-sig")
        before = self.log.read_bytes()
        code, text = self.run_log(CLEAN / "output.md")
        self.assertEqual(code, 1, text)
        self.assertIn("has columns", text)
        self.assertEqual(self.log.read_bytes(), before)


if __name__ == "__main__":
    unittest.main()
