# Codebook

The translator's dictionary: the only way a word the receipt does not print can reach the output. Each entry maps one exact printed item text to the name and category the price tracker uses. The translator applies entries; it never adds, edits or guesses one. You grow this table yourself, from the items your translations list as `not in codebook`.

Rules for entries:

- Printed text is copied exactly from a receipt: same characters, same case, one space between words.
- Each printed text appears once. Ids are never reused or renumbered.
- Category is one of the categories below, spelled exactly.

Entries C001 to C004 come from the synthetic receipt in `examples.md`, example 1. Entries C005 to C015 come from the real Superstore receipt in this repo (`inputs/heldout-1/`), added after it was translated, the way this table is meant to grow.

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
| C005 | NN RICE CRACKERS | Rice crackers, No Name | Snacks |
| C006 | OIKO YGRT | Oikos yogurt | Dairy & Eggs |
| C007 | DAIR COTT CHEESE | Cottage cheese, Dairyland | Dairy & Eggs |
| C008 | GEGG LARGE | Eggs, large | Dairy & Eggs |
| C009 | NN PINEAPPLE | Pineapple, frozen, No Name | Frozen |
| C010 | NNNI BLUEBERRIES | Blueberries, frozen, Naturally Imperfect | Frozen |
| C011 | NN GREEN PEAS CP | Green peas, frozen, No Name | Frozen |
| C012 | NN CUT GREEN BEA | Cut green beans, frozen, No Name | Frozen |
| C013 | LOVE CRN GRNL | Love Crunch granola | Pantry |
| C014 | APPLE FUJI | Apples, Fuji | Produce |
| C015 | OLD CHEDDAR | Old cheddar | Dairy & Eggs |
