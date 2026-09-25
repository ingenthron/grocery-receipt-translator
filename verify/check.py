#!/usr/bin/env python3
"""Offline checker for grocery-receipt-translator outputs.

Proves one translator output after the fact against the four gates in
TEST_METHOD.md (fidelity, trace, coverage, shape), with the trace-gate
correction for codebook citations logged in runs/LOG.md on 2026-09-25.

The contract is read, not copied: section headings, status lines, receipt
fields and their multi-value flags, table columns, sentinels and reason codes
come from the markdown tables in translator/reference/output-schema.md, and
categories and entries come from the codebook's tables. The few names the
checker has to reason about (the sentinels below, the reason code
`illegible`, the column `As printed`, the codebook columns `Id` and
`Printed text`) are named here, and the checker stops with an error if the
reference files no longer define them. So the checker and the contract
cannot drift apart silently.

Standard library only, Python 3.8+, offline, no API key.

Usage:
  python verify/check.py OUTPUT.md --truth TRUTH.txt [--codebook PATH]
  python verify/check.py --fixtures

Exit codes: 0 no gate failed, 1 a gate failed (or a fixture misbehaved),
2 usage error or unreadable reference file.
"""

import argparse
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
SCHEMA_PATH = REPO / "translator" / "reference" / "output-schema.md"
DEFAULT_CODEBOOK = REPO / "translator" / "reference" / "codebook.md"
FIXTURES_DIR = REPO / "tests" / "fixtures"

GATES = ("fidelity", "trace", "coverage", "shape")

# Names the checker reasons about. Each must still exist in the reference files.
ILLEGIBLE = "[illegible]"
NOT_IN_SOURCE = "not in source"
NOT_IN_CODEBOOK = "not in codebook"
NONE = "none"
ILLEGIBLE_REASON = "illegible"
AS_PRINTED = "As printed"
CB_ID = "Id"
CB_PRINTED = "Printed text"
# Section roles, by letter. The schema's Sections table must list exactly these.
SOURCE, FIELDS, TAXES, ITEMS, LEDGER = "A", "B", "C", "D", "E"

FENCE_RE = re.compile(r"^(`{3,}|~{3,})(.*)$")
SEP_RE = re.compile(r"^\|?\s*:?-{3,}:?\s*(\|\s*:?-{3,}:?\s*)*\|?$")
CITE_RE = re.compile(r"^(?P<text>.*\S) \{(?P<id>[RC]\d+)\}$")
ANY_CITE_RE = re.compile(r"\{[RC]\d+\}")
R_CITE_RE = re.compile(r"\{(R\d+)\}")
SOURCE_LINE_RE = re.compile(r"^(R\d+)(?: (.*))?$")
MAX_SHOWN = 6  # problems shown per gate before "and N more"


class ContractError(Exception):
    """A reference file is missing something the checker relies on."""


# ---------------------------------------------------------------- markdown

def collapse(s):
    return " ".join(s.split())


def read_lines(path):
    text = Path(path).read_text(encoding="utf-8")
    if text.startswith("﻿"):
        text = text[1:]
    return [line.rstrip() for line in text.splitlines()]


def fence_mask(lines):
    """True for every line that is part of a fenced code block (fences included)."""
    mask, opener = [], None
    for line in lines:
        m = FENCE_RE.match(line)
        if opener is None:
            mask.append(bool(m))
            if m:
                opener = m.group(1)
        else:
            mask.append(True)
            if (m and m.group(1)[0] == opener[0] and len(m.group(1)) >= len(opener)
                    and not m.group(2).strip()):
                opener = None
    return mask


def split_row(line):
    s = line.strip()
    if s.startswith("|"):
        s = s[1:]
    if s.endswith("|") and not s.endswith("\\|"):
        s = s[:-1]
    return [c.strip().replace("\\|", "|") for c in re.split(r"(?<!\\)\|", s)]


def untick(cell):
    if len(cell) >= 2 and cell.startswith("`") and cell.endswith("`"):
        return cell[1:-1]
    return cell


def headings(lines, mask):
    """[(line index, heading line)] for '## ' headings outside code blocks."""
    return [(i, l) for i, l in enumerate(lines) if not mask[i] and l.startswith("## ")]


def section_bounds(lines, heads):
    out = []
    for k, (i, _) in enumerate(heads):
        end = heads[k + 1][0] if k + 1 < len(heads) else len(lines)
        out.append((i + 1, end))
    return out


class Table(object):
    def __init__(self, header, rows, line_idx, sep_ok):
        self.header, self.rows, self.line_idx, self.sep_ok = header, rows, line_idx, sep_ok


def first_table(lines, mask, start, end):
    idx = [i for i in range(start, end) if not mask[i] and lines[i].lstrip().startswith("|")]
    if not idx:
        return None
    run = [idx[0]]
    for i in idx[1:]:
        if i != run[-1] + 1:
            break
        run.append(i)
    rows = [split_row(lines[i]) for i in run]
    sep_ok = len(run) >= 2 and bool(SEP_RE.match(lines[run[1]].strip()))
    return Table(rows[0], rows[2:] if sep_ok else rows[1:], run, sep_ok)


# ---------------------------------------------------------------- contract

class Schema(object):
    """The output shape, read from output-schema.md's tables."""

    def __init__(self, path):
        self.path = Path(path)
        lines = read_lines(path)
        mask = fence_mask(lines)
        heads = headings(lines, mask)
        secs = {l[3:].strip(): b for (_, l), b in zip(heads, section_bounds(lines, heads))}

        def table(name, first_cols):
            if name not in secs:
                raise ContractError("%s has no '## %s' section" % (self.path.name, name))
            t = first_table(lines, mask, *secs[name])
            if t is None or not t.sep_ok:
                raise ContractError("%s: no table under '## %s'" % (self.path.name, name))
            header = [untick(c) for c in t.header]
            if header[:len(first_cols)] != first_cols:
                raise ContractError("%s: table under '## %s' should start with columns %s, has %s"
                                    % (self.path.name, name, first_cols, header))
            return header, [[untick(c) for c in r] for r in t.rows]

        # Title: first line inside the template's fenced block.
        if "The template" not in secs:
            raise ContractError("%s has no '## The template' section" % self.path.name)
        s, e = secs["The template"]
        opener = next((i for i in range(s, e) if mask[i]), None)
        if opener is None or opener + 1 >= e:
            raise ContractError("%s: the template has no fenced block" % self.path.name)
        self.title = lines[opener + 1]

        _, rows = table("Sections", ["Section", "Heading (exact)"])
        self.sections = [(r[0], r[1]) for r in rows]  # [(letter, '## A. Source lines')]
        if [L for L, _ in self.sections] != [SOURCE, FIELDS, TAXES, ITEMS, LEDGER]:
            raise ContractError("%s: sections are %s; check.py knows the roles of A to E only"
                                % (self.path.name, [L for L, _ in self.sections]))

        _, rows = table("Status values", ["Status line (exact)"])
        self.statuses = [r[0] for r in rows]
        self.translated_statuses = [s for s in self.statuses if "not translated" not in s]
        if len(self.translated_statuses) != 1:
            raise ContractError("%s: expected exactly one translated status line" % self.path.name)

        header, rows = table("Receipt fields (section B)", ["Field", "Multiple values allowed"])
        self.field_label = header[0]
        self.fields = [r[0] for r in rows]
        self.multi = {r[0]: r[1].strip().lower() == "yes" for r in rows}

        _, rows = table("Table columns", ["Section", "Columns (exact, in order)"])
        self.columns = {r[0]: [c.strip() for c in r[1].split(",")] for r in rows}
        for L in (FIELDS, TAXES, ITEMS, LEDGER):
            if L not in self.columns:
                raise ContractError("%s: no columns listed for section %s" % (self.path.name, L))
        if AS_PRINTED not in self.columns[ITEMS]:
            raise ContractError("%s: section D has no '%s' column" % (self.path.name, AS_PRINTED))

        _, rows = table("Sentinels", ["Sentinel", "Meaning", "Where"])
        self.sentinels = {r[0]: r[2] for r in rows}
        _, rows = table("Reason codes (section E)", ["Code"])
        self.reasons = [r[0] for r in rows]

        for name in (ILLEGIBLE, NOT_IN_SOURCE, NOT_IN_CODEBOOK, NONE):
            if name not in self.sentinels:
                raise ContractError("%s no longer defines the sentinel '%s'; update check.py"
                                    % (self.path.name, name))
        if ILLEGIBLE_REASON not in self.reasons:
            raise ContractError("%s no longer defines the reason code '%s'; update check.py"
                                % (self.path.name, ILLEGIBLE_REASON))

        # Where each sentinel may stand uncited, read from the Where column:
        # "Any value cell in B, C, D" names sections; otherwise the column names
        # it mentions ("Tracker name and Category only"). "cited to" means the
        # sentinel is not uncited at all ([illegible] {R07}).
        value_cols = set()
        for L in (FIELDS, TAXES, ITEMS):
            value_cols.update(self.value_columns(L))
        self.places, self.cited_sentinels = {}, set()
        for name, where in self.sentinels.items():
            m = re.search(r"[Aa]ny value cell in ([A-E](?:, ?[A-E])*)\b", where)
            secs_ok = set(re.findall(r"[A-E]", m.group(1))) if m else set()
            cols_ok = set() if m else {c for c in value_cols
                                       if re.search(r"\b%s\b" % re.escape(c), where)}
            self.places[name] = (secs_ok, cols_ok)
            if re.search(r"\bcited to\b", where):
                self.cited_sentinels.add(name)

    def value_columns(self, letter):
        cols = self.columns[letter]
        return [c for c in cols if not (letter == FIELDS and c == self.field_label)]

    def uncited_ok(self, letter, col):
        return {name for name, (secs_ok, cols_ok) in self.places.items()
                if name not in self.cited_sentinels and (letter in secs_ok or col in cols_ok)}

    def heading(self, letter):
        return dict(self.sections)[letter]


class Codebook(object):
    """Categories and entries, read from the codebook's tables. Problems go to shape."""

    def __init__(self, path):
        self.path = Path(path)
        self.problems = []
        lines = read_lines(path)
        mask = fence_mask(lines)
        heads = headings(lines, mask)
        secs = {l[3:].strip(): b for (_, l), b in zip(heads, section_bounds(lines, heads))}
        for name in ("Categories", "Entries"):
            if name not in secs:
                raise ContractError("%s has no '## %s' section" % (self.path, name))
        cats = first_table(lines, mask, *secs["Categories"])
        ents = first_table(lines, mask, *secs["Entries"])
        if cats is None or ents is None:
            raise ContractError("%s: missing Categories or Entries table" % self.path)
        self.category_col = cats.header[0]
        self.categories = [r[0] for r in cats.rows]
        self.header = ents.header
        for col in (CB_ID, CB_PRINTED, self.category_col):
            if col not in self.header:
                raise ContractError("%s: Entries table has no '%s' column" % (self.path, col))
        self.entries, self.by_id, self.by_printed = [], {}, {}
        if len(set(self.categories)) != len(self.categories):
            self.problems.append("a category is listed twice")
        for n, row in enumerate(ents.rows, 1):
            if len(row) != len(self.header):
                self.problems.append("entry row %d has %d cells, header has %d"
                                     % (n, len(row), len(self.header)))
                continue
            e = dict(zip(self.header, row))
            eid, printed = e[CB_ID], e[CB_PRINTED]
            if any(not v for v in row):
                self.problems.append("entry %s has an empty cell" % (eid or "row %d" % n))
            if not re.match(r"^C\d{3,}$", eid):
                self.problems.append("entry id '%s' is not C followed by three or more digits" % eid)
            if eid in self.by_id:
                self.problems.append("entry id %s is used twice" % eid)
            if collapse(printed) in self.by_printed:
                self.problems.append("printed text '%s' appears twice (%s and %s)"
                                     % (printed, self.by_printed[collapse(printed)][CB_ID], eid))
            if printed != collapse(printed):
                self.problems.append("entry %s printed text '%s' is not single-spaced" % (eid, printed))
            if e[self.category_col] not in self.categories:
                self.problems.append("entry %s category '%s' is not in the Categories list"
                                     % (eid, e[self.category_col]))
            self.entries.append(e)
            self.by_id.setdefault(eid, e)
            self.by_printed.setdefault(collapse(printed), e)


# ---------------------------------------------------------------- the output

class Output(object):
    """A translator output, parsed tolerantly so every gate can report."""

    def __init__(self, path, schema):
        self.path = Path(path)
        self.lines = read_lines(path)
        self.mask = fence_mask(self.lines)
        self.heads = headings(self.lines, self.mask)
        bounds = section_bounds(self.lines, self.heads)
        letters = [L for L, _ in schema.sections]
        expected = [h for _, h in schema.sections]
        self.body = {}
        if len(self.heads) == len(expected):
            # Same number of sections: locate by position, so a renamed heading
            # is reported once, under shape, and the other gates still run.
            self.body = dict(zip(letters, bounds))
        else:
            for (_, line), b in zip(self.heads, bounds):
                if line in expected:
                    self.body.setdefault(letters[expected.index(line)], b)
        self._parse_source()
        self.tables = {L: self._table(L) for L in (FIELDS, TAXES, ITEMS, LEDGER)}

    def _parse_source(self):
        self.a_block = None      # (first, last+1) line indices of the fenced block
        self.a_inner = []        # raw lines inside it
        self.src = {}            # 'R07' -> text of the line
        rng = self.body.get(SOURCE)
        if not rng:
            return
        s, e = rng
        i = next((k for k in range(s, e) if self.mask[k]), None)
        if i is None:
            return
        j = i
        while j < e and self.mask[j]:
            j += 1
        self.a_block = (i, j)
        block = self.lines[i:j]
        closed = len(block) > 1 and FENCE_RE.match(block[-1]) is not None
        self.a_inner = block[1:-1] if closed else block[1:]
        for line in self.a_inner:
            m = SOURCE_LINE_RE.match(line)
            if m:
                self.src.setdefault(m.group(1), (m.group(2) or "").strip())

    def source_texts(self):
        """Section A lines with the 'Rnn ' prefix stripped, in order."""
        out = []
        for line in self.a_inner:
            m = SOURCE_LINE_RE.match(line)
            out.append((m.group(2) or "") if m else line)
        return out

    def _table(self, letter):
        rng = self.body.get(letter)
        return first_table(self.lines, self.mask, *rng) if rng else None


# ---------------------------------------------------------------- gates

def contiguous(sub, seq):
    n = len(sub)
    return n > 0 and any(seq[i:i + n] == sub for i in range(len(seq) - n + 1))


def fidelity_note(out):
    marks = sum(t.count(ILLEGIBLE) for t in out.source_texts())
    lines = sum(1 for t in out.source_texts() if ILLEGIBLE in t)
    return "%d [illegible] mark%s on %d line%s" % (marks, "" if marks == 1 else "s",
                                                    lines, "" if lines == 1 else "s")


def check_fidelity(out, truth_path):
    truth = [collapse(l) for l in read_lines(truth_path) if l.strip()]
    got = [collapse(t) for t in out.source_texts()]
    problems = []
    if len(got) != len(truth):
        problems.append("section A has %d lines, the ground truth has %d" % (len(got), len(truth)))
    for k, (o, t) in enumerate(zip(got, truth), 1):
        pattern = ".+?".join(re.escape(p) for p in o.split(ILLEGIBLE))
        if not re.fullmatch(pattern, t, re.S):
            problems.append("R%02d reads '%s' but the ground truth line %d is '%s'" % (k, o, k, t))
    note = "%d lines; %s" % (len(got), fidelity_note(out))
    return problems, note


def check_trace(out, schema, cb):
    problems = []
    src = out.src
    cb_cols = [c for c in schema.columns[ITEMS] if c in cb.header and c not in (CB_ID, CB_PRINTED)]

    def token_hint(text, lid):
        toks = text.split()
        if text in src[lid]:
            return " (only part of a longer token there)"
        on = [k for k, v in src.items() if k != lid and contiguous(toks, v.split())]
        if on:
            return " (it is printed on %s)" % ", ".join(on)
        ids = list(src)
        for n in range(1, len(toks)):
            for a, b in zip(ids, ids[1:]):
                if contiguous(toks[:n], src[a].split()) and contiguous(toks[n:], src[b].split()):
                    return " (joined from %s and %s)" % (a, b)
        return ""

    def check_cited(where, part):
        m = CITE_RE.match(part)
        if not m:
            if part in schema.cited_sentinels:
                problems.append("%s: '%s' must be cited to the line it is on, as '%s {Rnn}'"
                                % (where, part, part))
            elif part in schema.sentinels:
                problems.append("%s: the sentinel '%s' is not allowed here" % (where, part))
            else:
                problems.append("%s: '%s' has no citation and is not a sentinel" % (where, part))
            return
        text, cid = m.group("text"), m.group("id")
        if ANY_CITE_RE.search(text):
            problems.append("%s: '%s' holds more than one value" % (where, part))
        elif cid.startswith("C"):
            problems.append("%s: '%s' cites the codebook; only %s may"
                            % (where, part, " and ".join(cb_cols)))
        elif cid not in src:
            problems.append("%s: '%s' cites %s, which is not a line in section A" % (where, text, cid))
        elif ILLEGIBLE in text:
            if text != ILLEGIBLE:
                problems.append("%s: '%s' mixes %s with other text; the value must be just %s"
                                % (where, text, ILLEGIBLE, ILLEGIBLE))
            elif ILLEGIBLE not in src[cid]:
                problems.append("%s: %s cited to %s, but %s has no %s: '%s'"
                                % (where, ILLEGIBLE, cid, cid, ILLEGIBLE, src[cid]))
        elif not contiguous(text.split(), src[cid].split()):
            problems.append("%s: '%s' is not whole tokens on %s '%s'%s"
                            % (where, text, cid, src[cid], token_hint(text, cid)))

    def check_cell(where, letter, col, cell, multi):
        if cell == "":
            problems.append("%s: empty cell" % where)
        elif cell in schema.uncited_ok(letter, col):
            return
        elif multi and " ; " in cell:
            for part in cell.split(" ; "):
                check_cited(where, part)
        else:
            check_cited(where, cell)

    # B: the Value cells, one per field.
    t = out.tables[FIELDS]
    if t:
        for row in t.rows:
            field = row[0]
            for col, cell in zip(t.header[1:], row[1:]):
                check_cell("B %s" % field, FIELDS, col, cell, schema.multi.get(field, False))

    # C: every cell.
    t = out.tables[TAXES]
    if t:
        for n, row in enumerate(t.rows, 1):
            for col, cell in zip(t.header, row):
                check_cell("C row %d %s" % (n, col), TAXES, col, cell, False)

    # D: every cell; Tracker name and Category through the codebook correction.
    t = out.tables[ITEMS]
    if t:
        for n, row in enumerate(t.rows, 1):
            cells = dict(zip(t.header, row))
            ap = cells.get(AS_PRINTED, "")
            label = "D row %d (%s)" % (n, ap)
            for col, cell in zip(t.header, row):
                if col not in cb_cols:
                    check_cell("%s %s" % (label, col), ITEMS, col, cell, False)
            check_codebook_row(label, cells, ap, cb_cols, src, cb, problems)
    return problems


def check_codebook_row(label, cells, ap, cb_cols, src, cb, problems):
    """The runs/LOG.md 2026-09-25 correction, applied to one D row."""
    vals, bad = {}, False
    for col in cb_cols:
        if col not in cells:
            continue
        cell = cells[col]
        if cell == NOT_IN_CODEBOOK:
            vals[col] = None
            continue
        m = CITE_RE.match(cell)
        if not m or not m.group("id").startswith("C") or ANY_CITE_RE.search(m.group("text")):
            problems.append("%s %s: '%s' must be '%s' or one codebook value cited {Cnnn}; %s "
                            "comes only from the codebook" % (label, col, cell, NOT_IN_CODEBOOK, col))
            bad = True
            continue
        vals[col] = (m.group("text"), m.group("id"))
    if bad or not vals:
        return

    m = CITE_RE.match(ap)
    ap_text = None
    if m and m.group("id").startswith("R") and m.group("id") in src and not ANY_CITE_RE.search(m.group("text")):
        ap_text = m.group("text")
    ap_entry = cb.by_printed.get(collapse(ap_text)) if ap_text else None

    cited = {c: v for c, v in vals.items() if v}
    if not cited:
        if ap_entry:
            problems.append("%s: As printed '%s' matches codebook entry %s, but the row says '%s'"
                            % (label, ap_text, ap_entry[CB_ID], NOT_IN_CODEBOOK))
        return
    if len(cited) != len(vals):
        problems.append("%s: '%s' in %s but a codebook citation in %s; both come from one entry or neither does"
                        % (label, NOT_IN_CODEBOOK, ", ".join(c for c in vals if not vals[c]),
                           ", ".join(cited)))
        return
    ids = sorted({v[1] for v in cited.values()})
    if len(ids) > 1:
        problems.append("%s: %s cite different entries (%s)" % (label, " and ".join(cited), ", ".join(ids)))
        return
    cid = ids[0]
    entry = cb.by_id.get(cid)
    if entry is None:
        problems.append("%s: cites codebook entry %s, which does not exist in %s" % (label, cid, cb.path.name))
        return
    if ap_text is None:
        problems.append("%s: a codebook value needs As printed to be one value cited to a line in section A; "
                        "As printed is '%s'" % (label, ap))
        return
    if collapse(ap_text) != collapse(entry[CB_PRINTED]):
        extra = " (it matches entry %s)" % ap_entry[CB_ID] if ap_entry else ""
        problems.append("%s: As printed '%s' is not exactly entry %s's printed text '%s'%s"
                        % (label, ap_text, cid, entry[CB_PRINTED], extra))
        return
    for col, (text, _) in cited.items():
        if text != entry[col]:
            problems.append("%s %s: '%s' is not entry %s's %s '%s'" % (label, col, text, cid, col, entry[col]))


def check_coverage(out, schema):
    problems = []
    src = out.src
    cited = set()
    for L in (FIELDS, TAXES, ITEMS):
        t = out.tables[L]
        if t:
            for row in t.rows:
                for cell in (row[1:] if L == FIELDS else row):
                    cited.update(R_CITE_RE.findall(cell))

    ledger = {}
    t = out.tables[LEDGER]
    if t and t.rows:
        if any(NONE in row for row in t.rows):
            if len(t.rows) != 1 or any(c != NONE for c in t.rows[0]):
                problems.append("E: '%s' must be the only row, with '%s' in both cells" % (NONE, NONE))
        else:
            for row in t.rows:
                lid = row[0]
                reason = row[1] if len(row) > 1 else ""
                if lid not in src:
                    problems.append("E lists '%s', which is not a line in section A" % lid)
                elif lid in ledger:
                    problems.append("E lists %s twice" % lid)
                if reason not in schema.reasons:
                    problems.append("E %s: '%s' is not a reason code (%s)"
                                    % (lid, reason, ", ".join(schema.reasons)))
                elif reason == ILLEGIBLE_REASON and lid in src and ILLEGIBLE not in src[lid]:
                    problems.append("E %s: reason '%s' on a line with no %s: '%s'"
                                    % (lid, reason, ILLEGIBLE, src[lid]))
                ledger.setdefault(lid, reason)

    for lid, text in src.items():
        c, l = lid in cited, lid in ledger
        if c and l:
            problems.append("%s is both cited and in the ledger: '%s'" % (lid, text))
        elif not c and not l:
            problems.append("%s is neither cited in B, C or D nor listed in E: '%s'" % (lid, text))
    return problems


def check_shape(out, schema, cb):
    problems = []
    lines = out.lines
    if not lines or lines[0] != schema.title:
        problems.append("line 1 must be exactly '%s', found '%s'" % (schema.title, lines[0] if lines else ""))
    first_head = out.heads[0][0] if out.heads else len(lines)
    pre = [l for l in lines[1:first_head] if l.strip()]
    status = pre[0] if len(pre) == 1 and pre[0] in schema.statuses else None
    if status is None:
        problems.append("between the title and the first section there must be exactly one status line "
                        "(one of: %s); found %s" % ("; ".join(schema.statuses), pre))
    translated = status is None or status in schema.translated_statuses

    found = [l for _, l in out.heads]
    expected = [h for _, h in schema.sections]
    if found != expected:
        problems.append("section headings must be exactly %s in that order; found %s" % (expected, found))

    for letter, heading in schema.sections:
        rng = out.body.get(letter)
        if rng is None:
            continue
        body = list(range(*rng))
        nonblank = [i for i in body if lines[i].strip()]
        if not translated:
            if [lines[i] for i in nonblank] != [NONE]:
                problems.append("%s: when the status is not translated, the body must be the single line '%s'"
                                % (letter, NONE))
            continue
        if letter == SOURCE:
            problems.extend(shape_source(out, nonblank))
        else:
            problems.extend(shape_table(out, schema, letter, nonblank))

    problems.extend("codebook %s: %s" % (cb.path.name, p) for p in cb.problems)
    return problems


def shape_source(out, nonblank):
    problems = []
    lines = out.lines
    if out.a_block is None:
        return ["A: no ```text code block"]
    first, last = out.a_block
    outside = [lines[i] for i in nonblank if not (first <= i < last)]
    if outside:
        problems.append("A: text outside the code block: '%s'" % outside[0])
    if lines[first] != "```text":
        problems.append("A: the code block must open with ```text, found '%s'" % lines[first])
    if last - first < 2 or lines[last - 1] != "```":
        problems.append("A: the code block is not closed with ```")
    if not out.a_inner:
        problems.append("A: the code block has no lines")
    for k, line in enumerate(out.a_inner, 1):
        want = "R%02d" % k
        m = re.match(r"^(R\d+) (\S.*)$", line)
        if not m:
            problems.append("A line %d: '%s' is not '%s <line as printed>'" % (k, line, want))
        elif m.group(1) != want:
            problems.append("A line %d: numbered %s, expected %s (R01 upward, no gaps)" % (k, m.group(1), want))
    return problems


def shape_table(out, schema, letter, nonblank):
    problems = []
    t = out.tables[letter]
    if t is None:
        return ["%s: no table" % letter]
    outside = [out.lines[i] for i in nonblank if i not in t.line_idx]
    if outside:
        problems.append("%s: text outside the table: '%s'" % (letter, outside[0]))
    want = schema.columns[letter]
    if t.header != want:
        problems.append("%s: columns must be exactly %s, found %s" % (letter, want, t.header))
    if not t.sep_ok:
        problems.append("%s: the second table line must be the |---| separator" % letter)
    for n, row in enumerate(t.rows, 1):
        if len(row) != len(want):
            problems.append("%s row %d has %d cells, expected %d" % (letter, n, len(row), len(want)))
    if not t.rows:
        problems.append("%s: the table has no rows" % letter)
    if letter == FIELDS:
        got = [r[0] for r in t.rows]
        if got != schema.fields:
            problems.append("B: fields must be exactly %s in that order, found %s" % (schema.fields, got))
    if letter == TAXES:
        blank = [r for r in t.rows if all(c == NOT_IN_SOURCE for c in r)]
        if blank and len(t.rows) != 1:
            problems.append("C: a '%s' row is allowed only as the one row when no tax is printed" % NOT_IN_SOURCE)
    return problems


# ---------------------------------------------------------------- running

def run_checks(output_path, truth_path, codebook_path, schema):
    """{gate: (status, problems, note)} with status PASS, FAIL or SKIP."""
    cb = Codebook(codebook_path)
    out = Output(output_path, schema)
    res = {}
    if truth_path is None:
        res["fidelity"] = ("SKIP", [], "no ground truth given")
    else:
        probs, note = check_fidelity(out, truth_path)
        res["fidelity"] = ("FAIL" if probs else "PASS", probs, note)
    for gate, fn in (("trace", lambda: check_trace(out, schema, cb)),
                     ("coverage", lambda: check_coverage(out, schema)),
                     ("shape", lambda: check_shape(out, schema, cb))):
        probs = fn()
        res[gate] = ("FAIL" if probs else "PASS", probs, "")
    return res


def gate_line(gate, result):
    status, probs, note = result
    if status == "SKIP":
        return "SKIP %s (%s)" % (gate, note)
    if status == "PASS":
        return "PASS %s%s" % (gate, " (%s)" % note if note else "")
    shown = probs[:MAX_SHOWN]
    more = " ... and %d more" % (len(probs) - MAX_SHOWN) if len(probs) > MAX_SHOWN else ""
    body = shown[0] if len(shown) == 1 else " ".join("[%d] %s" % (k, p) for k, p in enumerate(shown, 1))
    tail = " (%s)" % note if note else ""
    return "FAIL %s: %s%s%s" % (gate, body, more, tail)


def main_single(args, schema):
    truth = Path(args.truth) if args.truth else None
    codebook = Path(args.codebook) if args.codebook else DEFAULT_CODEBOOK
    res = run_checks(Path(args.output), truth, codebook, schema)
    for gate in GATES:
        print(gate_line(gate, res[gate]))
    failed = [g for g in GATES if res[g][0] == "FAIL"]
    if failed:
        print("RESULT: FAIL (%s)" % ", ".join(failed))
        return 1
    if res["fidelity"][0] == "SKIP":
        print("RESULT: trace, coverage and shape pass, but fidelity was NOT checked because no ground truth "
              "was given. This is not a full pass.")
        return 0
    print("RESULT: PASS (all four gates)")
    return 0


def main_fixtures(schema):
    if not FIXTURES_DIR.is_dir():
        print("no fixtures folder at %s" % FIXTURES_DIR)
        return 1
    shared_cb = FIXTURES_DIR / "codebook.md"
    dirs = sorted(d for d in FIXTURES_DIR.iterdir() if d.is_dir())
    bad, saw_clean, reds = 0, False, 0
    width = max([len(d.name) for d in dirs] + [8])
    for d in dirs:
        expect_file = d / "expect.txt"
        expect = expect_file.read_text(encoding="utf-8").strip() if expect_file.exists() else ""
        if expect not in GATES + ("pass",):
            print("BAD  %-*s expect.txt must name one gate (%s) or 'pass', found '%s'"
                  % (width, d.name, ", ".join(GATES), expect))
            bad += 1
            continue
        cb = d / "codebook.md" if (d / "codebook.md").exists() else shared_cb
        truth = d / "truth.txt" if (d / "truth.txt").exists() else None
        res = run_checks(d / "output.md", truth, cb, schema)
        failed = [g for g in GATES if res[g][0] == "FAIL"]
        skipped = [g for g in GATES if res[g][0] == "SKIP"]
        if expect == "pass":
            saw_clean = saw_clean or d.name == "clean"
            ok = not failed and not skipped
            got = "all four gates pass" if ok else "; ".join(gate_line(g, res[g]) for g in failed + skipped)
        else:
            reds += 1
            ok = failed == [expect] and not skipped
            if ok:
                got = "FAIL %s: %s" % (expect, res[expect][1][0])
            else:
                got = "failed %s, skipped %s: %s" % (failed or "nothing", skipped or "nothing",
                                                   "; ".join(gate_line(g, res[g]) for g in failed))
        print("%s  %-*s expect %-8s -> %s" % ("ok " if ok else "BAD", width, d.name, expect, got))
        bad += 0 if ok else 1
    if not saw_clean:
        print("BAD  no fixture named 'clean' expecting pass")
        bad += 1
    if reds == 0:
        print("BAD  no red fixtures")
        bad += 1
    print("%d fixtures, %d red; %s" % (len(dirs), reds,
                                       "all behave as declared" if bad == 0 else "%d BAD" % bad))
    print("A red fixture is ok only if it fails through its declared gate and passes the other three.")
    return 0 if bad == 0 else 1


def main(argv=None):
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    p = argparse.ArgumentParser(
        description="Check a receipt translation against the four gates in TEST_METHOD.md.")
    p.add_argument("output", nargs="?", help="the translator output (markdown)")
    p.add_argument("--truth", help="ground-truth transcript: one line per non-blank printed line")
    p.add_argument("--codebook", help="codebook to check against (default: translator/reference/codebook.md)")
    p.add_argument("--fixtures", action="store_true", help="run every fixture in tests/fixtures/")
    args = p.parse_args(argv)
    if args.fixtures == bool(args.output):
        p.error("give either OUTPUT.md or --fixtures")
    try:
        schema = Schema(SCHEMA_PATH)
        return main_fixtures(schema) if args.fixtures else main_single(args, schema)
    except ContractError as e:
        print("ERROR: %s" % e)
        return 2
    except (OSError, UnicodeDecodeError) as e:
        print("ERROR: %s" % e)
        return 2


if __name__ == "__main__":
    sys.exit(main())
