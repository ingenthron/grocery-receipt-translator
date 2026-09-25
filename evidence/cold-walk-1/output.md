# Receipt translation

Status: translated

## A. Source lines

```text
R01 SAVE MART FOODS #0412
R02 1234 ALBERT ST
R03 REGINA SK S4P 2Z5
R04 (306) 555-0142
R05 PRODUCE
R06 ORG BNNA
R07 0.844 kg @ $3.28/kg 2.77 G
R08 RED PEPPERS 2 @ 1.99 3.98 G
R09 DAIRY
R10 NN 2% MLK 4L 5.49
R11 DEPOSIT 0.25 GP
R12 MULTI BUY SAVINGS 1.00-
R13 SUBTOTAL 11.49
R14 GST 5% 0.27
R15 PST 6% 0.02
R16 TOTAL 11.78
R17 VISA [redacted]
R18 09/24/26 18:02
R19 THANK YOU FOR SHOPPING
```

## B. Receipt fields

| Field | Value |
|---|---|
| Store name | SAVE MART FOODS {R01} |
| Store address | 1234 ALBERT ST {R02} ; REGINA SK S4P 2Z5 {R03} |
| Date | 09/24/26 {R18} |
| Time | 18:02 {R18} |
| Subtotal | 11.49 {R13} |
| Total | 11.78 {R16} |

## C. Taxes

| Tax as printed | Amount |
|---|---|
| GST 5% {R14} | 0.27 {R14} |
| PST 6% {R15} | 0.02 {R15} |

## D. Items

| As printed | Qty | Unit price | Amount | Tax code | Tracker name | Category |
|---|---|---|---|---|---|---|
| ORG BNNA {R06} | 0.844 kg {R07} | $3.28/kg {R07} | 2.77 {R07} | G {R07} | not in codebook | not in codebook |
| RED PEPPERS {R08} | 2 {R08} | 1.99 {R08} | 3.98 {R08} | G {R08} | not in codebook | not in codebook |
| NN 2% MLK 4L {R10} | not in source | not in source | 5.49 {R10} | not in source | not in codebook | not in codebook |
| DEPOSIT {R11} | not in source | not in source | 0.25 {R11} | GP {R11} | not in codebook | not in codebook |
| MULTI BUY SAVINGS {R12} | not in source | not in source | 1.00- {R12} | not in source | not in codebook | not in codebook |

## E. Coverage ledger

| Line | Reason |
|---|---|
| R04 | no-field |
| R05 | no-field |
| R09 | no-field |
| R17 | no-field |
| R19 | no-field |
