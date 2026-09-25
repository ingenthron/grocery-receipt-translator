# Run log

Append-only, in time order. One entry per event: run, result, failure, change, re-run. Times are Saskatchewan time (UTC-6). See `TEST_METHOD.md` for the bar.

## 2026-09-25 17:40: correction to TEST_METHOD.md, made before any test ran

**What changed in the contract.** The item table gained two columns, Tracker name and Category, filled only from `translator/reference/codebook.md` (a published table that maps exact printed item text to a name and category) and cited to the codebook entry as `{C001}`, where receipt values are cited to a line as `{R01}`. Decided with the builder at about 17:30, before any contract file, checker or run existed.

**Why the frozen method needs a correction.** Its trace gate says every value appears as a whole token on the source line it cites. A codebook name is not printed on the receipt, so the gate as written would fail every codebook value, including correct ones.

**The correction, and nothing else.** A value cited to a codebook entry `{Cnnn}` passes the trace gate only if all of these hold: (a) entry `Cnnn` exists in `translator/reference/codebook.md`; (b) the same row's As printed value, cited to a receipt line, equals that entry's printed text exactly; (c) the value equals that entry's name or category exactly. A row whose As printed value equals an entry's printed text but whose Tracker name says `not in codebook` also fails. Values cited to receipt lines are checked exactly as frozen. The other three gates are unchanged.

**Fixtures added to the frozen list, all through the trace gate:** codebook name with no matching entry; name taken from a different entry than the one the printed text matches; entry applied when the printed text only partly matches its key; a matching entry missed (`not in codebook` where an entry matches).
