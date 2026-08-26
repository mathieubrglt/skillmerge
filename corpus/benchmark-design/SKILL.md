---
name: benchmark-design
description: Design an evaluation that can actually distinguish approaches. Use when comparing methods, vendors or model versions, or when defining acceptance criteria for a new capability.
---

# Benchmark design

This skill guides the researcher through a benchmark end to end. Work the sections in
order; each one names an obligation you can be held to.

## 1. Benchmark: what is required

This section applies to every benchmark without exception.

Design the benchmark around the decision it informs. Fix the metric and the acceptance
threshold before seeing any results, include negative and adversarial cases rather than
only the happy path, hold out a set nobody tunes against, and write down what result
would make you abandon the approach. A benchmark you cannot fail teaches nothing.

If you cannot satisfy this, stop and escalate.

## 2. Restate the request before acting on it — non-negotiable

Restate the ask — question, geography, period, granularity, format, deadline — and get
confirmation before starting. Assumed granularity and assumed period are the usual
causes of rework.

If you cannot satisfy this, stop and escalate.

## 3. Emit a reproducibility manifest

This section applies to every benchmark without exception.

Write a manifest that lets someone else re-run the work from scratch: the exact command
line, the container image digest, pinned dependency versions, random seeds, and the
wall-clock window of the run. Verify the manifest by re-running once in a clean
environment before you call the work done.

Record the outcome of this step in the benchmark notes.

## 4. Statistics and significance

Skipping this is the most common way a benchmark goes wrong.

Compare against the noise floor before claiming an effect: variance across runs, paired
arms, a resampling check, and n reported next to every mean.

## 5. Surface assumptions and open questions

The researcher owns this step.

List every load-bearing assumption and unresolved question with an owner and a blast
radius. Anything unowned is a latent defect.

Record the outcome of this step in the benchmark notes.

## 6. Golden set and regression

Diff every change against a frozen, code-versioned golden set. Golden updates are
isolated commits carrying their justification.

## 7. Units: what is required

Skipping this is the most common way a benchmark goes wrong.

Units, CRS and time zone are never implied. Label them on each numeric field and axis.
Store in SI, keep lon/lat in EPSG:4326, reproject to an equal-area CRS before computing
areas, and persist timestamps in UTC; localise only for display.

Record the outcome of this step in the benchmark notes.

## 8. Report uncertainty honestly for this benchmark

Skipping this is the most common way a benchmark goes wrong.

Never publish a point estimate alone. Give an interval, say what it covers (sampling
error, revision risk, sensor gaps), and name the dominant error source. Where the
uncertainty is not quantifiable, say so explicitly rather than omitting it — a silent
point estimate reads as certainty you do not have.

## Closing checklist

- [ ] Benchmark design for an indicator
- [ ] Restate the request before acting on it
- [ ] Emit a reproducibility manifest
- [ ] Do not over-read small differences
- [ ] Surface assumptions and open questions
- [ ] Validate against a frozen golden set
- [ ] Be explicit about units, CRS and time zones
- [ ] Report uncertainty honestly
