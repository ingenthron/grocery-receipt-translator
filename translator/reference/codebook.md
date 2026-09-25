# Codebook

The translator's dictionary: the only way a word the receipt does not print can reach the output. Each entry maps one exact printed item text to the name and category the price tracker uses. The translator applies entries; it never adds, edits or guesses one. You grow this table yourself, from the items your translations list as `not in codebook`.

Rules for entries:

- Printed text is copied exactly from a receipt: same characters, same case, one space between words.
- Each printed text appears once. Ids are never reused or renumbered.
- Category is one of the categories below, spelled exactly.

The four starter entries come from the synthetic receipt in `examples.md`, example 1.

## Categories

| Category |
|---|
| Produce |
| Dairy & Eggs |
| Meat & Seafood |
| Bakery |
| Pantry |
| Frozen |
| Snacks |
| Beverages |
| Household |
| Personal Care |

## Entries

| Id | Printed text | Tracker name | Category |
|---|---|---|---|
| C001 | ORG BNNA | Bananas, organic | Produce |
| C002 | NN 2% MLK 4L | Milk 2%, 4 L | Dairy & Eggs |
| C003 | LG EGGS 12 | Eggs, large, dozen | Dairy & Eggs |
| C004 | PAPER TOWEL 6RL | Paper towel, 6 rolls | Household |
