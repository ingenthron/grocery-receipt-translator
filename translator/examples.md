# Examples

Three inputs and the exact translation each one must produce. The receipts are synthetic (made up for these examples, not from a real store), so that the real receipts in this repo stay unseen by the translator. Each translation is shown inside a fence only so you can see where it starts and ends; a real translation is never inside a fence. Every translation here passes `verify/check.py`.

## Example 1: a full receipt, with codebook matches

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
NN 2% MLK 4L 5.49
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
R10 NN 2% MLK 4L 5.49
R11 DEPOSIT 0.25 GP
R12 LG EGGS 12 4.79
R13 MULTI BUY SAVINGS 1.00-
R14 HOUSEHOLD
R15 PAPER TOWEL 6RL 8.99 GP
R16 SUBTOTAL 25.27
R17 GST 5% 0.46
R18 PST 6% 0.55
R19 TOTAL 26.28
R20 DEBIT [illegible]
R21 09/24/26 18:02
R22 THANK YOU FOR SHOPPING
```

## B. Receipt fields

| Field | Value |
|---|---|
| Store name | MAPLE CART GROCERY {R01} |
| Store address | 88 VICTORIA AVE E {R02} ; REGINA SK S4N 0N9 {R03} |
| Date | 09/24/26 {R21} |
| Time | 18:02 {R21} |
| Subtotal | 25.27 {R16} |
| Total | 26.28 {R19} |

## C. Taxes

| Tax as printed | Amount |
|---|---|
| GST 5% {R17} | 0.46 {R17} |
| PST 6% {R18} | 0.55 {R18} |

## D. Items

| As printed | Qty | Unit price | Amount | Tax code | Tracker name | Category |
|---|---|---|---|---|---|---|
| ORG BNNA {R06} | 0.844 kg {R07} | $3.28/kg {R07} | 2.77 {R07} | not in source | Bananas, organic {C001} | Produce {C001} |
| RED PEPPERS {R08} | 2 {R08} | 1.99 {R08} | 3.98 {R08} | not in source | not in codebook | not in codebook |
| NN 2% MLK 4L {R10} | not in source | not in source | 5.49 {R10} | not in source | Milk 2%, 4 L {C002} | Dairy & Eggs {C002} |
| DEPOSIT {R11} | not in source | not in source | 0.25 {R11} | GP {R11} | not in codebook | not in codebook |
| LG EGGS 12 {R12} | not in source | not in source | 4.79 {R12} | not in source | Eggs, large, dozen {C003} | Dairy & Eggs {C003} |
| MULTI BUY SAVINGS {R13} | not in source | not in source | 1.00- {R13} | not in source | not in codebook | not in codebook |
| PAPER TOWEL 6RL {R15} | not in source | not in source | 8.99 {R15} | GP {R15} | Paper towel, 6 rolls {C004} | Household {C004} |

## E. Coverage ledger

| Line | Reason |
|---|---|
| R04 | no-field |
| R05 | no-field |
| R09 | no-field |
| R14 | no-field |
| R20 | no-field |
| R22 | no-field |
````

Points to notice: `ORG BNNA` has no amount, but the next line continues it, so it is an item; `PRODUCE`, `DAIRY` and `HOUSEHOLD` are headings, so they go to the ledger and never become a Category. The milk and eggs have no printed quantity, so Qty is `not in source`, not 1. The covered card number is `[illegible]`, never guessed. `RED PEPPERS` has no codebook entry, so it is `not in codebook`, even though the name is obvious.

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

| As printed | Qty | Unit price | Amount | Tax code | Tracker name | Category |
|---|---|---|---|---|---|---|
| BREAD WW 675G {R01} | not in source | not in source | 3.29 {R01} | not in source | not in codebook | not in codebook |
| BTR SALTED 454G {R02} | not in source | not in source | 6.49 {R02} | not in source | not in codebook | not in codebook |
| CHDR MED 400G {R03} | not in source | not in source | [illegible] {R03} | not in source | not in codebook | not in codebook |

## E. Coverage ledger

| Line | Reason |
|---|---|
| R04 | no-field |
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
````
