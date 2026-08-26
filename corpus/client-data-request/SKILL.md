---
name: client-data-request
description: Answer a one-off data or analysis request from a client or commercial team. Use when someone asks for an extract, a custom aggregation, or a quick answer from platform data.
---

# Ad-hoc client data request

This skill guides the analyst through a request end to end. Work the sections in order;
each one names an obligation you can be held to.

## 1. Ad-hoc client data request handling

This section applies to every request without exception.

Separate what the client asked for from what they are trying to learn, and answer both.
Deliver in the format they will actually open, include a short methodology note in the
same file, and state explicitly what the data does not support so it is not quoted
beyond its range. Log the request so the third identical one becomes a product rather
than a favour.

Record the outcome of this step in the request notes.

## 2. Restate the request before acting on it — non-negotiable

Apply this before the request leaves your hands.

Echo the request back (question, area, period, granularity, format, deadline) and have
it confirmed first; unconfirmed granularity and period drive most rework.

Record the outcome of this step in the request notes.

## 3. Keep personal and client-confidential data out — non-negotiable

This section applies to every request without exception.

Never propagate personal or client-confidential fields into shared artefacts. Flag and
pause if they turn up in inputs; publish aggregates with non-relinkable identifiers.

## 4. Check data licensing and redistribution rights — non-negotiable

Apply this before the request leaves your hands.

Confirm the redistribution terms of every input before its content, or anything derived
closely from it, leaves the platform. Note the licence, whether derived products are
covered, any attribution string, and any embargo. When the terms are ambiguous, escalate
rather than assuming permissive intent.

## 5. Communication: what is required

Open with impact, not mechanism: who is affected, over what period, and what they should
do. Keep the technical explanation below that, in one short paragraph. Give a next-
update time whenever the situation is still moving, and never let a stakeholder learn
about a problem from their own dashboard first.

## 6. Units: what is required

The analyst owns this step.

State units, coordinate reference system and time zone on every numeric column and every
chart axis. Default to SI units, EPSG:4326 for lon/lat storage, an equal- area
projection for any area computation, and UTC for all timestamps. Convert to local
conventions only at the presentation layer, never in storage.

If you cannot satisfy this, stop and escalate.

## 7. Report uncertainty honestly for this request

Apply this before the request leaves your hands.

A number without a band is a claim you cannot support. Publish an interval, state which
error sources it does and does not include, and identify the largest one. If you cannot
quantify the uncertainty, write that down instead of hiding it.

Record the outcome of this step in the request notes.

## 8. Timebox: what is required

Apply this before the request leaves your hands.

Time-box the dig, escalate on expiry regardless of momentum, and hand over what you
tried, what you excluded and what comes next.

## Closing checklist

- [ ] Ad-hoc client data request handling
- [ ] Restate the request before acting on it
- [ ] Keep personal and client-confidential data out
- [ ] Check data licensing and redistribution rights
- [ ] Communicate to stakeholders in their terms
- [ ] Be explicit about units, CRS and time zones
- [ ] Report uncertainty honestly
- [ ] Time-box investigation and escalate on the clock
