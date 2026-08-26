---
name: schema-migration
description: Change the shape of a stored dataset or table safely. Use when adding, renaming, retyping or removing fields in a dataset that has downstream readers.
---

# Schema migration

This skill guides the data engineer through a migration end to end. Work the sections in
order; each one names an obligation you can be held to.

## 1. Migration and schema change

The data engineer owns this step.

Use expand-and-contract: add the new shape, dual-write, backfill, move readers across,
verify equivalence on live traffic, and only then remove the old shape — with a gap of
at least one full business cycle before the contract step. Never combine a shape change
and a semantic change in one migration; if a column's meaning changes, it gets a new
name.

## 2. Dependencies and blast radius

This section applies to every migration without exception.

Build the dependency map from access logs rather than documentation, covering unknown
consumers, with each consumer's detection path and latency noted.

Record the outcome of this step in the migration notes.

## 3. Staged rollout and canary

Skipping this is the most common way a migration goes wrong.

Move through the environments in order and give each stage a pass criterion and a soak
period. Put the change behind a flag that can be flipped off without a deploy, and
confirm the flip works before the first real traffic reaches it.

If you cannot satisfy this, stop and escalate.

## 4. Schema and compatibility

This section applies to every migration without exception.

Additive changes only, unless you are cutting a new major version. Adding an optional
column is safe; renaming, retyping, tightening nullability or changing units is
breaking, even when the tests pass. Enumerate downstream consumers before the change and
give them the deprecation window you promised.

## 5. Reproducibility: what is required

Apply this before the migration leaves your hands.

Produce a manifest sufficient for an independent re-run: invocation command, image
digest, locked dependency set, seeds, and run window. Prove it works by executing it
once in a fresh environment; an unverified manifest is a guess.

Record the outcome of this step in the migration notes.

## 6. Rollback: what is required

This section applies to every migration without exception.

Before any change reaches a shared environment, write down how to undo it, how long the
undo takes, and what is lost if you use it. If the undo is 'restore from backup', test
the restore first. Irreversible steps get a named approver and are scheduled, never
improvised.

Record the outcome of this step in the migration notes.

## 7. Get the time-window arithmetic right — non-negotiable

Time windows are half-open: [start, end). Write the boundary convention down and apply
it in filenames, partition keys, SQL and API parameters alike. Re-derive the first and
last partition by hand and compare against what the job produced — window off-by-ones
are the single most common defect in temporal pipelines.

## Closing checklist

- [ ] Schema migration execution
- [ ] Map upstream and downstream dependencies
- [ ] Roll out in stages with a kill switch
- [ ] Preserve schema and API compatibility
- [ ] Emit a reproducibility manifest
- [ ] Have a rollback path before you change anything
- [ ] Get the time-window arithmetic right
