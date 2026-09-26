# Ground-truth cross-check for heldout-1 (2026-09-25, after the deadline)

A second Claude agent (Opus, fresh context) transcribed the original full-resolution photo **blind**, before opening `inputs/heldout-1/truth.txt`, then compared the two line by line and re-examined every disagreement at up to 8x zoom. Its blind transcription is `blind.txt` (private values written `[redacted]`).

- Blind pass against `truth.txt`: 81 of 83 lines identical. Line 19: the blind pass read `BG`; at 8x the glyph matches this receipt's `G`s, not its `B`s, so `truth.txt`'s `GG` stands. Line 43: the blind pass kept the twelve non-private asterisks beside the covered card number; `truth.txt` covers the whole token, a formatting choice.
- Confirmed on closer look: `lmt` (lowercase L) on lines 10, 29 and 34; the faded `D` of `DateTime:` (line 44); each amount on the same printed line as its `@` text (lines 11, 26, 30, 35); 11-digit item codes; 26 barcode digits; nothing printed after `Welcome #`.
- Line 1: a tiny mark after `REAL CANADIAN` (about 8 x 4 pixels) is too small to read as any character; `truth.txt` leaves it out.

**What this is not:** a proofread against the paper. The agent is the same model family as the translator and as the drafter of `truth.txt`, so a misreading all three share would survive it. Only the two asterisk rules (lines 62 and 67) have been checked against the paper, by the builder.
