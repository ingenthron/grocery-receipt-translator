# Output schema

The exact shape of every output, for every input. Nothing comes before it or after it. `verify/check.py` reads the tables in this file, so this file is the one home of the shape.

## The template

````
# Receipt translation

Status: translated

## A. Source lines

```text
R01 <line 1 of the receipt, as printed>
R02 <line 2>
...
```

## B. Receipt fields

| Field | Value |
|---|---|
| Store name | <value> |
| Store address | <value> |
| Date | <value> |
| Time | <value> |
| Subtotal | <value> |
| Total | <value> |

## C. Taxes

| Tax as printed | Amount |
|---|---|
| <value> | <value> |

## D. Items

| As printed | Qty | Unit price | Amount | Price note | Tax code | Tracker name | Category |
|---|---|---|---|---|---|---|---|
| <value> | <value> | <value> | <value> | <value> | <value> | <value> | <value> |

## E. Coverage ledger

| Lines | Reason |
|---|---|
| <line id or range> | <reason code> |

## F. Spreadsheet rows

| Date | Store | As printed | Qty | Unit price | Amount | Price note | Tracker name | Category |
|---|---|---|---|---|---|---|---|---|
| <copy> | <copy> | <copy> | <copy> | <copy> | <copy> | <copy> | <copy> | <copy> |

## G. Codebook to-do

| Printed text | Tracker name | Category |
|---|---|---|
| <copy> | | |
````

## Sections

| Section | Heading (exact) | Holds |
|---|---|---|
| A | `## A. Source lines` | Every non-blank printed line, numbered, in a `text` code block |
| B | `## B. Receipt fields` | The six fields below, in this order, one row each |
| C | `## C. Taxes` | One row per tax line printed |
| D | `## D. Items` | One row per purchased item, deposit, fee, coupon or discount, in receipt order |
| E | `## E. Coverage ledger` | Every source line not cited in B, C or D, one line or one range of lines per row |
| F | `## F. Spreadsheet rows` | The rows of D again, values only, ready to paste into a spreadsheet: every cell is a copy of a cell above, without its citation |
| G | `## G. Codebook to-do` | Each distinct As printed text in D that is `not in codebook`, ready to paste into `codebook.md`, with the name and category left empty for the owner to fill |

## Status values

| Status line (exact) | When |
|---|---|
| `Status: translated` | The input is one receipt: one photo, up to three overlapping photos of the same receipt sent together, or its text |
| `Status: not translated (not-a-receipt)` | The input is not a receipt |
| `Status: not translated (more-than-one-receipt)` | The input shows two or more receipts |
| `Status: not translated (no-input)` | No image and no receipt text was given |

When the status is `not translated`, sections A to G keep their headings and each body is the single line `none`.

## Receipt fields (section B)

| Field | Multiple values allowed |
|---|---|
| Store name | no |
| Store address | yes |
| Date | no |
| Time | no |
| Subtotal | no |
| Total | no |

## Table columns

| Section | Columns (exact, in order) |
|---|---|
| B | Field, Value |
| C | Tax as printed, Amount |
| D | As printed, Qty, Unit price, Amount, Price note, Tax code, Tracker name, Category |
| E | Lines, Reason |
| F | Date, Store, As printed, Qty, Unit price, Amount, Price note, Tracker name, Category |
| G | Printed text, Tracker name, Category |

## Sentinels

Fixed values written in place of a receipt value. All of them except `[illegible]` stand without a citation.

| Sentinel | Meaning | Where |
|---|---|---|
| `not in source` | The receipt does not print this | Any value cell in B, C, D, except Tracker name and Category (those are `not in codebook`) |
| `[illegible]` | The receipt prints something here that cannot be read | Any value cell in B, C, D, cited to the line it is on, as `[illegible] {R07}`; also inside source lines |
| `not in codebook` | No codebook entry matches this row's As printed text exactly | Tracker name and Category only |
| `none` | Nothing to list | Section E when every line is cited; section G when every item has a codebook entry; every section when not translated |

When the receipt prints no tax, section C has one row with `not in source` in both cells. When section E has nothing to list, its one row is `none` in both cells.

## Spreadsheet rows (section F)

Section F adds no value of its own. It has exactly one row per row of D, in the same order. Each cell is copied from one cell above, with the citation removed; a sentinel is copied as it is, and `[illegible] {R07}` becomes `[illegible]`.

| F column | Copied from |
|---|---|
| Date | B, Date |
| Store | B, Store name |
| As printed | D, As printed, same row |
| Qty | D, Qty, same row |
| Unit price | D, Unit price, same row |
| Amount | D, Amount, same row |
| Price note | D, Price note, same row |
| Tracker name | D, Tracker name, same row |
| Category | D, Category, same row |

## Reason codes (section E)

| Code | Meaning |
|---|---|
| `no-field` | The receipt prints this line, and this schema has no field for it (for example a phone number, a cashier line, payment, points, a department heading, a barcode, a thank-you) |
| `illegible` | The line is mostly `[illegible]` and cannot be placed in a field. Allowed only on a line that contains `[illegible]` |

## Price note (section D)

Price note may hold more than one value when a row has more than one note line: one value per line, each with its citation, joined with ` ; `, as for Store address.

## Codebook to-do (section G)

One row per distinct As printed text in D whose Tracker name is `not in codebook`, in the order D first shows it, copied without its citation. Rows whose As printed is `[illegible]` or `not in source` are left out, because they cannot be a codebook key. The Tracker name and Category cells are always empty: the translator never proposes a name. When every row of D has a codebook entry, G has one row with `none` in all three cells.

## Ledger ranges (section E)

A ledger row names one line (`R07`) or a range of consecutive lines (`R40-R62`, both ends included) that share one reason code and none of which is cited in B, C or D. Every source line not cited appears in exactly one ledger row.

## Citations

Every value in B, C and D that is not a sentinel ends with its citation in braces. Section F carries no citations: each of its cells points to the cell it was copied from. How citations work is defined in `format-spec.md`.
