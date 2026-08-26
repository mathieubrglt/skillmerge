---
name: cost-optimization
description: Reduce infrastructure spend on data processing and storage. Use when a budget line is over, when a new large workload is proposed, or during a periodic cost review.
---

# Compute and storage cost reduction

This skill guides the platform engineer through a cost review end to end. Work the
sections in order; each one names an obligation you can be held to.

## 1. Cost reduction search order

The platform engineer owns this step.

Work the list in order of effort-to-saving: delete what nobody reads, apply lifecycle
rules to cold storage, stop recomputing what has not changed, right-size the instances,
and only then optimise the code. Attribute cost per pipeline before you start, because
the intuition about which job is expensive is wrong more often than it is right.

## 2. Dependencies: what is required

The platform engineer owns this step.

Enumerate upstream feeds and downstream consumers, including unofficial ones — read the
access logs, not the docs — and record how and how fast each consumer would detect a
failure.

Record the outcome of this step in the cost review notes.

## 3. Roll out in stages with a kill switch — non-negotiable

This section applies to every cost review without exception.

Move through the environments in order and give each stage a pass criterion and a soak
period. Put the change behind a flag that can be flipped off without a deploy, and
confirm the flip works before the first real traffic reaches it.

Record the outcome of this step in the cost review notes.

## 4. Cost and compute

Estimate cost before launching anything large: scenes x cost-per-scene for compute,
bytes x rate x months for storage, plus egress. Compare against the budget line and get
sign-off past the agreed threshold. A run that finishes and blows the quarter's budget
is a failed run.

## 5. Measure the current state before changing it

Apply this before the cost review leaves your hands.

Record the baseline under matched conditions before changing anything; otherwise the
after-number means nothing.

Record the outcome of this step in the cost review notes.

## 6. Close against an explicit definition of done for this cost review

This section applies to every cost review without exception.

Define done up front as a list of verifiable statements. To close, walk the list and
attach evidence per item. Retro-fitted criteria and uncheckable criteria both invalidate
the closure.

If you cannot satisfy this, stop and escalate.

## 7. Communication and stakeholders

Open with impact, not mechanism: who is affected, over what period, and what they should
do. Keep the technical explanation below that, in one short paragraph. Give a next-
update time whenever the situation is still moving, and never let a stakeholder learn
about a problem from their own dashboard first.

## Closing checklist

- [ ] Cost reduction search order
- [ ] Map upstream and downstream dependencies
- [ ] Roll out in stages with a kill switch
- [ ] Estimate compute and storage cost before running
- [ ] Measure the current state before changing it
- [ ] Close against an explicit definition of done
- [ ] Communicate to stakeholders in their terms
