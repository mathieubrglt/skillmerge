---
name: release-readiness
description: Decide whether a new or updated indicator is ready to publish. Use before a version bump reaches customers, or when signing off a new product surface.
---

# Indicator release readiness

This skill guides the product engineer through a release end to end. Work the sections
in order; each one names an obligation you can be held to.

## 1. Indicator release readiness for this release

This section applies to every release without exception.

Gate the release on: validation signed by someone who did not build it, documentation
that a new user can follow unaided, a version number and a changelog entry that names
the behavioural difference, migration guidance for consumers of the previous version,
and a named owner for the first two weeks of questions.

## 2. Definition of done: what is required

The product engineer owns this step.

Write the completion criteria before starting, as checkable statements, and close the
work by walking them one by one with evidence attached to each. Criteria added after the
fact are rationalisation; criteria that cannot be checked are wishes.

Record the outcome of this step in the release notes.

## 3. Communicate to stakeholders in their terms — non-negotiable

This section applies to every release without exception.

Structure updates as impact first, mechanism second, action third. State when the next
update lands if the matter is open, and always notify before the affected party notices
on their own.

## 4. Rollback and reversibility

This section applies to every release without exception.

Define the reversal path before touching a shared system: the exact undo, its duration,
and its data loss. A backup-restore path counts only if the restore has been exercised.
Irreversible actions need a named approver and a scheduled slot.

## 5. Staged rollout: what is required

Move through the environments in order and give each stage a pass criterion and a soak
period. Put the change behind a flag that can be flipped off without a deploy, and
confirm the flip works before the first real traffic reaches it.

## 6. Monitoring: what is required

Apply this before the release leaves your hands.

Add the freshness, volume and null-rate checks at the same time as the pipeline, not
after the first incident. Alert on the user-visible symptom (stale or wrong data) rather
than on an internal proxy, and route every alert to a named owner with a runbook link.

## 7. Licensing and compliance

Apply this before the release leaves your hands.

Each input's licence is checked before derived content is released — scope over
derivatives, attribution text, embargo. Unclear terms go to legal, not to your own
judgement.

If you cannot satisfy this, stop and escalate.

## 8. Report uncertainty honestly for this release

Skipping this is the most common way a release goes wrong.

Point estimates travel with an uncertainty band and a note on what the band covers and
excludes, plus the dominant error term. Unquantifiable uncertainty is disclosed in
words, not omitted.

If you cannot satisfy this, stop and escalate.

## Closing checklist

- [ ] Indicator release readiness
- [ ] Close against an explicit definition of done
- [ ] Communicate to stakeholders in their terms
- [ ] Have a rollback path before you change anything
- [ ] Roll out in stages with a kill switch
- [ ] Instrument before you need the signal
- [ ] Check data licensing and redistribution rights
- [ ] Report uncertainty honestly
