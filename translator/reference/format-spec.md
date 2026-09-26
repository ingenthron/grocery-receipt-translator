# Format spec

How values, lines and citations are written. `output-schema.md` says where things go; this file says how each one is written.

## Source lines (section A)

- One entry per non-blank printed line, top to bottom, left to right. Blank space between lines is not a line.
- Each entry is `R` + a two-digit number (`R01`, `R02` ... `R99`, then `R100`), one space, then the line as printed.
- Copy every character as printed: same spelling, same case, same abbreviations, same symbols. Runs of spaces may be written as one space.
- Anything that cannot be read, or is covered, is written `[illegible]`, for one character, one word, or the whole line. Never guess a character.
- If you are given receipt text that already says `[redacted]`, copy it as `[redacted]`, like any other printed text.
- A line made only of one repeated symbol (a rule of `*` or `-`) must have exactly the printed count. If you cannot be sure of the count, write the whole line as `[illegible]`: a wrong count is a wrong line. Receipt text you are given (not a photo) is copied exactly as given, rules included.
- A receipt that continues past the edge of the photo ends at the last line the photo shows.
- A long receipt may come as up to three photos of overlapping sections. Transcribe it once, top to bottom: a line that appears in two photos is one source line, written once.

## Values

- A value is one or more whole tokens copied from one source line, exactly as printed. A token is a run of characters between spaces. `3.49` is not a value on a line that prints `13.49` or `3.49GC`; the value there is the whole token `13.49` or `3.49GC`.
- A value never joins text from two lines, never changes case, never expands or corrects anything, and is never computed (no sums, no differences, no unit prices worked out from other numbers).
- If any character of the value is `[illegible]`, the value is `[illegible]`, cited to its line.

## Citations

- A value copied from the receipt ends with a space and the line it came from in braces: `1.88 {R08}`.
- A value taken from the codebook ends with a space and the entry id in braces: `Bananas, organic {C001}`.
- Sentinels (`not in source`, `not in codebook`, `none`) have no citation. `[illegible]` in a value cell is cited to its line.
- Section F has no citations at all: its cells are copies of cells in B and D, which carry them.

## Several values in one cell

Only where `output-schema.md` allows multiple values (Store address, Price note). Each value carries its own citation, and values are separated by ` ; ` (space, semicolon, space):

`1234 ALBERT ST {R02} ; REGINA SK S4P 2Z5 {R03}`

## Rows that span lines

An item row may draw its values from more than one line (a weighed item often prints its name on one line and its weight, price per kilogram and amount on the next). Each value still cites the one line it is on.

## Codebook lookups

- Tracker name and Category come only from `codebook.md`.
- Look up the row's As printed value, without its citation, in the codebook's Printed text column. It must match exactly: same characters, same case, same words in the same order (a run of spaces counts as one space).
- A match fills Tracker name and Category from that entry, both cited to its id. No match: both are `not in codebook`. A partial or near match is no match.
