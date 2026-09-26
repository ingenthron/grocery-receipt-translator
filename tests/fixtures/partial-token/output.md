# Receipt translation

Status: translated

## A. Source lines

```text
R01 PRAIRIE FRSH MKT #0412
R02 1234 ALBERT ST
R03 REGINA SK S4P 2Z5
R04 TEL (306) 555-0148
R05 GROCERY
R06 BANANAS
R07 1.020 kg 1.55
R08 GRN ONIONS 1.29
R09 SPRKL WTR 1L
R10 2 @ 2.49 4.98 GP
R11 $2.49 lmt 4, $3.29 ea
R12 YOU SAVED $1.60
R13 DEPOSIT 0.20
R14 MULTI-BUY SAVINGS -1.00 GP
R15 SUBTOTAL 7.02
R16 GST 5% 0.20
R17 PST 6% 0.24
R18 TOTAL 7.46
R19 VISA ************[illegible] 7.46
R20 09/20/26 14:32
R21 [illegible]
R22 THANK YOU FOR SHOPPING
```

## B. Receipt fields

| Field | Value |
|---|---|
| Store name | PRAIRIE FRSH MKT #0412 {R01} |
| Store address | 1234 ALBERT ST {R02} ; REGINA SK S4P 2Z5 {R03} |
| Date | 09/20/26 {R20} |
| Time | 14:32 {R20} |
| Subtotal | 7.02 {R15} |
| Total | 7.46 {R18} |

## C. Taxes

| Tax as printed | Amount |
|---|---|
| GST 5% {R16} | 0.20 {R16} |
| PST 6% {R17} | 0.24 {R17} |

## D. Items

| As printed | Qty | Unit price | Amount | Price note | Tax code | Tracker name | Category |
|---|---|---|---|---|---|---|---|
| BANANAS {R06} | 1.020 kg {R07} | not in source | 1.55 {R07} | not in source | not in source | Bananas {C001} | Produce {C001} |
| GRN ONIONS {R08} | not in source | not in source | 1.29 {R08} | not in source | not in source | not in codebook | not in codebook |
| SPRKL WTR 1L {R09} | 2 {R10} | 2.49 {R10} | 4.98 {R10} | $2.49 lmt 4, $3.29 ea {R11} ; YOU SAVED $1.60 {R12} | GP {R10} | not in codebook | not in codebook |
| DEPOSIT {R13} | not in source | not in source | 0.20 {R13} | not in source | not in source | not in codebook | not in codebook |
| MULTI-BUY SAVINGS {R14} | not in source | not in source | 1.00 {R14} | not in source | GP {R14} | not in codebook | not in codebook |

## E. Coverage ledger

| Lines | Reason |
|---|---|
| R04-R05 | no-field |
| R19 | no-field |
| R21 | illegible |
| R22 | no-field |

## F. Spreadsheet rows

| Date | Store | As printed | Qty | Unit price | Amount | Price note | Tracker name | Category |
|---|---|---|---|---|---|---|---|---|
| 09/20/26 | PRAIRIE FRSH MKT #0412 | BANANAS | 1.020 kg | not in source | 1.55 | not in source | Bananas | Produce |
| 09/20/26 | PRAIRIE FRSH MKT #0412 | GRN ONIONS | not in source | not in source | 1.29 | not in source | not in codebook | not in codebook |
| 09/20/26 | PRAIRIE FRSH MKT #0412 | SPRKL WTR 1L | 2 | 2.49 | 4.98 | $2.49 lmt 4, $3.29 ea ; YOU SAVED $1.60 | not in codebook | not in codebook |
| 09/20/26 | PRAIRIE FRSH MKT #0412 | DEPOSIT | not in source | not in source | 0.20 | not in source | not in codebook | not in codebook |
| 09/20/26 | PRAIRIE FRSH MKT #0412 | MULTI-BUY SAVINGS | not in source | not in source | 1.00 | not in source | not in codebook | not in codebook |

## G. Codebook to-do

| Printed text | Tracker name | Category |
|---|---|---|
| GRN ONIONS | | |
| SPRKL WTR 1L | | |
| DEPOSIT | | |
| MULTI-BUY SAVINGS | | |
