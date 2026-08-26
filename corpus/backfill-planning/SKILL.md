---
name: backfill-planning
description: Plan and execute a historical reprocessing run. Use when a fix must be applied to past periods, when a new field needs populating retroactively, or when a vendor restates upstream data.
---

# Backfill planning

This skill guides the pipeline owner through a backfill end to end. Work the sections in
order; each one names an obligation you can be held to.

## 1. Backfill sequencing and idempotency

Backfill newest-first when consumers care about recency, oldest-first when they care
about continuity — decide which and say so. Every backfill task must be idempotent and
independently retryable: write to a staging location, then swap partitions atomically.
Throttle so the backfill never competes with the live schedule, and checkpoint progress
so a killed run resumes rather than restarts.

## 2. Get the time-window arithmetic right

Adopt [start, end) everywhere and state it. Manually verify the edge partitions against
produced output — off-by-one at the window edges is the modal failure.

If you cannot satisfy this, stop and escalate.

## 3. Emit a reproducibility manifest

Produce a manifest sufficient for an independent re-run: invocation command, image
digest, locked dependency set, seeds, and run window. Prove it works by executing it
once in a fresh environment; an unverified manifest is a guess.

## 4. Estimate compute and storage cost before running for this backfill

Apply this before the backfill leaves your hands.

Estimate cost before launching anything large: scenes x cost-per-scene for compute,
bytes x rate x months for storage, plus egress. Compare against the budget line and get
sign-off past the agreed threshold. A run that finishes and blows the quarter's budget
is a failed run.

## 5. Definition of done: what is required

Completion criteria are written first and verified last, item by item, each with its
evidence. No post-hoc criteria, no unverifiable ones.

## 6. Be explicit about units, CRS and time zones — non-negotiable

Apply this before the backfill leaves your hands.

Annotate units, CRS and time zone everywhere. Storage is SI, EPSG:4326 for coordinates,
equal-area for area maths, UTC for time. Local formats belong to the presentation layer
alone.

Record the outcome of this step in the backfill notes.

## 7. Measure the current state before changing it — non-negotiable

This section applies to every backfill without exception.

Capture the current numbers first — latency, cost, accuracy, coverage, whichever the
change targets — under the conditions you will re-measure in later. Without a baseline
taken under matched conditions, any improvement you report is a story.

## 8. Have a rollback path before you change anything — non-negotiable

Apply this before the backfill leaves your hands.

Before any change reaches a shared environment, write down how to undo it, how long the
undo takes, and what is lost if you use it. If the undo is 'restore from backup', test
the restore first. Irreversible steps get a named approver and are scheduled, never
improvised.

If you cannot satisfy this, stop and escalate.

## 9. Provenance: what is required

Apply this before the backfill leaves your hands.

Every artefact you produce must be traceable back to its inputs. Record, for each
output: the source dataset identifiers and versions, the acquisition window, the
processing code revision (git SHA), and the configuration hash. Store this beside the
output, not in a separate wiki page that will drift. If an output cannot state where it
came from, treat it as unpublishable.

## Closing checklist

- [ ] Backfill sequencing and idempotency
- [ ] Get the time-window arithmetic right
- [ ] Emit a reproducibility manifest
- [ ] Estimate compute and storage cost before running
- [ ] Close against an explicit definition of done
- [ ] Be explicit about units, CRS and time zones
- [ ] Measure the current state before changing it
- [ ] Have a rollback path before you change anything
- [ ] Record provenance and lineage
