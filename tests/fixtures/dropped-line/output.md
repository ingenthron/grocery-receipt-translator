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
R11 DEPOSIT 0.20
R12 MULTI-BUY SAVINGS -1.00 GP
R13 SUBTOTAL 7.02
R14 GST 5% 0.20
R15 PST 6% 0.24
R16 TOTAL 7.46
R17 VISA ************[illegible] 7.46
R18 09/20/26 14:32
R19 [illegible]
R20 THANK YOU FOR SHOPPING
```

## B. Receipt fields

| Field | Value |
|---|---|
| Store name | PRAIRIE FRSH MKT #0412 {R01} |
| Store address | 1234 ALBERT ST {R02} ; REGINA SK S4P 2Z5 {R03} |
| Date | 09/20/26 {R18} |
| Time | 14:32 {R18} |
| Subtotal | 7.02 {R13} |
| Total | 7.46 {R16} |

## C. Taxes

| Tax as printed | Amount |
|---|---|
| GST 5% {R14} | 0.20 {R14} |
| PST 6% {R15} | 0.24 {R15} |

## D. Items

| As printed | Qty | Unit price | Amount | Tax code | Tracker name | Category |
|---|---|---|---|---|---|---|
| BANANAS {R06} | 1.020 kg {R07} | not in source | 1.55 {R07} | not in source | Bananas {C001} | Produce {C001} |
| GRN ONIONS {R08} | not in source | not in source | 1.29 {R08} | not in source | not in codebook | not in codebook |
| SPRKL WTR 1L {R09} | 2 {R10} | 2.49 {R10} | 4.98 {R10} | GP {R10} | not in codebook | not in codebook |
| DEPOSIT {R11} | not in source | not in source | 0.20 {R11} | not in source | not in codebook | not in codebook |
| MULTI-BUY SAVINGS {R12} | not in source | not in source | -1.00 {R12} | GP {R12} | not in codebook | not in codebook |

## E. Coverage ledger

| Line | Reason |
|---|---|
| R04 | no-field |
| R05 | no-field |
| R17 | no-field |
| R19 | illegible |
