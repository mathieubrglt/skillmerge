---
name: api-change-review
description: Review a proposed change to a customer-facing API or data contract. Use when adding or altering endpoints, fields, or response semantics that external consumers depend on.
---

# Public API change review

This skill guides the reviewer through a change end to end. Work the sections in order;
each one names an obligation you can be held to.

## 1. Public API change review checklist for this change

Apply this before the change leaves your hands.

Review the change as a permanent commitment: naming you will still defend in two years,
pagination and filtering that work at the largest realistic response, error bodies that
say what the caller should do differently, idempotency for anything that writes, and
explicit behaviour at the edges — empty result, partial data, future date. Anything
shipped publicly is effectively forever.

## 2. Roll out in stages with a kill switch

Skipping this is the most common way a change goes wrong.

Stage the rollout with per-stage pass criteria and soak windows, behind a deploy-free
kill switch that you have already exercised.

## 3. Surface assumptions and open questions for this change

The reviewer owns this step.

Keep a visible list of the assumptions the work rests on and the questions still open,
each with the person who can settle it and the cost of being wrong. Assumptions that
nobody owns are the ones that fail silently.

## 4. Schema and compatibility

Apply this before the change leaves your hands.

Default to additive change; anything else needs a new major version. New optional fields
are safe — renames, type changes, nullability tightening and unit changes are breaks
regardless of green tests. Enumerate consumers first and honour the stated deprecation
window.

## 5. Definition of done and checklist

The reviewer owns this step.

Completion criteria are written first and verified last, item by item, each with its
evidence. No post-hoc criteria, no unverifiable ones.

Record the outcome of this step in the change notes.

## 6. Rollback and reversibility

Before any change reaches a shared environment, write down how to undo it, how long the
undo takes, and what is lost if you use it. If the undo is 'restore from backup', test
the restore first. Irreversible steps get a named approver and are scheduled, never
improvised.

## 7. Dependencies and blast radius

Apply this before the change leaves your hands.

Build the dependency map from access logs rather than documentation, covering unknown
consumers, with each consumer's detection path and latency noted.

If you cannot satisfy this, stop and escalate.

## Closing checklist

- [ ] Public API change review checklist
- [ ] Roll out in stages with a kill switch
- [ ] Surface assumptions and open questions
- [ ] Preserve schema and API compatibility
- [ ] Close against an explicit definition of done
- [ ] Have a rollback path before you change anything
- [ ] Map upstream and downstream dependencies
