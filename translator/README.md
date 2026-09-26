# Grocery receipt translator

Turns a photo of a grocery receipt into a fixed table you can paste into a price-tracking spreadsheet. Every value in it is either printed on the receipt, with the line it came from, or taken from your own codebook, with the entry it came from. Nothing is guessed.

## Set it up (once, about 3 minutes)

1. In claude.ai, create a new Project.
2. Add these files to the Project's knowledge, and nothing else:
   `identity.md`, `rules.md`, `examples.md`, and the four files in `reference/` (`output-schema.md`, `field-definitions.md`, `format-spec.md`, `codebook.md`).
3. In the Project's instructions, paste this line:
   `You are the receipt translator described in identity.md. Follow rules.md and the files in reference/ exactly. Begin every reply with "# Receipt translation" and write nothing before it, not even a note that you are reading these files.`

## Use it

Use the most capable Claude model you have (tested on Claude Opus 5.5; on Claude Haiku it ignored these files). Start a new chat in the Project, attach a photo of one receipt (or paste its text), and send:

`Translate this receipt.`

Photograph the whole receipt, flat, in good light. A long receipt reads better as two or three photos of overlapping sections, sent together in one message. Cover card numbers and loyalty numbers first if you plan to share the photo.

## What comes back

Always the same seven parts, in the same order:

- **A. Source lines:** every printed line, numbered `R01`, `R02` ..., copied as printed. Anything unreadable is `[illegible]`.
- **B. Receipt fields:** store name, address, date, time, subtotal, total.
- **C. Taxes:** each tax line printed.
- **D. Items:** one row per item, deposit, fee or discount: the words as printed, quantity, unit price, amount, any price note printed under it (such as a sale and regular price), tax code, and your tracker name and category from the codebook.
- **E. Coverage ledger:** every line the tables do not use (runs of lines as ranges, like `R40-R62`), with the reason, so nothing is silently dropped.
- **F. Spreadsheet rows:** the items again with the date and store on each row, values only, ready to paste into your spreadsheet. Every cell is a copy of a cited cell above it, so each can still be checked.
- **G. Codebook to-do:** the items your codebook does not know yet, with the name and category left empty for you.

`{R08}` after a value means "printed on line R08". `{C014}` means "from codebook entry C014". `not in source` means the receipt does not print it. `not in codebook` means your codebook has no entry for that exact printed text.

If you send something that is not one receipt, you get the same seven parts with a status saying why it was not translated.

## Grow your codebook

Receipts print items their own way (`ORG BNNA`, `NN 2% MLK 4L`). The codebook is where you decide, once, what each printed text means in your spreadsheet. After a translation, section G lists every item your codebook does not know yet. Copy those rows into `reference/codebook.md`, give each the next id, your name and one of the listed categories, and re-upload the file to the Project. The translator never fills in a name itself.

## What it will not do

It will not spell out abbreviations, fix spellings, add anything up, work out a price per kilogram, fill in a missing date, or guess a category. Ask it to, and it replies that the receipt and the codebook do not give that.
