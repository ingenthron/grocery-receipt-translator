# Grocery receipt translator

Turns a photo of a grocery receipt into a fixed table you can paste into a price-tracking spreadsheet. Every value in it is either printed on the receipt, with the line it came from, or taken from your own codebook, with the entry it came from. Nothing is guessed.

## Set it up (once, about 3 minutes)

1. In claude.ai, create a new Project.
2. Add these files to the Project's knowledge, and nothing else:
   `identity.md`, `rules.md`, `examples.md`, and the four files in `reference/` (`output-schema.md`, `field-definitions.md`, `format-spec.md`, `codebook.md`).
3. In the Project's instructions, paste this line:
   `You are the receipt translator described in identity.md. Follow rules.md and the files in reference/ exactly.`

## Use it

Start a new chat in the Project, attach a photo of one receipt (or paste its text), and send:

`Translate this receipt.`

Photograph the whole receipt, flat, in good light. Cover card numbers and loyalty numbers first if you plan to share the photo.

## What comes back

Always the same five parts, in the same order:

- **A. Source lines:** every printed line, numbered `R01`, `R02` ..., copied as printed. Anything unreadable is `[illegible]`.
- **B. Receipt fields:** store name, address, date, time, subtotal, total.
- **C. Taxes:** each tax line printed.
- **D. Items:** one row per item, deposit, fee or discount: the words as printed, quantity, unit price, amount, tax code, and your tracker name and category from the codebook.
- **E. Coverage ledger:** every line the table does not use, with the reason, so nothing is silently dropped.

`{R08}` after a value means "printed on line R08". `{C014}` means "from codebook entry C014". `not in source` means the receipt does not print it. `not in codebook` means your codebook has no entry for that exact printed text.

If you send something that is not one receipt, you get the same five parts with a status saying why it was not translated.

## Grow your codebook

Receipts print items their own way (`ORG BNNA`, `NN 2% MLK 4L`). The codebook is where you decide, once, what each printed text means in your spreadsheet. After a translation, copy any `not in codebook` item's printed text into a new row of `reference/codebook.md`, give it your name and one of the listed categories, and re-upload the file to the Project. The translator never adds entries itself.

## What it will not do

It will not spell out abbreviations, fix spellings, add anything up, work out a price per kilogram, fill in a missing date, or guess a category. Ask it to, and it replies that the receipt and the codebook do not give that.
