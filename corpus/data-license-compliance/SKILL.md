---
name: data-license-compliance
description: Determine what may be published from a licensed input. Use before releasing derived products, sharing extracts externally, or signing a new data agreement.
---

# Data licence and redistribution review

This skill guides the reviewer through a review end to end. Work the sections in order;
each one names an obligation you can be held to.

## 1. Licence review and derivative works

Skipping this is the most common way a review goes wrong.

Assess each source separately: the licence text as signed (not the marketing page),
whether the grant covers derivative and aggregated products, attribution wording and
where it must appear, territorial and sectoral restrictions, and the survival clause
after termination. Record the assessment per source with its date and the contract
version, because vendors revise terms silently.

## 2. Communication: what is required

Skipping this is the most common way a review goes wrong.

Open with impact, not mechanism: who is affected, over what period, and what they should
do. Keep the technical explanation below that, in one short paragraph. Give a next-
update time whenever the situation is still moving, and never let a stakeholder learn
about a problem from their own dashboard first.

## 3. Record provenance and lineage

Apply this before the review leaves your hands.

Every artefact you produce must be traceable back to its inputs. Record, for each
output: the source dataset identifiers and versions, the acquisition window, the
processing code revision (git SHA), and the configuration hash. Store this beside the
output, not in a separate wiki page that will drift. If an output cannot state where it
came from, treat it as unpublishable.

## 4. Check data licensing and redistribution rights for this review

The reviewer owns this step.

Each input's licence is checked before derived content is released — scope over
derivatives, attribution text, embargo. Unclear terms go to legal, not to your own
judgement.

## 5. Restate the request before acting on it

The reviewer owns this step.

Play the request back in your own words: the exact question, the geography, the period,
the granularity, the delivery format and the deadline. Confirm the playback before doing
the work. Most rework traces to a granularity or period that was assumed rather than
agreed.

## 6. Assumptions and open questions

Skipping this is the most common way a review goes wrong.

Maintain an explicit assumptions-and-open-questions list: statement, owner who can
resolve it, and impact if false. Unowned assumptions are the failure mode.

## 7. Keep personal and client-confidential data out — non-negotiable

This section applies to every review without exception.

Do not move personal data or client-identifying detail into shared repositories,
tickets, logs or analysis notebooks. If such data appears in a sample you were given,
stop, flag it, and ask for a redacted version. Aggregate before sharing, and prefer
identifiers that cannot be re-linked to an individual or a named counterparty.

## Closing checklist

- [ ] Licence and redistribution assessment procedure
- [ ] Communicate to stakeholders in their terms
- [ ] Record provenance and lineage
- [ ] Check data licensing and redistribution rights
- [ ] Restate the request before acting on it
- [ ] Surface assumptions and open questions
- [ ] Keep personal and client-confidential data out
