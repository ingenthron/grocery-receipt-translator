# Examples

Three inputs and the exact translation each one must produce. The receipts are synthetic (made up for these examples, not from a real store), so that the real receipts in this repo stay unseen by the translator. Each translation is shown inside a fence only so you can see where it starts and ends; a real translation is never inside a fence. Every translation here passes `verify/check.py`.

## Example 1: a full receipt, with codebook matches and a sale price

**Input:** a photo of one receipt. The card number on the payment line is covered with a strip of paper. The paper receipt prints these lines:

```text
MAPLE CART GROCERY #0217
88 VICTORIA AVE E
REGINA SK S4N 0N9
TEL 306-555-0199
PRODUCE
ORG BNNA
0.844 kg @ $3.28/kg 2.77
RED PEPPERS 2 @ 1.99 3.98
DAIRY
NN 2% MLK 4L
$5.49 lmt 4, $6.29 ea
1 @ $5.49 ea 5.49
DEPOSIT 0.25 GP
LG EGGS 12 4.79
MULTI BUY SAVINGS 1.00-
HOUSEHOLD
PAPER TOWEL 6RL 8.99 GP
SUBTOTAL 25.27
GST 5% 0.46
PST 6% 0.55
TOTAL 26.28
DEBIT [redacted]
09/24/26 18:02
THANK YOU FOR SHOPPING
```

**Translation:**

````markdown
# Receipt translation

Status: translated

## A. Source lines

```text
R01 MAPLE CART GROCERY #0217
R02 88 VICTORIA AVE E
R03 REGINA SK S4N 0N9
R04 TEL 306-555-0199
R05 PRODUCE
R06 ORG BNNA
R07 0.844 kg @ $3.28/kg 2.77
R08 RED PEPPERS 2 @ 1.99 3.98
R09 DAIRY
R10 NN 2% MLK 4L
R11 $5.49 lmt 4, $6.29 ea
R12 1 @ $5.49 ea 5.49
R13 DEPOSIT 0.25 GP
R14 LG EGGS 12 4.79
R15 MULTI BUY SAVINGS 1.00-
R16 HOUSEHOLD
R17 PAPER TOWEL 6RL 8.99 GP
R18 SUBTOTAL 25.27
R19 GST 5% 0.46
R20 PST 6% 0.55
R21 TOTAL 26.28
R22 DEBIT [illegible]
R23 09/24/26 18:02
R24 THANK YOU FOR SHOPPING
```

## B. Receipt fields

| Field | Value |
|---|---|
| Store name | MAPLE CART GROCERY {R01} |
| Store address | 88 VICTORIA AVE E {R02} ; REGINA SK S4N 0N9 {R03} |
| Date | 09/24/26 {R23} |
| Time | 18:02 {R23} |
| Subtotal | 25.27 {R18} |
| Total | 26.28 {R21} |

## C. Taxes

| Tax as printed | Amount |
|---|---|
| GST 5% {R19} | 0.46 {R19} |
| PST 6% {R20} | 0.55 {R20} |

## D. Items

| As printed | Qty | Unit price | Amount | Price note | Tax code | Tracker name | Category |
|---|---|---|---|---|---|---|---|
| ORG BNNA {R06} | 0.844 kg {R07} | $3.28/kg {R07} | 2.77 {R07} | not in source | not in source | Bananas, organic {C001} | Produce {C001} |
| RED PEPPERS {R08} | 2 {R08} | 1.99 {R08} | 3.98 {R08} | not in source | not in source | not in codebook | not in codebook |
| NN 2% MLK 4L {R10} | 1 {R12} | $5.49 ea {R12} | 5.49 {R12} | $5.49 lmt 4, $6.29 ea {R11} | not in source | Milk 2%, 4 L {C002} | Dairy & Eggs {C002} |
| DEPOSIT {R13} | not in source | not in source | 0.25 {R13} | not in source | GP {R13} | not in codebook | not in codebook |
| LG EGGS 12 {R14} | not in source | not in source | 4.79 {R14} | not in source | not in source | Eggs, large, dozen {C003} | Dairy & Eggs {C003} |
| MULTI BUY SAVINGS {R15} | not in source | not in source | 1.00- {R15} | not in source | not in source | not in codebook | not in codebook |
| PAPER TOWEL 6RL {R17} | not in source | not in source | 8.99 {R17} | not in source | GP {R17} | Paper towel, 6 rolls {C004} | Household {C004} |

## E. Coverage ledger

| Lines | Reason |
|---|---|
| R04-R05 | no-field |
| R09 | no-field |
| R16 | no-field |
| R22 | no-field |
| R24 | no-field |

## F. Spreadsheet rows

| Date | Store | As printed | Qty | Unit price | Amount | Price note | Tracker name | Category |
|---|---|---|---|---|---|---|---|---|
| 09/24/26 | MAPLE CART GROCERY | ORG BNNA | 0.844 kg | $3.28/kg | 2.77 | not in source | Bananas, organic | Produce |
| 09/24/26 | MAPLE CART GROCERY | RED PEPPERS | 2 | 1.99 | 3.98 | not in source | not in codebook | not in codebook |
| 09/24/26 | MAPLE CART GROCERY | NN 2% MLK 4L | 1 | $5.49 ea | 5.49 | $5.49 lmt 4, $6.29 ea | Milk 2%, 4 L | Dairy & Eggs |
| 09/24/26 | MAPLE CART GROCERY | DEPOSIT | not in source | not in source | 0.25 | not in source | not in codebook | not in codebook |
| 09/24/26 | MAPLE CART GROCERY | LG EGGS 12 | not in source | not in source | 4.79 | not in source | Eggs, large, dozen | Dairy & Eggs |
| 09/24/26 | MAPLE CART GROCERY | MULTI BUY SAVINGS | not in source | not in source | 1.00- | not in source | not in codebook | not in codebook |
| 09/24/26 | MAPLE CART GROCERY | PAPER TOWEL 6RL | not in source | not in source | 8.99 | not in source | Paper towel, 6 rolls | Household |

## G. Codebook to-do

| Printed text | Tracker name | Category |
|---|---|---|
| RED PEPPERS | | |
| DEPOSIT | | |
| MULTI BUY SAVINGS | | |
````

Points to notice: `ORG BNNA` has no amount, but the next line continues it, so it is an item; `PRODUCE`, `DAIRY` and `HOUSEHOLD` are headings, so they go to the ledger and never become a Category. The milk's `$5.49 lmt 4, $6.29 ea` is not where its quantity or amount come from, so it goes whole into Price note (the sale and regular price stay visible, and nothing is worked out); its Qty `1` is printed on `1 @ $5.49 ea`. The eggs have no printed quantity, so their Qty is `not in source`, not 1. The covered card number is `[illegible]`, never guessed. `RED PEPPERS` has no codebook entry, so it is `not in codebook` even though the name is obvious, and it appears in G for you to name. Section F repeats D without citations, with the date and store on every row, so it pastes into a spreadsheet as it is.

## Example 2: a torn, creased photo

**Input:** a photo of a receipt torn off above the first item, and cut off by the frame below the total. A crease runs through the price on the third line, so the photo does not show it. The visible part of the paper receipt prints these lines:

```text
BREAD WW 675G 3.29
BTR SALTED 454G 6.49
CHDR MED 400G 7.99
ITEMS 3
SUBTOTAL 17.77
TOTAL 17.77
```

**Translation:**

````markdown
# Receipt translation

Status: translated

## A. Source lines

```text
R01 BREAD WW 675G 3.29
R02 BTR SALTED 454G 6.49
R03 CHDR MED 400G [illegible]
R04 ITEMS 3
R05 SUBTOTAL 17.77
R06 TOTAL 17.77
```

## B. Receipt fields

| Field | Value |
|---|---|
| Store name | not in source |
| Store address | not in source |
| Date | not in source |
| Time | not in source |
| Subtotal | 17.77 {R05} |
| Total | 17.77 {R06} |

## C. Taxes

| Tax as printed | Amount |
|---|---|
| not in source | not in source |

## D. Items

| As printed | Qty | Unit price | Amount | Price note | Tax code | Tracker name | Category |
|---|---|---|---|---|---|---|---|
| BREAD WW 675G {R01} | not in source | not in source | 3.29 {R01} | not in source | not in source | not in codebook | not in codebook |
| BTR SALTED 454G {R02} | not in source | not in source | 6.49 {R02} | not in source | not in source | not in codebook | not in codebook |
| CHDR MED 400G {R03} | not in source | not in source | [illegible] {R03} | not in source | not in source | not in codebook | not in codebook |

## E. Coverage ledger

| Lines | Reason |
|---|---|
| R04 | no-field |

## F. Spreadsheet rows

| Date | Store | As printed | Qty | Unit price | Amount | Price note | Tracker name | Category |
|---|---|---|---|---|---|---|---|---|
| not in source | not in source | BREAD WW 675G | not in source | not in source | 3.29 | not in source | not in codebook | not in codebook |
| not in source | not in source | BTR SALTED 454G | not in source | not in source | 6.49 | not in source | not in codebook | not in codebook |
| not in source | not in source | CHDR MED 400G | not in source | not in source | [illegible] | not in source | not in codebook | not in codebook |

## G. Codebook to-do

| Printed text | Tracker name | Category |
|---|---|---|
| BREAD WW 675G | | |
| BTR SALTED 454G | | |
| CHDR MED 400G | | |
````

Points to notice: the store, address, date and time are not in the photo, so they are `not in source`, not filled in from the store you might recognize. The creased price is `[illegible]`, even though the subtotal would let you work it out: a translator never works anything out. `675G` and `400G` are part of the names, not quantities.

## Example 3: not a receipt

**Input:** a photo of a handwritten shopping list that reads `milk, eggs, bread, apples`.

**Translation:**

````markdown
# Receipt translation

Status: not translated (not-a-receipt)

## A. Source lines

none

## B. Receipt fields

none

## C. Taxes

none

## D. Items

none

## E. Coverage ledger

none

## F. Spreadsheet rows

none

## G. Codebook to-do

none
````
