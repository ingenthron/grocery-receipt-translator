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

| As printed | Qty | Unit price | Amount | Tax code | Tracker name | Category |
|---|---|---|---|---|---|---|
| <value> | <value> | <value> | <value> | <value> | <value> | <value> |

## E. Coverage ledger

| Line | Reason |
|---|---|
| <line id> | <reason code> |
````

## Sections

| Section | Heading (exact) | Holds |
|---|---|---|
| A | `## A. Source lines` | Every non-blank printed line, numbered, in a `text` code block |
| B | `## B. Receipt fields` | The six fields below, in this order, one row each |
| C | `## C. Taxes` | One row per tax line printed |
| D | `## D. Items` | One row per purchased item, deposit, fee or discount, in receipt order |
| E | `## E. Coverage ledger` | Every source line not cited in B, C or D |

## Status values

| Status line (exact) | When |
|---|---|
| `Status: translated` | The input is one receipt |
| `Status: not translated (not-a-receipt)` | The input is not a receipt |
| `Status: not translated (more-than-one-receipt)` | The input shows two or more receipts |
| `Status: not translated (no-input)` | No image and no receipt text was given |

When the status is `not translated`, sections A to E keep their headings and each body is the single line `none`.

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
| D | As printed, Qty, Unit price, Amount, Tax code, Tracker name, Category |
| E | Line, Reason |

## Sentinels

The only values that need no source citation.

| Sentinel | Meaning | Where |
|---|---|---|
| `not in source` | The receipt does not print this | Any value cell in B, C, D |
| `[illegible]` | The receipt prints something here that cannot be read | Any value cell in B, C, D, cited to the line it is on, as `[illegible] {R07}`; also inside source lines |
| `not in codebook` | No codebook entry matches this row's As printed text exactly | Tracker name and Category only |
| `none` | Nothing to list | Section E when every line is cited; every section when not translated |

When the receipt prints no tax, section C has one row with `not in source` in both cells. When section E has nothing to list, its one row is `none` in both cells.

## Reason codes (section E)

| Code | Meaning |
|---|---|
| `no-field` | The receipt prints this line, and this schema has no field for it (for example a phone number, a cashier line, payment, points, a department heading, a barcode, a thank-you) |
| `illegible` | The line is mostly `[illegible]` and cannot be placed in a field. Allowed only on a line that contains `[illegible]` |

## Citations

Every value that is not a sentinel ends with its citation in braces. How citations work is defined in `format-spec.md`.
