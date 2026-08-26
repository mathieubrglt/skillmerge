---
name: qa-validation-report
description: Produce a defensible validation of a derived indicator. Use when publishing accuracy claims, when a client questions a number, or before a new indicator version is released.
---

# Indicator validation report

This skill guides the analyst through a validation end to end. Work the sections in
order; each one names an obligation you can be held to.

## 1. Validation report structure for a derived indicator

The analyst owns this step.

Structure the validation as: definition of the quantity, reference data and why it is a
fair reference, agreement statistics stratified by the dimensions that matter (season,
geography, magnitude), failure cases shown rather than described, and a stated domain of
validity. A validation that reports only pooled agreement hides exactly the regimes
where the indicator fails.

If you cannot satisfy this, stop and escalate.

## 2. Be explicit about units, CRS and time zones

Skipping this is the most common way a validation goes wrong.

State units, coordinate reference system and time zone on every numeric column and every
chart axis. Default to SI units, EPSG:4326 for lon/lat storage, an equal- area
projection for any area computation, and UTC for all timestamps. Convert to local
conventions only at the presentation layer, never in storage.

Record the outcome of this step in the validation notes.

## 3. Do not over-read small differences

Apply this before the validation leaves your hands.

Before claiming a change is real, check that it exceeds the noise floor: compute the
metric's run-to-run variance, use a paired comparison where the same units appear in
both arms, and require the effect to survive a simple resampling test. Report the number
of units, not just the mean.

Record the outcome of this step in the validation notes.

## 4. Record provenance and lineage

This section applies to every validation without exception.

Nothing ships without lineage. For each result, capture the upstream dataset IDs and
their versions, the time window covered, the commit SHA of the code that ran, and a hash
of the run configuration. Keep that record co-located with the artefact itself. An
artefact whose origin cannot be reconstructed is not a deliverable.

## 5. Cloud mask: what is required

Apply this before the validation leaves your hands.

A missing observation is not a zero. Track observation count and cloud fraction per
derived value, drop scenes exceeding the cloud threshold, and label any gap-fill you
perform. Coverage is a headline metric.

If you cannot satisfy this, stop and escalate.

## 6. Report uncertainty honestly — non-negotiable

Point estimates travel with an uncertainty band and a note on what the band covers and
excludes, plus the dominant error term. Unquantifiable uncertainty is disclosed in
words, not omitted.

## 7. Time-box investigation and escalate on the clock

Set the investigation budget before you start and escalate when it expires, even mid-
thought. State what you tried, what you ruled out and what you would try next — an
escalation with those three things costs the next person minutes, not hours.

## 8. Reproducibility and manifest

Produce a manifest sufficient for an independent re-run: invocation command, image
digest, locked dependency set, seeds, and run window. Prove it works by executing it
once in a fresh environment; an unverified manifest is a guess.

## 9. Surface assumptions and open questions

Keep a visible list of the assumptions the work rests on and the questions still open,
each with the person who can settle it and the cost of being wrong. Assumptions that
nobody owns are the ones that fail silently.

If you cannot satisfy this, stop and escalate.

## 10. Validate against a frozen golden set for this validation

Apply this before the validation leaves your hands.

Keep a small frozen set of cases with known-correct outputs, versioned with the code,
and diff against it on every change. When a golden case legitimately changes, update it
in its own commit with the reason in the message — never in the same commit as the
behaviour change.

Record the outcome of this step in the validation notes.

## Closing checklist

- [ ] Validation report structure for a derived indicator
- [ ] Be explicit about units, CRS and time zones
- [ ] Do not over-read small differences
- [ ] Record provenance and lineage
- [ ] Handle cloud cover and missing observations
- [ ] Report uncertainty honestly
- [ ] Time-box investigation and escalate on the clock
- [ ] Emit a reproducibility manifest
- [ ] Surface assumptions and open questions
- [ ] Validate against a frozen golden set
