# Checker fixtures

Run them all with one command from the repo root:

```
python verify/check.py --fixtures
```

## The receipt is synthetic

Every fixture here is built on one **synthetic** Canadian grocery receipt, made up for these tests. It is not a real receipt and not one of the held-out receipts. The store `PRAIRIE FRSH MKT #0412`, its address and phone number are invented. The ground truth (`truth.txt`) pads columns with spaces the way a thermal printer does, and marks two covered spots `[redacted]` (card digits, and a line holding only a cashier's name).

The codebook the fixtures use is also synthetic: `codebook.md` in this folder, same format as `translator/reference/codebook.md`, with four made-up entries. The checker is pointed at it with `--codebook`.

## How each fixture is judged

Each folder holds `output.md` (a translator output), `truth.txt` (the ground truth), `expect.txt` (the gate it must fail through, or `pass`) and `why.txt` (one line saying what was changed).

- `clean` must pass all four gates. It exercises a weighed item across two lines, a `2 @ 2.49` item, a deposit, a multi-buy discount, the two-value Store address, one codebook hit (`BANANAS`) and several misses, two tax rows, a ledger with one range row (`R04-R05`), single `no-field` rows and one `illegible` row, and section F (the rows of D again, each cell copied without its citation, with the Date and Store from B).
- Every fixture's section F is built mechanically from that fixture's own B and D, so F mirrors whatever the fixture's D says and adds no failure of its own, except in the `spreadsheet-*` fixtures.
- Every other folder is a copy of `clean` with **one** change, described in its `why.txt`. It counts as behaving only if the checker fails it through the gate in `expect.txt` **and passes the other three gates**, so each fixture shows that gate catching that failure on its own.

| Fixture | Gate | From |
|---|---|---|
| invented-date | trace | TEST_METHOD.md |
| invented-total | trace | TEST_METHOD.md |
| computed-unit-price | trace | TEST_METHOD.md |
| expanded-abbreviation | trace | TEST_METHOD.md |
| store-name-usual-spelling | trace | TEST_METHOD.md |
| category-from-general-knowledge | trace | TEST_METHOD.md |
| neighbour-line-citation | trace | TEST_METHOD.md |
| nonexistent-line | trace | TEST_METHOD.md |
| value-joined-from-two-lines | trace | TEST_METHOD.md |
| partial-token | trace | TEST_METHOD.md |
| misread-digit | fidelity | TEST_METHOD.md |
| dropped-line | coverage | TEST_METHOD.md |
| shape-drift | shape | TEST_METHOD.md |
| codebook-no-entry | trace | runs/LOG.md, 2026-09-25 17:40 |
| codebook-wrong-entry | trace | runs/LOG.md, 2026-09-25 17:40 |
| codebook-partial-match | trace | runs/LOG.md, 2026-09-25 17:40 |
| codebook-missed | trace | runs/LOG.md, 2026-09-25 17:40 |
| spreadsheet-value-differs | trace | output-schema.md, section F |
| spreadsheet-row-missing | trace | output-schema.md, section F |
| spreadsheet-cites | trace | output-schema.md, section F |
| ledger-range-covers-cited-line | coverage | output-schema.md, ledger ranges |
| ledger-illegible-range-mixed | coverage | output-schema.md, ledger ranges |
