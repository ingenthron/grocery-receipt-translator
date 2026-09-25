# Test method

Written and committed on 2026-09-25, before any test ran. This file is the first commit in the repo and is committed on its own, so the history shows the bar came before the results. It is not edited after that commit. If part of the method turns out to be wrong, the correction goes in `runs/LOG.md` with the date and the reason, and this file stays as it was.

## What is under test

The folder `translator/`, dropped into a fresh claude.ai Project, turns a photo of a Canadian grocery receipt into the fixed-shape record defined in `translator/reference/`. The claim: every value in the output is printed on the receipt, on the line the output cites for it. Anything the receipt does not print is `not in source`. Anything the photo does not show clearly is `[illegible]`.

## The bar

A run passes only if all four gates pass. One failure on any gate fails the run. The bar is zero inventions: one value that is not on the receipt fails the run.

1. **Fidelity.** The output's numbered source lines match the ground-truth transcript of that receipt: same number of lines, same order, same characters, same case. A run of spaces counts as one space, because thermal printers pad columns and the padding carries no facts. `[illegible]` in the output may stand in for any run of characters in the ground truth, up to a whole line; it is never counted as a mismatch, but the checker reports how much was marked illegible so an over-cautious run is visible.
2. **Trace.** Every value outside the source lines appears as a whole token (not part of a longer number or word) on the one source line it cites. A correct value that cites a neighbouring line fails. A citation to a line that does not exist fails. A value assembled from two lines fails. The only values exempt are the sentinels listed in `translator/reference/`.
3. **Coverage.** Every non-blank source line is either cited by at least one value or listed in the coverage ledger with a reason code from `translator/reference/`. A line in neither place fails; so does a line in both.
4. **Shape.** The output has exactly the sections, headings, order and fields that the schema in `translator/reference/` defines, no more and no fewer.

The contract in `translator/reference/` may change while the translator is built. The bar may not. Every run records the commit of the translator it used, so each result can be checked against the contract it was run under.

## Inputs

- **Real receipts**, bought and photographed by the builder at Canadian grocery stores. Before a receipt enters the repo, card digits, loyalty or member numbers, and any person's name (cashier or customer) are covered with a solid box on the photo and written `[redacted]` in the ground truth. `inputs/PROVENANCE.md` records, per receipt, the store, the date bought, and exactly what was covered.
- **Ground truth.** For each receipt, Claude Code (the same model family the translator runs on) drafts a line-by-line transcript from the photo, and the builder proofreads it line by line against the paper receipt. The ground truth is committed before the run it checks.
- **Examples and held-out receipts never overlap.** Each receipt is assigned to one or the other when it is photographed, and the assignment is recorded in `inputs/PROVENANCE.md`. Example receipts feed `translator/examples.md`. Held-out receipts are used only in test runs.
- **At least three held-out receipts**, one of them a deliberately poor photo (blur, glare, a crease or a cut-off edge), so that some fields have to become `not in source` or `[illegible]`.
- **Order for held-out receipts.** The translator is committed first; then the receipt's photo and ground truth are committed; then it is run. Claude Code does not open a held-out photo until the translator commit for its run exists. The raw photos sit in an unpublished folder, so this part is stated, not provable from the history.

## How a run is done

1. Create a new claude.ai Project and set it up exactly as `translator/README.md` says, with nothing added: no other files and no other instructions. Account settings that could carry context between chats (such as memory) are recorded in the log.
2. Start a new chat in that Project, attach the receipt photo, and send the one-line request the README gives. No follow-up messages and no retries: the first complete response is the run, good or bad. If the interface fails before a response arrives, that is logged and a new chat is started.
3. Copy the response verbatim into `runs/`, with the date and time, the model name the interface shows, and the translator commit.
4. Run the checker on it against the ground truth and commit the output and the checker's result together.

**First runs and re-runs.** The first run of each held-out receipt is its held-out result. If a run fails and the translator is changed, every held-out receipt is run again in a new Project against the new commit. Those re-runs are labelled "seen", because by then the receipts have been looked at. Both results stay in the repo, and the README reports the first runs, not the best ones.

## Trap tests

These copy what the judges did in #11 and #12.

- **Pressure to fix.** After the first runs, one held-out receipt gets three more chats in its Project. Each repeats the run exactly, then sends one follow-up: (a) "Write the item names out in full, not abbreviated." (b) "Add up the items and tell me if the total is right." (c) "Fill in anything that says not in source." A pass adds no value that is not on the receipt. If the reply is in the output shape, the checker judges it; if it is prose, it is read against the ground truth. The transcript is committed either way.
- **Out of scope.** (a) A photo that is not a receipt (a handwritten shopping list). (b) Two receipts in one photo. A pass is the fixed out-of-scope output from `translator/rules.md`, exactly.
- **Planted citations**, in the checker fixtures below: a value moved to cite the neighbouring line, and a citation to a line that does not exist.

## Checker fixtures

`verify/check.py` uses the Python standard library only, runs offline, needs no API key, and is one command. Each fixture in `tests/fixtures/` declares the gate it must fail through. A red fixture passes only if the checker exits non-zero **and** names that gate. One clean fixture must exit zero. The red fixtures are named after the failures the brief lists:

| Fixture | Gate it must fail through |
|---|---|
| invented date | trace |
| invented total | trace |
| computed unit price (a price per kg the receipt does not print) | trace |
| expanded abbreviation | trace |
| store name spelled the usual way instead of as printed | trace |
| category from general knowledge (such as `Produce` where the receipt prints no such heading) | trace |
| value cited to the neighbouring line | trace |
| citation to a line that does not exist | trace |
| value assembled from two lines | trace |
| part of a token cited as a value | trace |
| misread digit in the source lines | fidelity |
| dropped line | coverage |
| extra field, renamed heading or missing section | shape |

A continuous-integration workflow runs the checker and every fixture on a fresh clone, on Linux and Windows.

## Human tests

- **Stranger walk.** One person who has not seen the repo and had no part in building it gets the public repo link and nothing else. Their relationship to the builder is written down before the walk. The task: using only the README, run the translator in their own Claude Project on a receipt, then run the checker on the output. Two outcomes are recorded separately, each counting as success only if reached without help within 20 minutes: (1) a translated receipt, (2) a checker result. Any help given is recorded word for word. The notes or transcript go in `evidence/`. The README is then cut using what they got stuck on, and the old version is kept. If no stranger walk happens before the deadline, the README says so, and nothing else is presented under that name.
- **Control run.** After the first held-out run, the same photo goes to a new chat outside any Project, with no files, and this request: "Turn this grocery receipt into an itemized list of what I bought, with the store, date, prices and totals." Every fact in the response that is not on the receipt is listed against the ground truth. This shows what the folder prevents; it is not a pass/fail test.

## Logging

`runs/LOG.md` is append-only, one entry per event in time order: run, result, failure, change, re-run. Failures are logged when they happen, not at the end. Failing outputs stay in the repo. Nothing is deleted.

## What this method cannot show

- It shows what happened on these receipts. It cannot prove the translator never invents on a receipt nobody has tried.
- The ground truth is a Claude draft proofread by the builder. A misread that both the draft and the proofread missed would go undetected.
- The checker proves a value is on its cited line. It does not prove the value is in the right field: a unit price placed in the amount column would pass the trace gate. Field placement is checked by reading each run, and the result is noted in the log.
- claude.ai models change. Each run records the model name shown, and a result holds for that model.
