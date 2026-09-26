# Run log

Append-only, in time order. One entry per event: run, result, failure, change, re-run. Times are Saskatchewan time (UTC-6). See `TEST_METHOD.md` for the bar.

## 2026-09-25 17:40: correction to TEST_METHOD.md, made before any test ran

**What changed in the contract.** The item table gained two columns, Tracker name and Category, filled only from `translator/reference/codebook.md` (a published table that maps exact printed item text to a name and category) and cited to the codebook entry as `{C001}`, where receipt values are cited to a line as `{R01}`. Decided with the builder at about 17:30, before any contract file, checker or run existed.

**Why the frozen method needs a correction.** Its trace gate says every value appears as a whole token on the source line it cites. A codebook name is not printed on the receipt, so the gate as written would fail every codebook value, including correct ones.

**The correction, and nothing else.** A value cited to a codebook entry `{Cnnn}` passes the trace gate only if all of these hold: (a) entry `Cnnn` exists in `translator/reference/codebook.md`; (b) the same row's As printed value, cited to a receipt line, equals that entry's printed text exactly; (c) the value equals that entry's name or category exactly. A row whose As printed value equals an entry's printed text but whose Tracker name says `not in codebook` also fails. Values cited to receipt lines are checked exactly as frozen. The other three gates are unchanged.

**Fixtures added to the frozen list, all through the trace gate:** codebook name with no matching entry; name taken from a different entry than the one the printed text matches; entry applied when the printed text only partly matches its key; a matching entry missed (`not in codebook` where an entry matches).

## 2026-09-25 17:45: development cold walk (not a test run)

A fresh Claude agent (Claude Code subagent, Opus) was given only `translator/` (no examples yet) and a synthetic pasted receipt, and asked to translate it and list every place the files made it guess. Output and receipt: `evidence/cold-walk-1/`. The output held the shape. It named nine ambiguities: how to tell a department heading from an item name, a savings row from a savings total, a size in a name (`4L`) from a quantity, which tokens form a tax label, whether count tokens belong in As printed, `[redacted]` in pasted text, a store number beside the store name, `coupon` missing from the schema's section D summary, and wrapping the output in a code block. All nine were clarified in `translator/` in the next commit. Not a held-out receipt, not a Claude Project, and not scored against the bar.

## 2026-09-25 18:02: heldout-1 opened, ground truth drafted

`heldout-1` (a real Superstore receipt) was assigned held out before Claude Code opened it, and opened only after translator commit `69e3654`. Claude Code drafted the 83-line ground truth and the pseudonymized photo (`inputs/PROVENANCE.md`). Flagged for the builder's proofread: `lmt` versus `1mt`, the asterisk counts, a trademark mark in the logo, whether four amounts share a line with their `@` text, three item names, the barcode digits.

## 2026-09-25 (before 21:07): heldout-1 run 1, FAIL

- **Slip in the method's order:** the builder ran it before the ground truth was proofread and committed. Its result does not depend on the ground truth: it fails the shape gate outright.
- Model: Claude Haiku (as reported by the builder; exact version not recorded). Translator commit `69e3654`. Whether the Project had all seven files and the instruction line is being confirmed.
- Output verbatim: `runs/heldout-1/run-1/output.md`. Checker: `runs/heldout-1/run-1/check.txt` (FAIL shape).
- The reply opens "The receipt is already in English", so the model read "translate" as changing language and did not follow `identity.md`. Against the receipt, it: invented a total (`$134.08`; the receipt prints `134.88`); invented item names (`Diko Yogurt` for `OIKO YGRT`, `PC Home Gallon Bags` for `PC ASHWD GRL BRS`, `Luma PC Salad` for `QUPA TC SALTED`, `WM` for `NN` throughout); gave wrong prices (`$1.49` for the yogurt's `4.93`, `$4.93` for `4.99`); dropped the eggs line and the GST line; labelled `0.72` (the PST) as GST; added categories and a reformatted date.
- **Checker defect found by this run:** trace and coverage printed PASS on an output with no sections, because there was nothing to check. They should fail. Fixed in the next commit.

## 2026-09-25 21:12: run 1 setup confirmed; photo withheld

- The builder confirms the run-1 Project had all seven files and the instruction line. Run 1 is therefore a failure of this translator on Claude Haiku, not a setup error.
- At the builder's request the photo is not published. It was removed from the two unpushed commits that contained it before the first push; nothing else in them changed. `inputs/heldout-1/truth.txt` (the receipt's pseudonymized text) stays, so the receipt can be run as pasted text.

## 2026-09-25 21:22: heldout-1 run 2, FAIL on the bar (fidelity, shape); trace and coverage pass

- Model: Claude Opus 5.5 (extended thinking), same Project and translator commit `69e3654`, new chat, the pseudonymized photo, `Translate this receipt.` The ground truth (draft, not yet proofread) was committed before this run. Not a re-run after a change: nothing in `translator/` changed after the receipt was opened.
- Output verbatim: `runs/heldout-1/run-2/output.md`. Checker: `runs/heldout-1/run-2/check.txt`.
- **Trace PASS:** all 66 receipt-cited values are whole tokens on the line they cite. No value is invented. Covered values came back `[illegible]`, never guessed.
- **Coverage PASS:** all 83 lines are cited or in the ledger.
- **Fidelity FAIL:** 81 of 83 lines match the ground truth exactly. The two asterisk rules (R62, R67) have 38 asterisks in the output and 37 in the unproofread ground truth. Claude Code's own count, made while drafting, was uncertain between 37 and 38; only the paper settles it, and the builder has been asked to count.
- **Shape FAIL:** two progress lines, written while the model zoomed into the photo, come before `# Receipt translation`. The rules forbid anything before the title; the model broke that rule. The body alone passes shape (a diagnostic, not the bar).
- Field placement, by reading: correct throughout. Store name `SUPERSTORE` is taken from R03; the logo lines R01 and R02 are ledgered, never joined. Qty `1` and Unit price `$4.93 ea` come from the printed `1 @ $4.93 ea`; nothing is assumed. The limit lines (`$4.93 lmt 5, $7.19 ea`) are ledgered as no-field.

## 2026-09-25 21:26: ground-truth correction (asterisk rules); run 2 re-checked

- The builder counted both asterisk rules on the paper: 38 and 38. The draft ground truth had 37, which was Claude Code's uncertain count. Lines 62 and 67 of `inputs/heldout-1/truth.txt` are corrected to 38. **Disclosed:** this proofread happened after run 2, and the builder knew run 2 said 38. The other 81 lines are still not proofread against the paper.
- Run 2 re-checked against the corrected ground truth: **fidelity PASS** (83 of 83 lines; the 6 covered values read `[illegible]`), **trace PASS**, **coverage PASS**, **shape FAIL** (the two progress lines before the title). Run 2 still fails the bar, on shape alone.
- Run 1 re-checked: still fails all four gates.

## 2026-09-25 21:28: change after run 2 (not yet re-run)

- `translator/rules.md`, step 8: forbids progress notes before the title, the one thing run 2 failed on, and says the reply's first characters are `# Receipt translation`.
- `translator/README.md`: names the tested model (Claude Opus 5.5) and says the folder failed on Claude Haiku (run 1).
- Made after both heldout-1 runs, so any later run on heldout-1 is labelled "seen". Nothing else in `translator/` changed.

## 2026-09-25 21:45: heldout-1 run 3, FAIL on the bar (fidelity, shape); trace and coverage pass

- Model: Claude Opus 5.5, medium effort, in the Project from runs 1 and 2 (files from commit `69e3654`; the builder did not re-upload `rules.md` after `7a151a3`). New chat, the pseudonymized photo, `Translate this receipt.` Checked with the checker as submitted (`7a151a3`).
- Output verbatim: `runs/heldout-1/run-3/output.md`. Checker: `runs/heldout-1/run-3/check.txt`.
- Below its first line, it differs from run 2 in three source lines only: R44 reads `[illegible]ateTime:` (a faint `D` marked illegible instead of guessed, which is correct behaviour), and both asterisk rules have 36 asterisks (the paper has 38; run 2 had 38). Sections B, C and D are identical to run 2 cell for cell.
- **Trace PASS, coverage PASS.** No value invented.
- **Fidelity FAIL** on R62 and R67: counting a long run of one symbol is unreliable (38 in run 2, 36 in run 3).
- **Shape FAIL:** one line before the title, "The project defines the output format, so I'll read its spec files first."

## 2026-09-25, after the 21:59 deadline: changes (the judged version is tag `comp13-submission`, commit `7a151a3`)

- **Section F, Spreadsheet rows:** the D rows again with the Date and Store name from B, values only, pasteable into a spreadsheet. The checker proves every F cell is a copy of its cited source cell, under the trace gate, so F adds no facts.
- **Ledger ranges:** section E rows may name a range (`R40-R62`) of consecutive uncited lines with one reason. It is the same coverage rule in shorter notation; the checker expands ranges.
- **Repeated-symbol rule:** a rule of `*` or `-` must have its exact count, or be written `[illegible]` whole. This is the answer to run 3's fidelity failure and uses the existing sentinel; the bar is unchanged.
- **No preamble, stronger:** the Project instruction line now says to begin with `# Receipt translation` and write nothing before it, not even a note about reading the files; `rules.md` names both preambles seen (runs 2 and 3).
- **Codebook C005 to C015:** 11 items from heldout-1 that were `not in codebook` in runs 2 and 3, named by Claude Code and pending the builder's approval. Five more (`GG PEACHES N CRM`, `QUPA TC SALTED`, `GRAPE BLUE 2L`, `FS HUMMUS TRDTNL`, `PC ASHWD GRL BRS`) are left unmapped until the builder names them.
- Any later run on heldout-1 is labelled "seen".
- Runs 1 to 3 stay judged against the contract, codebook and checker they ran with (commit `7a151a3`); their `check.txt` files are those results. Against the new contract they would fail shape (no section F, `Line` instead of `Lines`), and runs 2 and 3 would also fail trace, because the new codebook entries C005 to C015 now match rows they correctly wrote as `not in codebook`. That is the codebook growing, not a new failure.
- Checker after these changes: 23 fixtures (5 new: an F cell that differs, a missing F row, an F cell that keeps its citation, a ledger range that swallows a cited line, an `illegible` range with a legible line), all behaving as declared; the 18 old fixtures give the same problems as before.
- Cold walk 2 (development, not a test): a fresh agent with only the updated folder translated a synthetic pasted receipt; all four gates pass on the new format (`evidence/cold-walk-2/`). Three of the five ambiguities it named were clarified: receipt text is copied as given, rules of symbols included; F repeats six named D columns (not Tax code); "the store's header" is defined.
