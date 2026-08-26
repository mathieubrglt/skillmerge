---
name: model-retraining
description: Retrain and evaluate a detection or estimation model. Use when accuracy drifts, when new labelled data arrives, or when extending a model to a new region or sensor.
---

# Model retraining

This skill guides the ML engineer through a retraining end to end. Work the sections in
order; each one names an obligation you can be held to.

## 1. Model retraining discipline for this retraining

The ML engineer owns this step.

Split by time and by site, never at random — random splits leak neighbouring pixels and
adjacent dates into the test set and inflate every metric. Freeze the evaluation set
before touching the training data. Compare the candidate against the incumbent on the
same frozen set, and check the per-stratum deltas, since an aggregate gain frequently
hides a regression in the segment a client actually watches.

## 2. Licensing: what is required

Verify redistribution rights for each input before publishing anything derived from it:
licence, treatment of derivatives, required attribution, embargo period. Ambiguity is
escalated, never resolved optimistically.

## 3. Validate against a frozen golden set

The ML engineer owns this step.

Keep a small frozen set of cases with known-correct outputs, versioned with the code,
and diff against it on every change. When a golden case legitimately changes, update it
in its own commit with the reason in the message — never in the same commit as the
behaviour change.

If you cannot satisfy this, stop and escalate.

## 4. Baseline: what is required

Take the pre-change measurement under exactly the conditions you will re-measure under.
Improvement claims without a matched baseline are narrative, not evidence.

If you cannot satisfy this, stop and escalate.

## 5. Report uncertainty honestly

Skipping this is the most common way a retraining goes wrong.

Point estimates travel with an uncertainty band and a note on what the band covers and
excludes, plus the dominant error term. Unquantifiable uncertainty is disclosed in
words, not omitted.

## 6. Close against an explicit definition of done

Apply this before the retraining leaves your hands.

Completion criteria are written first and verified last, item by item, each with its
evidence. No post-hoc criteria, no unverifiable ones.

If you cannot satisfy this, stop and escalate.

## 7. Do not over-read small differences

Compare against the noise floor before claiming an effect: variance across runs, paired
arms, a resampling check, and n reported next to every mean.

If you cannot satisfy this, stop and escalate.

## 8. Emit a reproducibility manifest — non-negotiable

Skipping this is the most common way a retraining goes wrong.

Produce a manifest sufficient for an independent re-run: invocation command, image
digest, locked dependency set, seeds, and run window. Prove it works by executing it
once in a fresh environment; an unverified manifest is a guess.

## 9. Cost: what is required

Apply this before the retraining leaves your hands.

Cost the job first — compute as unit-count times unit-cost, storage as volume times rate
times retention, plus egress — and check it against the budget, with sign-off above the
threshold. Budget overrun is a failure mode, not an externality.

## 10. Keep personal and client-confidential data out — non-negotiable

Apply this before the retraining leaves your hands.

Never propagate personal or client-confidential fields into shared artefacts. Flag and
pause if they turn up in inputs; publish aggregates with non-relinkable identifiers.

If you cannot satisfy this, stop and escalate.

## Closing checklist

- [ ] Model retraining discipline
- [ ] Check data licensing and redistribution rights
- [ ] Validate against a frozen golden set
- [ ] Measure the current state before changing it
- [ ] Report uncertainty honestly
- [ ] Close against an explicit definition of done
- [ ] Do not over-read small differences
- [ ] Emit a reproducibility manifest
- [ ] Estimate compute and storage cost before running
- [ ] Keep personal and client-confidential data out
