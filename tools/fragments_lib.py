# -*- coding: utf-8 -*-
"""Ground-truth fragment library for the synthetic skill corpus.

Domain: Earth-observation / commodity-intelligence analytics platform engineering.

Each fragment is one atomic competency. `variants` are surface paraphrases of the
SAME competency; a skill instantiates one variant. This lets us plant exact,
near-duplicate and paraphrased redundancy with known ground truth.

kind: transverse (appears in >=5 skills) | cluster (2-4 skills) | unique (1 skill)
"""

FRAGMENTS = {

# ---------------------------------------------------------------- TRANSVERSE
"T-provenance": dict(kind="transverse", title="Record provenance and lineage",
 tags=["provenance","lineage","audit","traceability","data-quality"],
 variants=[
"""Every artefact you produce must be traceable back to its inputs. Record, for each
output: the source dataset identifiers and versions, the acquisition window, the
processing code revision (git SHA), and the configuration hash. Store this beside
the output, not in a separate wiki page that will drift. If an output cannot state
where it came from, treat it as unpublishable.""",
"""Nothing ships without lineage. For each result, capture the upstream dataset IDs
and their versions, the time window covered, the commit SHA of the code that ran,
and a hash of the run configuration. Keep that record co-located with the artefact
itself. An artefact whose origin cannot be reconstructed is not a deliverable.""",
"""Attach a lineage record to every output: input dataset versions, coverage window,
code revision, config hash. Co-locate it with the artefact so the two cannot drift
apart. Outputs without a reconstructable origin do not leave the team.""",
]),

"T-repro": dict(kind="transverse", title="Emit a reproducibility manifest",
 tags=["reproducibility","manifest","determinism","environment","rerun"],
 variants=[
"""Write a manifest that lets someone else re-run the work from scratch: the exact
command line, the container image digest, pinned dependency versions, random seeds,
and the wall-clock window of the run. Verify the manifest by re-running once in a
clean environment before you call the work done.""",
"""Produce a manifest sufficient for an independent re-run: invocation command,
image digest, locked dependency set, seeds, and run window. Prove it works by
executing it once in a fresh environment; an unverified manifest is a guess.""",
"""Ship a re-run manifest (command, image digest, pinned deps, seeds, run window)
and validate it with one clean-room execution before declaring completion.""",
]),

"T-units": dict(kind="transverse", title="Be explicit about units, CRS and time zones",
 tags=["units","crs","timezone","geospatial","conventions","normalization"],
 variants=[
"""State units, coordinate reference system and time zone on every numeric column
and every chart axis. Default to SI units, EPSG:4326 for lon/lat storage, an equal-
area projection for any area computation, and UTC for all timestamps. Convert to
local conventions only at the presentation layer, never in storage.""",
"""Units, CRS and time zone are never implied. Label them on each numeric field and
axis. Store in SI, keep lon/lat in EPSG:4326, reproject to an equal-area CRS before
computing areas, and persist timestamps in UTC; localise only for display.""",
"""Annotate units, CRS and time zone everywhere. Storage is SI, EPSG:4326 for
coordinates, equal-area for area maths, UTC for time. Local formats belong to the
presentation layer alone.""",
]),

"T-uncertainty": dict(kind="transverse", title="Report uncertainty honestly",
 tags=["uncertainty","confidence-interval","error-bars","statistics","caveats"],
 variants=[
"""Never publish a point estimate alone. Give an interval, say what it covers
(sampling error, revision risk, sensor gaps), and name the dominant error source.
Where the uncertainty is not quantifiable, say so explicitly rather than omitting
it — a silent point estimate reads as certainty you do not have.""",
"""A number without a band is a claim you cannot support. Publish an interval, state
which error sources it does and does not include, and identify the largest one. If
you cannot quantify the uncertainty, write that down instead of hiding it.""",
"""Point estimates travel with an uncertainty band and a note on what the band
covers and excludes, plus the dominant error term. Unquantifiable uncertainty is
disclosed in words, not omitted.""",
]),

"T-stakeholder": dict(kind="transverse", title="Communicate to stakeholders in their terms",
 tags=["communication","stakeholders","summary","clients","reporting"],
 variants=[
"""Open with impact, not mechanism: who is affected, over what period, and what
they should do. Keep the technical explanation below that, in one short paragraph.
Give a next-update time whenever the situation is still moving, and never let a
stakeholder learn about a problem from their own dashboard first.""",
"""Lead with consequence — affected parties, affected window, required action —
then explain the mechanism briefly underneath. Commit to a next-update time while
anything remains unresolved, and reach stakeholders before their dashboards do.""",
"""Structure updates as impact first, mechanism second, action third. State when the
next update lands if the matter is open, and always notify before the affected
party notices on their own.""",
]),

"T-dod": dict(kind="transverse", title="Close against an explicit definition of done",
 tags=["definition-of-done","checklist","completion","verification","handover"],
 variants=[
"""Write the completion criteria before starting, as checkable statements, and close
the work by walking them one by one with evidence attached to each. Criteria added
after the fact are rationalisation; criteria that cannot be checked are wishes.""",
"""Define done up front as a list of verifiable statements. To close, walk the list
and attach evidence per item. Retro-fitted criteria and uncheckable criteria both
invalidate the closure.""",
"""Completion criteria are written first and verified last, item by item, each with
its evidence. No post-hoc criteria, no unverifiable ones.""",
]),

"T-rollback": dict(kind="transverse", title="Have a rollback path before you change anything",
 tags=["rollback","reversibility","risk","safety","change-management"],
 variants=[
"""Before any change reaches a shared environment, write down how to undo it, how
long the undo takes, and what is lost if you use it. If the undo is 'restore from
backup', test the restore first. Irreversible steps get a named approver and are
scheduled, never improvised.""",
"""Define the reversal path before touching a shared system: the exact undo, its
duration, and its data loss. A backup-restore path counts only if the restore has
been exercised. Irreversible actions need a named approver and a scheduled slot.""",
"""No change without a rehearsed undo: the procedure, its runtime, its cost in lost
data. Untested restores do not count. Irreversible steps are approved by name and
scheduled in advance.""",
]),

"T-licensing": dict(kind="transverse", title="Check data licensing and redistribution rights",
 tags=["licensing","compliance","redistribution","legal","terms-of-use"],
 variants=[
"""Confirm the redistribution terms of every input before its content, or anything
derived closely from it, leaves the platform. Note the licence, whether derived
products are covered, any attribution string, and any embargo. When the terms are
ambiguous, escalate rather than assuming permissive intent.""",
"""Verify redistribution rights for each input before publishing anything derived
from it: licence, treatment of derivatives, required attribution, embargo period.
Ambiguity is escalated, never resolved optimistically.""",
"""Each input's licence is checked before derived content is released — scope over
derivatives, attribution text, embargo. Unclear terms go to legal, not to your own
judgement.""",
]),

"T-pii": dict(kind="transverse", title="Keep personal and client-confidential data out",
 tags=["pii","confidentiality","privacy","security","data-handling"],
 variants=[
"""Do not move personal data or client-identifying detail into shared repositories,
tickets, logs or analysis notebooks. If such data appears in a sample you were given,
stop, flag it, and ask for a redacted version. Aggregate before sharing, and prefer
identifiers that cannot be re-linked to an individual or a named counterparty.""",
"""Personal data and client-identifying detail stay out of shared repos, tickets,
logs and notebooks. On encountering it in a supplied sample, halt and request a
redacted copy. Share aggregates, and use identifiers that cannot be re-linked.""",
"""Never propagate personal or client-confidential fields into shared artefacts.
Flag and pause if they turn up in inputs; publish aggregates with non-relinkable
identifiers.""",
]),

"T-assumptions": dict(kind="transverse", title="Surface assumptions and open questions",
 tags=["assumptions","open-questions","ambiguity","scoping","risk"],
 variants=[
"""Keep a visible list of the assumptions the work rests on and the questions still
open, each with the person who can settle it and the cost of being wrong. Assumptions
that nobody owns are the ones that fail silently.""",
"""Maintain an explicit assumptions-and-open-questions list: statement, owner who
can resolve it, and impact if false. Unowned assumptions are the failure mode.""",
"""List every load-bearing assumption and unresolved question with an owner and a
blast radius. Anything unowned is a latent defect.""",
]),

# ------------------------------------------------------------------ CLUSTER
"C-window": dict(kind="cluster", title="Get the time-window arithmetic right",
 tags=["time-window","backfill","boundaries","off-by-one","temporal"],
 variants=[
"""Time windows are half-open: [start, end). Write the boundary convention down and
apply it in filenames, partition keys, SQL and API parameters alike. Re-derive the
first and last partition by hand and compare against what the job produced — window
off-by-ones are the single most common defect in temporal pipelines.""",
"""Use half-open intervals [start, end) consistently across filenames, partitions,
queries and API calls, and record the convention explicitly. Hand-check the first and
last partition against the job's output; boundary errors dominate temporal bugs.""",
"""Adopt [start, end) everywhere and state it. Manually verify the edge partitions
against produced output — off-by-one at the window edges is the modal failure.""",
]),

"C-cloudmask": dict(kind="cluster", title="Handle cloud cover and missing observations",
 tags=["cloud-mask","missing-data","gaps","satellite","coverage"],
 variants=[
"""Distinguish 'no signal' from 'no observation'. Carry an explicit observation-count
and cloud-fraction alongside every derived value, exclude scenes above the agreed
cloud threshold, and never forward-fill across a gap without labelling the filled
points. Report coverage as a first-class metric, not a footnote.""",
"""A missing observation is not a zero. Track observation count and cloud fraction
per derived value, drop scenes exceeding the cloud threshold, and label any gap-fill
you perform. Coverage is a headline metric.""",
"""Separate absence of signal from absence of observation: carry per-value counts and
cloud fraction, apply the cloud threshold, flag interpolated points, and publish
coverage prominently.""",
]),

"C-cost": dict(kind="cluster", title="Estimate compute and storage cost before running",
 tags=["cost","compute","storage","budget","estimation","egress"],
 variants=[
"""Estimate cost before launching anything large: scenes x cost-per-scene for
compute, bytes x rate x months for storage, plus egress. Compare against the budget
line and get sign-off past the agreed threshold. A run that finishes and blows the
quarter's budget is a failed run.""",
"""Cost the job first — compute as unit-count times unit-cost, storage as volume
times rate times retention, plus egress — and check it against the budget, with
sign-off above the threshold. Budget overrun is a failure mode, not an externality.""",
"""Produce a cost estimate (compute, storage, egress) before large runs, compare to
the budget line, and escalate past the agreed ceiling.""",
]),

"C-schemacompat": dict(kind="cluster", title="Preserve schema and API compatibility",
 tags=["schema","compatibility","versioning","api","contract","breaking-change"],
 variants=[
"""Additive changes only, unless you are cutting a new major version. Adding an
optional column is safe; renaming, retyping, tightening nullability or changing units
is breaking, even when the tests pass. Enumerate downstream consumers before the
change and give them the deprecation window you promised.""",
"""Default to additive change; anything else needs a new major version. New optional
fields are safe — renames, type changes, nullability tightening and unit changes are
breaks regardless of green tests. Enumerate consumers first and honour the stated
deprecation window.""",
"""Only additive edits outside a major-version bump. Renames, retypes, nullability
tightening and unit switches are breaking changes. List consumers up front and give
the promised deprecation period.""",
]),

"C-significance": dict(kind="cluster", title="Do not over-read small differences",
 tags=["statistics","significance","sample-size","noise","comparison"],
 variants=[
"""Before claiming a change is real, check that it exceeds the noise floor: compute
the metric's run-to-run variance, use a paired comparison where the same units appear
in both arms, and require the effect to survive a simple resampling test. Report the
number of units, not just the mean.""",
"""Test any claimed difference against run-to-run variance, prefer paired designs so
the same units appear in both arms, and confirm the effect survives resampling. Always
give n alongside the mean.""",
"""Compare against the noise floor before claiming an effect: variance across runs,
paired arms, a resampling check, and n reported next to every mean.""",
]),

"C-goldenset": dict(kind="cluster", title="Validate against a frozen golden set",
 tags=["golden-set","regression","validation","fixtures","ground-truth"],
 variants=[
"""Keep a small frozen set of cases with known-correct outputs, versioned with the
code, and diff against it on every change. When a golden case legitimately changes,
update it in its own commit with the reason in the message — never in the same commit
as the behaviour change.""",
"""Maintain a versioned, frozen fixture set with known-good outputs and diff each
change against it. Legitimate golden updates land in a separate commit whose message
explains the change.""",
"""Diff every change against a frozen, code-versioned golden set. Golden updates are
isolated commits carrying their justification.""",
]),

"C-monitor": dict(kind="cluster", title="Instrument before you need the signal",
 tags=["monitoring","alerting","observability","metrics","sla"],
 variants=[
"""Add the freshness, volume and null-rate checks at the same time as the pipeline,
not after the first incident. Alert on the user-visible symptom (stale or wrong data)
rather than on an internal proxy, and route every alert to a named owner with a
runbook link.""",
"""Ship freshness, volume and null-rate monitors with the pipeline itself. Alert on
user-visible symptoms, not internal proxies, and give each alert a named owner and a
runbook link.""",
"""Monitors for freshness, volume and null rate go in with the pipeline. Alerts fire
on symptoms users would notice and carry an owner plus a runbook.""",
]),

"C-scoping": dict(kind="cluster", title="Restate the request before acting on it",
 tags=["scoping","requirements","clarification","intake","expectations"],
 variants=[
"""Play the request back in your own words: the exact question, the geography, the
period, the granularity, the delivery format and the deadline. Confirm the playback
before doing the work. Most rework traces to a granularity or period that was assumed
rather than agreed.""",
"""Restate the ask — question, geography, period, granularity, format, deadline —
and get confirmation before starting. Assumed granularity and assumed period are the
usual causes of rework.""",
"""Echo the request back (question, area, period, granularity, format, deadline) and
have it confirmed first; unconfirmed granularity and period drive most rework.""",
]),

"C-staged": dict(kind="cluster", title="Roll out in stages with a kill switch",
 tags=["staged-rollout","canary","feature-flag","kill-switch","deployment"],
 variants=[
"""Move through the environments in order and give each stage a pass criterion and a
soak period. Put the change behind a flag that can be flipped off without a deploy,
and confirm the flip works before the first real traffic reaches it.""",
"""Promote through environments in sequence, each with its own pass criterion and
soak time. Gate the change behind a flag that disables without redeploying, and test
that flag before real traffic arrives.""",
"""Stage the rollout with per-stage pass criteria and soak windows, behind a
deploy-free kill switch that you have already exercised.""",
]),

"C-baseline": dict(kind="cluster", title="Measure the current state before changing it",
 tags=["baseline","measurement","before-after","profiling","evidence"],
 variants=[
"""Capture the current numbers first — latency, cost, accuracy, coverage, whichever
the change targets — under the conditions you will re-measure in later. Without a
baseline taken under matched conditions, any improvement you report is a story.""",
"""Take the pre-change measurement under exactly the conditions you will re-measure
under. Improvement claims without a matched baseline are narrative, not evidence.""",
"""Record the baseline under matched conditions before changing anything; otherwise
the after-number means nothing.""",
]),

"C-deps": dict(kind="cluster", title="Map upstream and downstream dependencies",
 tags=["dependencies","blast-radius","consumers","upstream","impact-analysis"],
 variants=[
"""List what feeds this component and what consumes it, including the consumers you
did not build. Query the access logs rather than trusting the documentation, and note
for each consumer how they would notice a failure and how quickly.""",
"""Enumerate upstream feeds and downstream consumers, including unofficial ones —
read the access logs, not the docs — and record how and how fast each consumer would
detect a failure.""",
"""Build the dependency map from access logs rather than documentation, covering
unknown consumers, with each consumer's detection path and latency noted.""",
]),

"C-timebox": dict(kind="cluster", title="Time-box investigation and escalate on the clock",
 tags=["timebox","escalation","triage","prioritisation","stuck"],
 variants=[
"""Set the investigation budget before you start and escalate when it expires, even
mid-thought. State what you tried, what you ruled out and what you would try next —
an escalation with those three things costs the next person minutes, not hours.""",
"""Fix an investigation time budget up front and escalate the moment it runs out,
carrying the attempts, the exclusions and the next hypothesis so the receiver starts
where you stopped.""",
"""Time-box the dig, escalate on expiry regardless of momentum, and hand over what
you tried, what you excluded and what comes next.""",
]),

# ------------------------------------------------------------------- UNIQUE
"U-incident": dict(kind="unique", title="Pipeline incident triage sequence",
 tags=["incident","triage","severity","outage","pipeline"],
 variants=["""Triage in this order: (1) confirm the symptom against the serving layer, not
the build logs; (2) classify severity by who is consuming the bad data right now, not by
how broken the code looks; (3) stop the bleeding — pause the schedule or freeze the
served partition — before diagnosing; (4) only then look for cause. Freezing a wrong
number in place is almost always better than letting it propagate while you think."""]),

"U-backfill": dict(kind="unique", title="Backfill sequencing and idempotency",
 tags=["backfill","idempotency","reprocessing","historical","ordering"],
 variants=["""Backfill newest-first when consumers care about recency, oldest-first when
they care about continuity — decide which and say so. Every backfill task must be
idempotent and independently retryable: write to a staging location, then swap
partitions atomically. Throttle so the backfill never competes with the live schedule,
and checkpoint progress so a killed run resumes rather than restarts."""]),

"U-onboard": dict(kind="unique", title="New sensor feed onboarding checks",
 tags=["onboarding","sensor","new-source","ingest","characterisation"],
 variants=["""Characterise the feed before trusting it: revisit interval and actual latency
distribution (not the advertised one), native resolution and resampling behaviour,
radiometric calibration and known artefacts, the vendor's own quality flags, and their
restatement policy. Run a parallel period against the incumbent source and quantify the
level shift before any switchover."""]),

"U-qa": dict(kind="unique", title="Validation report structure for a derived indicator",
 tags=["validation","qa-report","indicator","evidence","accuracy"],
 variants=["""Structure the validation as: definition of the quantity, reference data and why
it is a fair reference, agreement statistics stratified by the dimensions that matter
(season, geography, magnitude), failure cases shown rather than described, and a stated
domain of validity. A validation that reports only pooled agreement hides exactly the
regimes where the indicator fails."""]),

"U-retrain": dict(kind="unique", title="Model retraining discipline",
 tags=["retraining","model","drift","training-data","leakage"],
 variants=["""Split by time and by site, never at random — random splits leak neighbouring
pixels and adjacent dates into the test set and inflate every metric. Freeze the
evaluation set before touching the training data. Compare the candidate against the
incumbent on the same frozen set, and check the per-stratum deltas, since an aggregate
gain frequently hides a regression in the segment a client actually watches."""]),

"U-apireview": dict(kind="unique", title="Public API change review checklist",
 tags=["api-review","contract","pagination","errors","public-interface"],
 variants=["""Review the change as a permanent commitment: naming you will still defend in
two years, pagination and filtering that work at the largest realistic response, error
bodies that say what the caller should do differently, idempotency for anything that
writes, and explicit behaviour at the edges — empty result, partial data, future date.
Anything shipped publicly is effectively forever."""]),

"U-cost": dict(kind="unique", title="Cost reduction search order",
 tags=["cost-reduction","optimisation","waste","rightsizing","retention"],
 variants=["""Work the list in order of effort-to-saving: delete what nobody reads, apply
lifecycle rules to cold storage, stop recomputing what has not changed, right-size the
instances, and only then optimise the code. Attribute cost per pipeline before you start,
because the intuition about which job is expensive is wrong more often than it is right."""]),

"U-clientreq": dict(kind="unique", title="Ad-hoc client data request handling",
 tags=["client-request","delivery","ad-hoc","turnaround","scope"],
 variants=["""Separate what the client asked for from what they are trying to learn, and
answer both. Deliver in the format they will actually open, include a short methodology
note in the same file, and state explicitly what the data does not support so it is not
quoted beyond its range. Log the request so the third identical one becomes a product
rather than a favour."""]),

"U-schema": dict(kind="unique", title="Schema migration execution",
 tags=["migration","schema-change","expand-contract","dual-write","cutover"],
 variants=["""Use expand-and-contract: add the new shape, dual-write, backfill, move readers
across, verify equivalence on live traffic, and only then remove the old shape — with a
gap of at least one full business cycle before the contract step. Never combine a shape
change and a semantic change in one migration; if a column's meaning changes, it gets a
new name."""]),

"U-benchmark": dict(kind="unique", title="Benchmark design for an indicator",
 tags=["benchmark","evaluation-design","metric","task-suite","protocol"],
 variants=["""Design the benchmark around the decision it informs. Fix the metric and the
acceptance threshold before seeing any results, include negative and adversarial cases
rather than only the happy path, hold out a set nobody tunes against, and write down what
result would make you abandon the approach. A benchmark you cannot fail teaches nothing."""]),

"U-release": dict(kind="unique", title="Indicator release readiness",
 tags=["release","readiness","launch","versioning","announcement"],
 variants=["""Gate the release on: validation signed by someone who did not build it,
documentation that a new user can follow unaided, a version number and a changelog entry
that names the behavioural difference, migration guidance for consumers of the previous
version, and a named owner for the first two weeks of questions."""]),

"U-license": dict(kind="unique", title="Licence and redistribution assessment procedure",
 tags=["licence-review","derivative-works","attribution","contracts","assessment"],
 variants=["""Assess each source separately: the licence text as signed (not the marketing
page), whether the grant covers derivative and aggregated products, attribution wording
and where it must appear, territorial and sectoral restrictions, and the survival clause
after termination. Record the assessment per source with its date and the contract
version, because vendors revise terms silently."""]),
}
