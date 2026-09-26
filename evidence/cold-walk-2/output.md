# Receipt translation

Status: translated

## A. Source lines

```text
R01 PRAIRIE HARVEST FOODS #22
R02 410 MAIN ST N
R03 MOOSE JAW SK S6H 3K1
R04 PRODUCE
R05 ORG BNNA
R06 1.105 kg @ $3.28/kg 3.62
R07 AVOCADO 3 @ 1.49 4.47
R08 DAIRY
R09 NN 2% MLK 4L 5.79
R10 DEPOSIT 0.25 GP
R11 *******************************
R12 SUBTOTAL 14.13
R13 GST 5% 0.01
R14 TOTAL 14.14
R15 VISA [redacted]
R16 2026/09/22 17:15
R17 *******************************
R18 THANK YOU
```

## B. Receipt fields

| Field | Value |
|---|---|
| Store name | PRAIRIE HARVEST FOODS {R01} |
| Store address | 410 MAIN ST N {R02} ; MOOSE JAW SK S6H 3K1 {R03} |
| Date | 2026/09/22 {R16} |
| Time | 17:15 {R16} |
| Subtotal | 14.13 {R12} |
| Total | 14.14 {R14} |

## C. Taxes

| Tax as printed | Amount |
|---|---|
| GST 5% {R13} | 0.01 {R13} |

## D. Items

| As printed | Qty | Unit price | Amount | Tax code | Tracker name | Category |
|---|---|---|---|---|---|---|
| ORG BNNA {R05} | 1.105 kg {R06} | $3.28/kg {R06} | 3.62 {R06} | not in source | Bananas, organic {C001} | Produce {C001} |
| AVOCADO {R07} | 3 {R07} | 1.49 {R07} | 4.47 {R07} | not in source | not in codebook | not in codebook |
| NN 2% MLK 4L {R09} | not in source | not in source | 5.79 {R09} | not in source | Milk 2%, 4 L {C002} | Dairy & Eggs {C002} |
| DEPOSIT {R10} | not in source | not in source | 0.25 {R10} | GP {R10} | not in codebook | not in codebook |

## E. Coverage ledger

| Lines | Reason |
|---|---|
| R04 | no-field |
| R08 | no-field |
| R11 | no-field |
| R15 | no-field |
| R17-R18 | no-field |

## F. Spreadsheet rows

| Date | Store | As printed | Qty | Unit price | Amount | Tracker name | Category |
|---|---|---|---|---|---|---|---|
| 2026/09/22 | PRAIRIE HARVEST FOODS | ORG BNNA | 1.105 kg | $3.28/kg | 3.62 | Bananas, organic | Produce |
| 2026/09/22 | PRAIRIE HARVEST FOODS | AVOCADO | 3 | 1.49 | 4.47 | not in codebook | not in codebook |
| 2026/09/22 | PRAIRIE HARVEST FOODS | NN 2% MLK 4L | not in source | not in source | 5.79 | Milk 2%, 4 L | Dairy & Eggs |
| 2026/09/22 | PRAIRIE HARVEST FOODS | DEPOSIT | not in source | not in source | 0.25 | not in codebook | not in codebook |
