# Provenance of the real inputs

Every receipt here was bought and photographed by the builder, who consents to publishing it in the pseudonymized form below. Assignment (held out or example) was made before Claude Code opened the photo. Examples in `translator/examples.md` are synthetic; no real receipt is used as an example.

## heldout-1

| | |
|---|---|
| Store | Real Canadian Superstore, 2055 Prince of Wales Dr, Regina, Saskatchewan (as printed) |
| Bought | 2026-09-21 (as printed) |
| Photographed | 2026-09-25, Pixel 9 phone camera, on a wooden floor |
| Assigned | Held out, 2026-09-25, before Claude Code opened the photo; opened after translator commit `69e3654` |

**What was changed in `receipt.jpg`, and nothing else:**

- All metadata removed, including the phone's GPS location: the published file is the pixels only, re-saved as JPEG (quality 92).
- Cropped to the receipt (the original is 3072 x 4080; the crop is 990 x 3860 at full resolution, not scaled).
- Six solid black boxes over: the card number (`Card Number:` line, the trailing `P` left visible), the `Ref. #` value, the `Auth #` value, the PC Optimum `Closing Balance` value, the store manager's name, and the cashier's name on the date line.

**Ground truth (`truth.txt`):** drafted by Claude Code from the original photo at full resolution, to be proofread line by line against the paper receipt by the builder. **Status at commit: not yet proofread** (see `runs/LOG.md`). Each boxed value is written `[redacted]`. Printed text inside the two logos (`REAL CANADIAN` / `SUPERSTORE`, `20,000 POINTS` / `for You!`) is transcribed as lines; the barcode and QR code images are not text and are not lines.
