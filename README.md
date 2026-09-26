# Grocery receipt translator

A Claude Project folder that turns a photo of a grocery receipt into a fixed table for a price-tracking spreadsheet. Every value in the table either is printed on the receipt, cited to its line as `{R08}`, or comes from your own codebook, cited to its entry as `{C014}`. Anything else is `not in source`, `[illegible]` or `not in codebook`. Nothing is guessed.

**Who does this by hand today:** anyone who types their grocery receipts into a spreadsheet to track what they pay for each item across stores and over time, decoding `NN 2% MLK 4L` and `ORG BNNA` line by line.

## Use it

Everything you need is in [`translator/`](translator/). Its [README](translator/README.md) says exactly which seven files to add to a Claude Project, the one line of Project instructions, and the one-line request (`Translate this receipt.`). Nothing outside `translator/` goes into the Project.

## The one idea

A translator has to move from the receipt's words (`ORG BNNA`) to the spreadsheet's words (`Bananas, organic`) without inventing anything. Here the only way a word the receipt does not print can reach the output is [`translator/reference/codebook.md`](translator/reference/codebook.md): a table you write, mapping an exact printed text to your name and category. The translator applies entries and never adds one. Items with no entry come back `not in codebook`, which tells you what to add next. So every value cites a source you can open: the receipt line, or the codebook entry.

## Check it yourself

Python 3, standard library only, offline, no API key:

```
python verify/check.py --fixtures
```

This runs 18 fixtures (one clean translation that must pass, and 17 broken ones, each named after a failure the brief lists, that must each fail through the gate they declare), then checks every translation in `translator/examples.md`. It ends with `18 fixtures, 17 red; all behave as declared` and `3 examples in examples.md; all pass`. CI runs the same on Ubuntu and Windows.

To check a translation of your own: `python verify/check.py output.md --truth truth.txt`, where `truth.txt` is the receipt typed out line by line. The four gates are fidelity (the numbered lines match the receipt), trace (each value is whole words on the line it cites, so the right value on the neighbouring line fails), coverage (every line is used or listed in the ledger) and shape. The contract the checker enforces is read from `translator/reference/`, so the two cannot drift apart.

## Results so far, as they happened

The test method was written and committed before anything else ([`TEST_METHOD.md`](TEST_METHOD.md), first commit). Every run, failure and change is in [`runs/LOG.md`](runs/LOG.md), in time order.

- **Held-out real receipt, run 1: FAIL.** A real Superstore receipt, run from its pseudonymized photo with Claude Haiku, in a Project set up exactly as `translator/README.md` says (all seven files and the instruction line, confirmed by the builder). The photo is not published; the receipt's pseudonymized text is [`inputs/heldout-1/truth.txt`](inputs/heldout-1/truth.txt), and you can paste it into the Project to run the same receipt ([`PROVENANCE.md`](inputs/PROVENANCE.md)). The reply ignored the translator ("The receipt is already in English") and invented a total, item names and prices. Kept verbatim in [`runs/heldout-1/run-1/`](runs/heldout-1/run-1/). It shows what this folder exists to prevent; it is also a failure of this folder on that model.
- **Cold walk:** a fresh agent given only the folder translated a synthetic receipt; its output passes all four gates, and the nine places it had to guess were clarified ([`evidence/cold-walk-1/`](evidence/cold-walk-1/)).

## Not done, said plainly

Against the method I committed to: only one real held-out receipt, not three; its ground truth has not yet been proofread against the paper; no stranger has walked this README; the control run and the trap tests were not run. The examples are synthetic, so that the real receipt stays unseen.

## What it will not do

Spell out abbreviations, fix spellings, add anything up, work out a price per kilogram, fill in a missing date, or pick a category from general knowledge. What the checker cannot catch is listed at the end of [`TEST_METHOD.md`](TEST_METHOD.md): mainly, it proves a value is on its line, not that it sits in the right column.
