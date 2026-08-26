---
name: sensor-ingest-onboarding
description: Bring a new satellite or sensor feed into the platform. Use when evaluating a new data vendor, adding a constellation, or replacing an existing source.
---

# Sensor feed onboarding

This skill guides the ingest engineer through a feed end to end. Work the sections in
order; each one names an obligation you can be held to.

## 1. Onboarding: what is required

Skipping this is the most common way a feed goes wrong.

Characterise the feed before trusting it: revisit interval and actual latency
distribution (not the advertised one), native resolution and resampling behaviour,
radiometric calibration and known artefacts, the vendor's own quality flags, and their
restatement policy. Run a parallel period against the incumbent source and quantify the
level shift before any switchover.

Record the outcome of this step in the feed notes.

## 2. Keep personal and client-confidential data out for this feed

Personal data and client-identifying detail stay out of shared repos, tickets, logs and
notebooks. On encountering it in a supplied sample, halt and request a redacted copy.
Share aggregates, and use identifiers that cannot be re-linked.

Record the outcome of this step in the feed notes.

## 3. Check data licensing and redistribution rights for this feed

Each input's licence is checked before derived content is released — scope over
derivatives, attribution text, embargo. Unclear terms go to legal, not to your own
judgement.

Record the outcome of this step in the feed notes.

## 4. Surface assumptions and open questions — non-negotiable

The ingest engineer owns this step.

Maintain an explicit assumptions-and-open-questions list: statement, owner who can
resolve it, and impact if false. Unowned assumptions are the failure mode.

## 5. Provenance and lineage

Skipping this is the most common way a feed goes wrong.

Attach a lineage record to every output: input dataset versions, coverage window, code
revision, config hash. Co-locate it with the artefact so the two cannot drift apart.
Outputs without a reconstructable origin do not leave the team.

If you cannot satisfy this, stop and escalate.

## 6. Instrument before you need the signal for this feed

Apply this before the feed leaves your hands.

Monitors for freshness, volume and null rate go in with the pipeline. Alerts fire on
symptoms users would notice and carry an owner plus a runbook.

## 7. Time window: what is required

Apply this before the feed leaves your hands.

Use half-open intervals [start, end) consistently across filenames, partitions, queries
and API calls, and record the convention explicitly. Hand-check the first and last
partition against the job's output; boundary errors dominate temporal bugs.

If you cannot satisfy this, stop and escalate.

## 8. Handle cloud cover and missing observations

This section applies to every feed without exception.

Separate absence of signal from absence of observation: carry per-value counts and cloud
fraction, apply the cloud threshold, flag interpolated points, and publish coverage
prominently.

If you cannot satisfy this, stop and escalate.

## 9. Be explicit about units, CRS and time zones for this feed

The ingest engineer owns this step.

Annotate units, CRS and time zone everywhere. Storage is SI, EPSG:4326 for coordinates,
equal-area for area maths, UTC for time. Local formats belong to the presentation layer
alone.

If you cannot satisfy this, stop and escalate.

## Closing checklist

- [ ] New sensor feed onboarding checks
- [ ] Keep personal and client-confidential data out
- [ ] Check data licensing and redistribution rights
- [ ] Surface assumptions and open questions
- [ ] Record provenance and lineage
- [ ] Instrument before you need the signal
- [ ] Get the time-window arithmetic right
- [ ] Handle cloud cover and missing observations
- [ ] Be explicit about units, CRS and time zones
