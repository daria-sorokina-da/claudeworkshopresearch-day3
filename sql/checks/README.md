# Data-quality checks — your work goes here

One `.sql` file per constraint. Each file starts with a comment naming the constraint
it protects and what a non-empty result means.

Suggested naming: `01_orphan_race_entries.sql`, `02_duplicate_registrations.sql`, …

## Before you write any of them

Ask Claude for the *list* of constraints this schema should enforce but doesn't,
before asking for any SQL. Then write the queries. Then run them.

The order matters: if you ask for queries first, you get queries for the problems
that are easy to imagine, not the ones that are actually there.

## The question to answer at the end

For each problem you found — should it be a **database constraint** (so the bad row
can never be written) or a **validation query** (so you find bad rows already
present)? Usually both, but for different reasons. That judgement is yours, not the
model's.
