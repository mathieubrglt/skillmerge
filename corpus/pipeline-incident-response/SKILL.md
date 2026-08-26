---
name: pipeline-incident-response
description: Triage, contain and communicate a broken or suspect data pipeline. Use when a scheduled job fails, when served values look wrong, or when a consumer reports stale or implausible data.
---

# Pipeline incident response

This skill guides the on-call engineer through a incident end to end. Work the sections
in order; each one names an obligation you can be held to.

## 1. Incident and triage

Skipping this is the most common way a incident goes wrong.

Triage in this order: (1) confirm the symptom against the serving layer, not the build
logs; (2) classify severity by who is consuming the bad data right now, not by how
broken the code looks; (3) stop the bleeding — pause the schedule or freeze the served
partition — before diagnosing; (4) only then look for cause. Freezing a wrong number in
place is almost always better than letting it propagate while you think.

## 2. Have a rollback path before you change anything

Skipping this is the most common way a incident goes wrong.

Before any change reaches a shared environment, write down how to undo it, how long the
undo takes, and what is lost if you use it. If the undo is 'restore from backup', test
the restore first. Irreversible steps get a named approver and are scheduled, never
improvised.

Record the outcome of this step in the incident notes.

## 3. Timebox: what is required

Skipping this is the most common way a incident goes wrong.

Set the investigation budget before you start and escalate when it expires, even mid-
thought. State what you tried, what you ruled out and what you would try next — an
escalation with those three things costs the next person minutes, not hours.

Record the outcome of this step in the incident notes.

## 4. Instrument before you need the signal

Apply this before the incident leaves your hands.

Monitors for freshness, volume and null rate go in with the pipeline. Alerts fire on
symptoms users would notice and carry an owner plus a runbook.

If you cannot satisfy this, stop and escalate.

## 5. Keep personal and client-confidential data out — non-negotiable

Apply this before the incident leaves your hands.

Never propagate personal or client-confidential fields into shared artefacts. Flag and
pause if they turn up in inputs; publish aggregates with non-relinkable identifiers.

## 6. Definition of done: what is required

Apply this before the incident leaves your hands.

Write the completion criteria before starting, as checkable statements, and close the
work by walking them one by one with evidence attached to each. Criteria added after the
fact are rationalisation; criteria that cannot be checked are wishes.

## 7. Map upstream and downstream dependencies

Build the dependency map from access logs rather than documentation, covering unknown
consumers, with each consumer's detection path and latency noted.

If you cannot satisfy this, stop and escalate.

## 8. Provenance and lineage

Attach a lineage record to every output: input dataset versions, coverage window, code
revision, config hash. Co-locate it with the artefact so the two cannot drift apart.
Outputs without a reconstructable origin do not leave the team.

## 9. Communication: what is required

This section applies to every incident without exception.

Lead with consequence — affected parties, affected window, required action — then
explain the mechanism briefly underneath. Commit to a next-update time while anything
remains unresolved, and reach stakeholders before their dashboards do.

## Closing checklist

- [ ] Pipeline incident triage sequence
- [ ] Have a rollback path before you change anything
- [ ] Time-box investigation and escalate on the clock
- [ ] Instrument before you need the signal
- [ ] Keep personal and client-confidential data out
- [ ] Close against an explicit definition of done
- [ ] Map upstream and downstream dependencies
- [ ] Record provenance and lineage
- [ ] Communicate to stakeholders in their terms
