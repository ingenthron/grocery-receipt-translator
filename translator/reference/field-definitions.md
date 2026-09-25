# Field definitions

Which part of the receipt feeds each field, and what the field holds when the receipt does not print it. Every value is written as `format-spec.md` says: whole tokens from one line, copied exactly, with the line cited.

## B. Receipt fields

| Field | Comes from | When the receipt does not print it |
|---|---|---|
| Store name | The store's name as printed near the top: the words only, not a store number or slogan | `not in source` |
| Store address | The printed address lines near the top: one value per line, joined with ` ; ` | `not in source` |
| Date | The date as printed, in the receipt's own format (never reordered or reformatted) | `not in source` |
| Time | The time as printed, in the receipt's own format | `not in source` |
| Subtotal | The amount on the line labelled as the subtotal (for example `SUBTOTAL`, `SUB-TOTAL`, `SUB TOTAL`) | `not in source` |
| Total | The amount on the line labelled as the total to pay (for example `TOTAL`, `BALANCE DUE`). Not a savings total, not an amount tendered, not change | `not in source` |

## C. Taxes

One row per printed tax line (for example `GST`, `PST`, `HST`), in receipt order.

| Column | Comes from | When not printed |
|---|---|---|
| Tax as printed | The tax's label tokens as printed, such as `GST` or `PST 6%`, not the amount | `not in source` |
| Amount | The tax amount printed on that line | `not in source` |

No tax line printed: one row, `not in source` in both cells.

## D. Items

One row per purchased item, deposit, eco or environmental fee, coupon or discount, in the order the receipt prints them. A line that only continues the row above (a weight, a price per kilogram, a `2 @ 2.49`) belongs to that row, not to a new one. A discount printed under an item is its own row; it is not merged into the item.

| Column | Comes from | When not printed |
|---|---|---|
| As printed | The item's description tokens as printed, such as `PC ORG BNNA` or `DEPOSIT`. Not the amount, not a code letter | `[illegible] {Rnn}` if unreadable |
| Qty | The count or weight as printed, such as `2` or `1.234 kg`. A row with no printed count or weight says `not in source`; it is never assumed to be 1 | `not in source` |
| Unit price | The price per item or per unit as printed, such as `2.49` or `$3.30/kg` or `2/$5.00`. Never worked out from the amount and quantity | `not in source` |
| Amount | The line's printed amount, in the amount column, as printed (`1.88`, `-1.00`, `1.00-`) | `not in source` |
| Tax code | A separate token of letters printed with the amount to show how it is taxed, such as `G`, `GP` or `H`. If the letters are joined to the amount in one token (`3.49GC`), that whole token is the Amount and Tax code is `not in source` | `not in source` |
| Tracker name | The Tracker name of the codebook entry whose Printed text exactly equals this row's As printed text, cited `{Cnnn}` | `not in codebook` |
| Category | The Category of the same codebook entry, cited `{Cnnn}` | `not in codebook` |

No item printed: one row, `not in source` in every cell.

## E. Coverage ledger

Every source line that no value in B, C or D cites, one row each, in line order: its id (`R12`) and a reason code from `output-schema.md`. Lines the schema has no field for (phone, cashier, payment, card, points, savings summary, item count, department heading, barcode, thank-you, store number) are `no-field`. They are listed, never dropped.
