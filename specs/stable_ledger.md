# Specification — `feed_ledger` module

**Status: specification only. There is no implementation, and you should not write one
until you have written the tests.**

This is the spec-driven / test-driven exercise. Read it, argue with it, fix it, then
write tests from it, then implement.

---

## Purpose

A **ledger** is a written record of things that happened, in order — like a diary or a
log book. A **feed ledger** is a weekly record of what each stable fed its horses.

Every week, each stable sends in a list of lines. Each line records one feeding: which
horse, what it was fed, how much, and who wrote the line down. This module reads that
list, checks that each line is written correctly, and turns it into data the database
can store.

Each line names a **feed code** for what the horse was fed. A feed code is a short code
for a type of food — for example:

| Code | What it means |
|---|---|
| `HAY-STD` | Standard hay |
| `MIX-HIF` | High-fibre mixed feed |

This spec does not keep an official list of codes to check against. It only checks that
a code has the right *shape* (see Field rules below), not that it is a real code a
stable actually uses.

## Input format

One entry per line, pipe-delimited, five fields:

```
<date> | <horse registration> | <feed code> | <quantity> | <submitter initials>
```

Example of a valid line:

```
2026-03-16 | RS-1001 | HAY-STD | 4.5kg | AF
```

## Field rules

| Field | Rule |
|---|---|
| date | ISO `YYYY-MM-DD`. Must be a real calendar date. Must not be in the future relative to a `today` value passed in by the caller. |
| horse registration | `RS-` followed by exactly four digits. Case-insensitive on the prefix; normalise to uppercase. |
| feed code | Two to four uppercase letters, a hyphen, then three uppercase letters. E.g. `HAY-STD`, `MIX-HIF`. |
| quantity | A positive number followed by a unit. Accept `kg`, `g`, `lb`. Normalise to kilograms, rounded to 3 decimal places. Reject zero and negatives. |
| submitter initials | Two or three letters, uppercase after normalisation. |

## Whitespace and separators

- Any amount of whitespace may surround a field or the pipes. Strip it.
- A line with fewer or more than five fields is invalid.
- Blank lines and lines whose first non-whitespace character is `#` are **skipped**,
  not treated as errors.

## Output

`parse_ledger(lines: Iterable[str], today: date) -> LedgerResult`

`LedgerResult` exposes:

- `entries` — a list of valid entries in input order. Each entry has `entry_date`,
  `registration`, `feed_code`, `quantity_kg`, `submitter`.
- `errors` — a list of `(line_number, message)` pairs, 1-based line numbers counting
  every input line including skipped ones.
- `total_kg` — the sum of `quantity_kg` across valid entries, rounded to 3 dp.

## Error behaviour

- **Never raise on bad input data.** A malformed line produces an error entry and
  parsing continues to the next line.
- One error per bad line — the first problem found. Do not report five errors for one
  line.
- Error messages must name the offending field. Callers display these to submitters,
  so "invalid quantity: '4.5 stone'" is useful and "parse error" is not.
- **Do** raise `TypeError` if `lines` is not iterable, or `today` is not a `date`.
  That's a programming error, not a data error, and it should be loud.

## Duplicates

Two entries with the same date **and** registration **and** feed code are a duplicate.
Keep the first; report the second as an error naming the earlier line number.

## Worked examples

Input:
```
# week commencing 2026-03-16
2026-03-16 | RS-1001 | HAY-STD | 4.5kg  | AF

2026-03-16 | rs-1002 | MIX-HIF | 3000g  | bm
2026-03-16 | RS-1001 | HAY-STD | 4.5kg  | AF
2026-03-16 | RS-9999 | HAY-STD | -2kg   | AF
2026-13-01 | RS-1003 | HAY-STD | 4kg    | CA
2026-03-16 | RS-1004 | hay-std | 4kg    | DR
```

Expected: 2 valid entries (lines 2 and 4), `total_kg == 7.5`, and errors on lines 5, 6,
7 and 8 — duplicate, negative quantity, impossible date, lowercase feed code.

> **Note the trap in that example.** Line 5 is a duplicate of line 2 *and* has a
> registration that doesn't match any horse. The spec says one error per line, first
> problem found — so which error do you report? The spec as written does not say
> whether duplicate detection happens before or after field validation. **This is a
> genuine ambiguity and you should fix the spec before writing the test.** Finding it
> is part of the exercise.

## Explicitly out of scope

- Checking the registration against the `horses` table. Format only.
- Anything to do with the database.
- Currency, cost, or supplier.
