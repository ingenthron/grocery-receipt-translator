The project defines the output format, so I'll read its spec files first.

# Receipt translation

Status: translated

## A. Source lines

```text
R01 REAL CANADIAN
R02 SUPERSTORE
R03 SUPERSTORE (2055 PRINCE OF WALES DR)
R04 (306)546-6518
R05 Welcome #
R06 21-GROCERY
R07 06038371434 NN RICE CRACKERS RJ 1.49
R08 22-DAIRY
R09 05680063095 OIKO YGRT RJ
R10 $4.93 lmt 5, $7.19 ea
R11 1 @ $4.93 ea 4.93
R12 06870004877 DAIR COTT CHEESE RJ 7.49
R13 67495900022 GEGG LARGE RJ 8.98
R14 23-FROZEN
R15 06038300574 NN PINEAPPLE RJ 16.49
R16 06038309313 NNNI BLUEBERRIES RJ 17.99
R17 06038310141 NN GREEN PEAS CP RJ 6.79
R18 06038386701 NN CUT GREEN BEA RJ 3.79
R19 19056942325 GG PEACHES N CRM RJ 3.50
R20 25-NATURAL FOODS
R21 05844918204 LOVE CRN GRNL RJ 12.99
R22 06882617603 QUPA TC SALTED GPRJ 4.99
R23 27-PRODUCE
R24 03338346576 GRAPE BLUE 2L RJ 7.00
R25 4131 APPLE FUJI RJ
R26 1.120 kg @ $4.14/kg 4.64
R27 35-DELI
R28 05889854006 OLD CHEDDAR RJ
R29 $13.00 lmt 4, $16.99 ea
R30 1 @ $13.00 ea 13.00
R31 77033302206 FS HUMMUS TRDTNL RJ 12.49
R32 41-HOME
R33 05870372038 PC ASHWD GRL BRS GPRJ
R34 $7.00 lmt 8, $14.00 ea
R35 1 @ $7.00 ea 7.00
R36 SUBTOTAL 133.56
R37 G=GST 5% 11.99 @ 5.000% 0.60
R38 P=PST 6% 11.99 @ 6.000% 0.72
R39 TOTAL 134.88
R40 Trans. Type: PURCHASE
R41 Account: MASTERCARD CAD$ 134.88
R42 Card Type: CREDIT
R43 Card Number: [illegible] P
R44 [illegible]ateTime: 26/09/21 20:41:43
R45 Ref. #: [illegible]
R46 Auth #: [illegible]
R47 MASTERCARD
R48 A0000000041010 0020008001
R49 00 APPROVED - THANK YOU
R50 Retain this copy for statement
R51 validation
R52 *** CUSTOMER COPY ***
R53 CREDIT TN 134.88
R54 PC Optimum
R55 Points Redeemed 0
R56 Closing Balance [illegible]
R57 99158407923720260921204148
R58 You could have earned at least 1,340
R59 PC Optimum points with a
R60 PC Financial Mastercard or PC Money Account.
R61 Learn more at pcfinancial.ca
R62 ************************************
R63 GST # 12223-5922 RT0001
R64 Your Store Manager is [illegible]
R65 Thank you for shopping at
R66 The Real Canadian Superstore
R67 ************************************
R68 2026/09/21 [illegible] 206 07 9237 20:41
R69 Tell us how we did today! Visit
R70 storeopinion.ca or call 1-800-531-2928
R71 Win a $1,000 PC gift card or
R72 1,000,000 PC Optimum points
R73 Full contest rules on survey website
R74 CODE: 092126 204107 9237 01584
R75 20,000 POINTS
R76 for You!
R77 September 26: THANK
R78 YOU EVENT Get 20,000
R79 Points!
R80 September 26 only. Open PC Optimum app
R81 before you shop to get 20,000 points when
R82 you spend $200 or more.
R83 Offer valid September 26, 2026 only.
```

## B. Receipt fields

| Field | Value |
|---|---|
| Store name | SUPERSTORE {R03} |
| Store address | (2055 PRINCE OF WALES DR) {R03} |
| Date | 2026/09/21 {R68} |
| Time | 20:41 {R68} |
| Subtotal | 133.56 {R36} |
| Total | 134.88 {R39} |

## C. Taxes

| Tax as printed | Amount |
|---|---|
| G=GST 5% 11.99 @ 5.000% {R37} | 0.60 {R37} |
| P=PST 6% 11.99 @ 6.000% {R38} | 0.72 {R38} |

## D. Items

| As printed | Qty | Unit price | Amount | Tax code | Tracker name | Category |
|---|---|---|---|---|---|---|
| NN RICE CRACKERS {R07} | not in source | not in source | 1.49 {R07} | RJ {R07} | not in codebook | not in codebook |
| OIKO YGRT {R09} | 1 {R11} | $4.93 ea {R11} | 4.93 {R11} | RJ {R09} | not in codebook | not in codebook |
| DAIR COTT CHEESE {R12} | not in source | not in source | 7.49 {R12} | RJ {R12} | not in codebook | not in codebook |
| GEGG LARGE {R13} | not in source | not in source | 8.98 {R13} | RJ {R13} | not in codebook | not in codebook |
| NN PINEAPPLE {R15} | not in source | not in source | 16.49 {R15} | RJ {R15} | not in codebook | not in codebook |
| NNNI BLUEBERRIES {R16} | not in source | not in source | 17.99 {R16} | RJ {R16} | not in codebook | not in codebook |
| NN GREEN PEAS CP {R17} | not in source | not in source | 6.79 {R17} | RJ {R17} | not in codebook | not in codebook |
| NN CUT GREEN BEA {R18} | not in source | not in source | 3.79 {R18} | RJ {R18} | not in codebook | not in codebook |
| GG PEACHES N CRM {R19} | not in source | not in source | 3.50 {R19} | RJ {R19} | not in codebook | not in codebook |
| LOVE CRN GRNL {R21} | not in source | not in source | 12.99 {R21} | RJ {R21} | not in codebook | not in codebook |
| QUPA TC SALTED {R22} | not in source | not in source | 4.99 {R22} | GPRJ {R22} | not in codebook | not in codebook |
| GRAPE BLUE 2L {R24} | not in source | not in source | 7.00 {R24} | RJ {R24} | not in codebook | not in codebook |
| APPLE FUJI {R25} | 1.120 kg {R26} | $4.14/kg {R26} | 4.64 {R26} | RJ {R25} | not in codebook | not in codebook |
| OLD CHEDDAR {R28} | 1 {R30} | $13.00 ea {R30} | 13.00 {R30} | RJ {R28} | not in codebook | not in codebook |
| FS HUMMUS TRDTNL {R31} | not in source | not in source | 12.49 {R31} | RJ {R31} | not in codebook | not in codebook |
| PC ASHWD GRL BRS {R33} | 1 {R35} | $7.00 ea {R35} | 7.00 {R35} | GPRJ {R33} | not in codebook | not in codebook |

## E. Coverage ledger

| Line | Reason |
|---|---|
| R01 | no-field |
| R02 | no-field |
| R04 | no-field |
| R05 | no-field |
| R06 | no-field |
| R08 | no-field |
| R10 | no-field |
| R14 | no-field |
| R20 | no-field |
| R23 | no-field |
| R27 | no-field |
| R29 | no-field |
| R32 | no-field |
| R34 | no-field |
| R40 | no-field |
| R41 | no-field |
| R42 | no-field |
| R43 | no-field |
| R44 | no-field |
| R45 | no-field |
| R46 | no-field |
| R47 | no-field |
| R48 | no-field |
| R49 | no-field |
| R50 | no-field |
| R51 | no-field |
| R52 | no-field |
| R53 | no-field |
| R54 | no-field |
| R55 | no-field |
| R56 | no-field |
| R57 | no-field |
| R58 | no-field |
| R59 | no-field |
| R60 | no-field |
| R61 | no-field |
| R62 | no-field |
| R63 | no-field |
| R64 | no-field |
| R65 | no-field |
| R66 | no-field |
| R67 | no-field |
| R69 | no-field |
| R70 | no-field |
| R71 | no-field |
| R72 | no-field |
| R73 | no-field |
| R74 | no-field |
| R75 | no-field |
| R76 | no-field |
| R77 | no-field |
| R78 | no-field |
| R79 | no-field |
| R80 | no-field |
| R81 | no-field |
| R82 | no-field |
| R83 | no-field |
