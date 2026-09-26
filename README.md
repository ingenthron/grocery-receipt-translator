# Grocery receipt translator

A Claude Project folder that turns a photo of a grocery receipt into a fixed table for a price-tracking spreadsheet. Every value in the table either is printed on the receipt, cited to its line as `{R08}`, or comes from your own codebook, cited to its entry as `{C001}`. Anything else is `not in source`, `[illegible]` or `not in codebook`. Nothing is guessed.

The output also gives the same items as clean spreadsheet rows (date, store, item as printed, quantity, unit price, amount, any sale or regular price printed under it, your name and category), which the checker proves are copies of cited cells, and a to-do list of the items your codebook does not know yet.

**Judged version:** tag [`comp13-submission`](https://github.com/ingenthron/grocery-receipt-translator/tree/comp13-submission) (commit `7a151a3`), the last commit before the Clief Notes Comp #13 deadline. Everything after it is listed, with the reason, in [`runs/LOG.md`](runs/LOG.md).

**Who does this by hand today:** anyone who types their grocery receipts into a spreadsheet to track what they pay for each item across stores and over time, decoding `NN 2% MLK 4L` and `ORG BNNA` line by line.

## Use it

Everything you need is in [`translator/`](translator/). Its [README](translator/README.md) says exactly which seven files to add to a Claude Project, the one line of Project instructions, and the one-line request (`Translate this receipt.`). Nothing outside `translator/` goes into the Project.

## The one idea

A translator has to move from the receipt's words (`ORG BNNA`) to the spreadsheet's words (`Bananas, organic`) without inventing anything. Here the only way a word the receipt does not print can reach the output is [`translator/reference/codebook.md`](translator/reference/codebook.md): a table you write, mapping an exact printed text to your name and category. The translator applies entries and never adds one. Items with no entry come back `not in codebook`, which tells you what to add next. So every value cites a source you can open: the receipt line, or the codebook entry.

## Keep a price log

Once a translation checks out, one command adds its spreadsheet rows to your own log:

```
python tools/log.py output.md
```

It runs the checker first and **writes nothing unless the translation passes**, so a misread price or an invented total never reaches your price history. It refuses to log the same receipt twice. The log is `prices/prices.csv`, which stays on your machine (it is in `.gitignore`).

## Check it yourself

Python 3, standard library only, offline, no API key:

```
python verify/check.py --fixtures
```

This runs 27 fixtures (one clean translation that must pass, and 26 broken ones, each named after a failure the brief lists or a way to fake the spreadsheet rows, the codebook to-do or the ledger, that must each fail through the gate they declare), then checks every translation in `translator/examples.md`. It ends with `27 fixtures, 26 red; all behave as declared` and `3 examples in examples.md; all pass`. The price-log tool has its own tests: `python -m unittest discover -s tests`. CI runs the same on Ubuntu and Windows.

To check a translation of your own: `python verify/check.py output.md --truth truth.txt`, where `truth.txt` is the receipt typed out line by line. The four gates are fidelity (the numbered lines match the receipt), trace (each value is whole words on the line it cites, so the right value on the neighbouring line fails), coverage (every line is used or listed in the ledger) and shape. The contract the checker enforces is read from `translator/reference/`, so the two cannot drift apart.

## Results so far, as they happened

The test method was written and committed before anything else ([`TEST_METHOD.md`](TEST_METHOD.md), first commit). Every run, failure and change is in [`runs/LOG.md`](runs/LOG.md), in time order.

- **Held-out real receipt, run 1: FAIL.** A real Superstore receipt, run from its pseudonymized photo with Claude Haiku, in a Project set up exactly as `translator/README.md` says (all seven files and the instruction line, confirmed by the builder). The photo is not published; the receipt's pseudonymized text is [`inputs/heldout-1/truth.txt`](inputs/heldout-1/truth.txt), and you can paste it into the Project to run the same receipt ([`PROVENANCE.md`](inputs/PROVENANCE.md)). The reply ignored the translator ("The receipt is already in English") and invented a total, item names and prices. Kept verbatim in [`runs/heldout-1/run-1/`](runs/heldout-1/run-1/). It shows what this folder exists to prevent; it is also a failure of this folder on that model.
- **Held-out real receipt, run 2 (Claude Opus 5.5): FAIL on the bar, on shape only; nothing invented.** Same Project, same translator, same photo. Fidelity, trace and coverage pass: all 83 numbered lines match the receipt (the six covered values came back `[illegible]`, never guessed), all 66 cited values sit on the line they cite, and every line is cited or ledgered. It fails shape because two progress notes precede the title. Fidelity first failed on two asterisk rules; the paper showed the model was right and my draft ground truth was wrong, corrected and disclosed in the log. Details in [`runs/heldout-1/run-2/`](runs/heldout-1/run-2/). **Use the strongest model you have:** on Haiku the same folder failed completely.
- **Held-out real receipt, run 3 (Claude Opus 5.5, medium effort): FAIL on the bar; nothing invented.** Sections B, C and D came out identical to run 2, cell for cell. It fails fidelity because it counted 36 asterisks in two decorative rules (the paper has 38), and shape because of one line before the title. Both led to rule changes after the deadline (see the log). Details in [`runs/heldout-1/run-3/`](runs/heldout-1/run-3/).
- **Cold walk:** a fresh agent given only the folder translated a synthetic receipt; its output passes all four gates, and the nine places it had to guess were clarified ([`evidence/cold-walk-1/`](evidence/cold-walk-1/)).

## Not done, said plainly

Against the method I committed to: only one real held-out receipt, not three; of its ground truth, only the two asterisk rules have been checked against the paper; no stranger has walked this README; the control run and the trap tests were not run. The examples are synthetic, so that the real receipt stays unseen.

## What it will not do

Spell out abbreviations, fix spellings, add anything up, work out a price per kilogram, fill in a missing date, or pick a category from general knowledge. What the checker cannot catch is listed at the end of [`TEST_METHOD.md`](TEST_METHOD.md): mainly, it proves a value is on its line, not that it sits in the right column.
