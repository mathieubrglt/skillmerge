# -*- coding: utf-8 -*-
"""Evaluation task suite.

Each task is a realistic work request in the corpus domain. `oracle_skills` is the
set of corpus skills a human would load. `rubric` items are checkable criteria; those
carrying a `fragment` are traceable to a ground-truth competency, which lets us
measure competency coverage independently of prose quality.
"""

TASKS = [
dict(id="T01", oracle_skills=["pipeline-incident-response","qa-validation-report","client-data-request"],
 prompt=("Our Cushing crude-inventory indicator printed a +12% week-on-week jump this morning. "
   "A large client has emailed asking whether it is real before they trade on it. The satellite "
   "acquisition over the last five days was unusually cloudy. Decide what to do and draft the reply "
   "you would send the client."),
 rubric=[
  dict(fragment="U-incident", c="Checks the served/published value against the source before responding, rather than reasoning only from the pipeline code or logs"),
  dict(fragment="U-incident", c="Considers containing the number (freezing, flagging or withholding the print) before completing root-cause analysis"),
  dict(fragment="C-cloudmask", c="Treats the cloudy period as reduced observation count rather than as real signal, and asks for coverage/observation-count per data point"),
  dict(fragment="T-uncertainty", c="Gives the client an uncertainty band or explicitly states that the move is within/outside the noise, rather than a bare number"),
  dict(fragment="T-stakeholder", c="Client reply leads with impact and what the client should do, with mechanism secondary"),
  dict(fragment="T-stakeholder", c="Commits to a specific next-update time while the matter is unresolved"),
  dict(fragment="C-timebox", c="Sets a time budget for investigation and an escalation point"),
  dict(fragment="T-provenance", c="Identifies the specific input scenes/versions and processing revision behind the suspect print"),
  dict(fragment=None, c="Does not assert the move is real or fake without evidence; distinguishes what is known from what is suspected"),
  dict(fragment=None, c="The drafted client reply is actually written out, not merely described"),
 ]),

dict(id="T02", oracle_skills=["backfill-planning","qa-validation-report"],
 prompt=("We found a bug in the cloud-mask threshold used by the gas-flaring indicator. It has been wrong "
   "since January 2023. Write the plan to reprocess the affected history and republish."),
 rubric=[
  dict(fragment="U-backfill", c="Backfill tasks are idempotent and independently retryable, with staging-then-atomic-swap rather than in-place mutation"),
  dict(fragment="U-backfill", c="States and justifies an ordering (newest-first vs oldest-first) and throttles against the live schedule"),
  dict(fragment="C-window", c="States a half-open [start, end) boundary convention and checks the edge partitions explicitly"),
  dict(fragment="C-cost", c="Estimates compute/storage cost of the reprocessing before running it"),
  dict(fragment="C-baseline", c="Captures the pre-change values so the old-vs-new difference can be quantified"),
  dict(fragment="T-rollback", c="Defines how to revert to the previous published series, including what is lost"),
  dict(fragment="T-repro", c="Produces a re-run manifest (command, image/deps, seeds, window) or equivalent pinning"),
  dict(fragment="T-provenance", c="Records input versions and code revision alongside republished outputs"),
  dict(fragment="T-stakeholder", c="Plans a restatement notice to affected consumers"),
  dict(fragment=None, c="Recognises that republishing history is itself a breaking event for consumers who stored the old values"),
 ]),

dict(id="T03", oracle_skills=["sensor-ingest-onboarding","data-license-compliance","benchmark-design"],
 prompt=("A SAR data vendor is pitching us their constellation as a replacement for our current radar source. "
   "Produce the evaluation plan we should run before committing."),
 rubric=[
  dict(fragment="U-onboard", c="Measures actual latency distribution rather than the advertised revisit/latency"),
  dict(fragment="U-onboard", c="Runs a parallel/overlap period against the incumbent and quantifies the level shift before switchover"),
  dict(fragment="U-onboard", c="Asks about the vendor's restatement policy and their own quality flags"),
  dict(fragment="T-licensing", c="Checks whether the licence covers derived and aggregated products, attribution and embargo"),
  dict(fragment="U-benchmark", c="Fixes the acceptance metric and threshold before seeing results, and names the result that would kill the deal"),
  dict(fragment="C-goldenset", c="Uses a frozen reference/golden set for the comparison"),
  dict(fragment="T-units", c="Pins down units, CRS/resolution and timestamp conventions of the new feed"),
  dict(fragment="C-monitor", c="Plans freshness/volume/null-rate monitoring for the new feed from the start"),
  dict(fragment="T-assumptions", c="Lists load-bearing assumptions with owners"),
  dict(fragment=None, c="Plan is sequenced and has a decision point, not just a list of concerns"),
 ]),

dict(id="T04", oracle_skills=["api-change-review","schema-migration"],
 prompt=("A team wants to rename the public API field `volume_bbl` to `volume` and switch its unit to cubic "
   "metres in the same release. Review the proposal."),
 rubric=[
  dict(fragment="C-schemacompat", c="Identifies the rename AND the unit change as separately breaking, not merely as a rename"),
  dict(fragment="C-schemacompat", c="Requires a major version bump or an additive path, and a deprecation window for the old field"),
  dict(fragment="U-schema", c="Rejects combining a shape change with a semantic change; requires the new meaning to get a new name"),
  dict(fragment="C-deps", c="Enumerates downstream consumers from access logs rather than documentation, including unknown ones"),
  dict(fragment="T-units", c="Notes that unit must be explicit in the field name, schema or response metadata"),
  dict(fragment="C-staged", c="Proposes staged rollout behind a flag with pass criteria"),
  dict(fragment="T-rollback", c="Defines the revert path for a public contract change"),
  dict(fragment="U-apireview", c="Treats the public name as a long-lived commitment and checks edge behaviour (empty, partial, future)"),
  dict(fragment=None, c="Gives a clear verdict rather than only listing considerations"),
  dict(fragment=None, c="Notes the silent-corruption risk: consumers that keep parsing successfully but now read the wrong magnitude"),
 ]),

dict(id="T05", oracle_skills=["cost-optimization"],
 prompt=("Our object-storage bill for the imagery archive doubled quarter on quarter and finance wants it back "
   "under the previous run rate. Produce the plan."),
 rubric=[
  dict(fragment="U-cost", c="Attributes cost per pipeline/bucket before acting, rather than guessing which job is expensive"),
  dict(fragment="U-cost", c="Works cheapest-effort-first: delete unread data, lifecycle/tier cold data, stop recomputation, right-size, then optimise code"),
  dict(fragment="C-baseline", c="Establishes the current baseline under conditions that can be re-measured after"),
  dict(fragment="C-cost", c="Quantifies expected saving per action against the budget line, including egress"),
  dict(fragment="C-deps", c="Checks who consumes the data before deleting or tiering it"),
  dict(fragment="C-staged", c="Applies changes in stages with a reversible first step"),
  dict(fragment="T-stakeholder", c="Reports back to finance in terms of run rate and timeline, not internal mechanism"),
  dict(fragment="T-dod", c="Defines verifiable completion criteria for the cost target"),
  dict(fragment=None, c="Distinguishes one-off deletions from structural run-rate reduction"),
 ]),

dict(id="T06", oracle_skills=["model-retraining","benchmark-design"],
 prompt=("We have 40k new labelled flaring sites from West Africa. Plan the retraining of the flare-detection "
   "model and how we decide whether to ship it."),
 rubric=[
  dict(fragment="U-retrain", c="Splits by time AND by site/geography, explicitly rejecting random splits because of spatial/temporal leakage"),
  dict(fragment="U-retrain", c="Freezes the evaluation set before touching training data"),
  dict(fragment="U-retrain", c="Compares candidate vs incumbent on the same frozen set and inspects per-stratum deltas, not just the aggregate"),
  dict(fragment="C-significance", c="Checks the improvement against run-to-run variance / uses paired comparison and reports n"),
  dict(fragment="C-goldenset", c="Uses a versioned frozen golden set with isolated, justified updates"),
  dict(fragment="C-baseline", c="Measures the incumbent under matched conditions"),
  dict(fragment="T-repro", c="Pins seeds, image and dependency versions so the training run can be repeated"),
  dict(fragment="T-licensing", c="Checks that the label/imagery licence permits model training and derived-product release"),
  dict(fragment="T-uncertainty", c="Reports accuracy with intervals, not point estimates"),
  dict(fragment=None, c="Names an explicit ship / no-ship decision rule"),
 ]),

dict(id="T07", oracle_skills=["client-data-request","data-license-compliance"],
 prompt=("A commercial colleague forwards this from a client: 'Can you send us daily LNG cargo counts out of "
   "Qatar for 2019 to 2024? Excel is fine. Need it Friday.' Handle it."),
 rubric=[
  dict(fragment="C-scoping", c="Restates and confirms the ask: exact definition of 'cargo count', geography, period, granularity, format, deadline"),
  dict(fragment="U-clientreq", c="Separates the literal request from the underlying question the client is trying to answer"),
  dict(fragment="U-clientreq", c="Includes a methodology note in the delivered file itself"),
  dict(fragment="U-clientreq", c="States explicitly what the data does not support, so it is not over-quoted"),
  dict(fragment="T-licensing", c="Checks redistribution rights before sending underlying or closely-derived data externally"),
  dict(fragment="T-units", c="Fixes time zone and date-boundary convention for 'daily' counts"),
  dict(fragment="T-uncertainty", c="Conveys uncertainty/coverage rather than implying an exact census"),
  dict(fragment="T-pii", c="Avoids putting client-identifying or personal detail into shared systems"),
  dict(fragment="C-timebox", c="Sets a turnaround plan against the Friday deadline with an escalation point"),
  dict(fragment=None, c="Logs/flags the request as a candidate for productisation if repeated"),
 ]),

dict(id="T08", oracle_skills=["benchmark-design","qa-validation-report"],
 prompt=("Design the benchmark that decides whether our new methane plume quantification method replaces the "
   "current one."),
 rubric=[
  dict(fragment="U-benchmark", c="Fixes metric and acceptance threshold before results are seen"),
  dict(fragment="U-benchmark", c="Includes negative/adversarial cases, not only the happy path"),
  dict(fragment="U-benchmark", c="Holds out a set nobody tunes against, and states what result would cause abandonment"),
  dict(fragment="U-qa", c="Stratifies agreement by the dimensions that matter (magnitude, geography, season) rather than reporting only pooled agreement"),
  dict(fragment="U-qa", c="States a domain of validity and shows failure cases"),
  dict(fragment="C-significance", c="Checks the difference against noise, uses paired comparison, reports n"),
  dict(fragment="T-uncertainty", c="Reports intervals and names the dominant error source"),
  dict(fragment="T-repro", c="Benchmark is re-runnable: pinned data version, code revision, seeds"),
  dict(fragment="T-units", c="Pins the physical units and the reference quantity being compared"),
  dict(fragment=None, c="Ties the benchmark to the decision it informs rather than generic accuracy maximisation"),
 ]),

dict(id="T09", oracle_skills=["release-readiness","qa-validation-report"],
 prompt=("The European gas storage indicator is about to go from v2 to v3, with a methodology change that "
   "shifts levels by a few percent. Decide whether it is ready to publish and what must accompany it."),
 rubric=[
  dict(fragment="U-release", c="Requires validation signed off by someone who did not build it"),
  dict(fragment="U-release", c="Requires a version number and changelog naming the behavioural difference, plus migration guidance for v2 consumers"),
  dict(fragment="U-release", c="Names an owner for post-release questions"),
  dict(fragment="C-staged", c="Stages the rollout with pass criteria and a kill switch"),
  dict(fragment="C-monitor", c="Has freshness/volume/null-rate monitoring and symptom-level alerts in place at release"),
  dict(fragment="T-rollback", c="Defines the revert to v2 including what is lost"),
  dict(fragment="T-stakeholder", c="Notifies consumers before they see the shift in their own dashboards"),
  dict(fragment="T-uncertainty", c="Characterises the level shift with uncertainty rather than a single percentage"),
  dict(fragment="T-dod", c="Closes against explicit, verifiable release criteria with evidence"),
  dict(fragment=None, c="Gives a ready / not-ready verdict with conditions"),
 ]),

dict(id="T10", oracle_skills=["schema-migration","api-change-review"],
 prompt=("We need to add `vessel_imo` to the cargo table and split the existing `port` string into "
   "`port_code` and `port_name`. The table has downstream readers we do not fully know. Write the migration."),
 rubric=[
  dict(fragment="U-schema", c="Uses expand-and-contract: add, dual-write, backfill, migrate readers, verify, then contract"),
  dict(fragment="U-schema", c="Leaves a gap of at least one full business cycle before the contract step"),
  dict(fragment="C-deps", c="Discovers unknown consumers from access logs rather than documentation"),
  dict(fragment="C-schemacompat", c="Treats adding optional columns as safe and splitting/removing `port` as breaking, with a deprecation window"),
  dict(fragment="C-staged", c="Promotes through environments with per-stage pass criteria and soak time"),
  dict(fragment="C-window", c="Handles the backfill window boundaries explicitly"),
  dict(fragment="T-rollback", c="Rollback path defined and rehearsed, with data-loss cost stated"),
  dict(fragment="T-repro", c="Migration is re-runnable/idempotent with pinned tooling"),
  dict(fragment=None, c="Verifies equivalence on live traffic before removing the old column"),
 ]),

dict(id="T11", oracle_skills=["data-license-compliance","client-data-request"],
 prompt=("Marketing wants to publish a blog post with a chart built from our vessel-tracking indicator, which "
   "is derived from a licensed AIS feed. Can we? Write the assessment."),
 rubric=[
  dict(fragment="U-license", c="Reads the signed licence text rather than the vendor's marketing/website terms"),
  dict(fragment="U-license", c="Checks whether the grant covers derivative and aggregated products specifically"),
  dict(fragment="U-license", c="Checks attribution wording and where it must appear, plus territorial/sectoral restrictions and survival after termination"),
  dict(fragment="U-license", c="Records the assessment with its date and the contract version, noting vendors revise terms"),
  dict(fragment="T-licensing", c="Escalates ambiguity to legal instead of assuming permissive intent"),
  dict(fragment="T-pii", c="Considers whether vessel/operator-level detail identifies a counterparty and aggregates accordingly"),
  dict(fragment="T-provenance", c="Records which input versions the published chart derives from"),
  dict(fragment="C-scoping", c="Pins down exactly what will be published: granularity, period, geography, format"),
  dict(fragment=None, c="Gives a conditional yes/no with the specific conditions, not a generic 'check with legal'"),
 ]),

dict(id="T12", oracle_skills=["pipeline-incident-response","release-readiness"],
 prompt=("The nightly job producing the copper smelting indicator has failed silently for three nights. Nobody "
   "noticed until a client asked why the series stopped. Handle it and make sure it cannot recur."),
 rubric=[
  dict(fragment="U-incident", c="Confirms symptom at the serving layer and classifies severity by who is consuming the stale data now"),
  dict(fragment="U-incident", c="Stops the bleeding (pause/freeze/flag) before completing root cause"),
  dict(fragment="C-monitor", c="Adds freshness/volume/null-rate monitoring alerting on the user-visible symptom, not an internal proxy"),
  dict(fragment="C-monitor", c="Routes alerts to a named owner with a runbook link"),
  dict(fragment="C-timebox", c="Time-boxes the investigation with an escalation trigger"),
  dict(fragment="T-stakeholder", c="Notifies affected consumers proactively with impact, window and next update time"),
  dict(fragment="C-deps", c="Maps who consumed the stale series and how they would have detected it"),
  dict(fragment="T-dod", c="Defines verifiable criteria for 'cannot recur', not just an intention"),
  dict(fragment="T-provenance", c="Identifies the affected partitions/versions precisely"),
  dict(fragment=None, c="Treats 'failed silently' as the primary defect, above the job failure itself"),
 ]),
]

if __name__ == "__main__":
    from collections import Counter
    n = sum(len(t["rubric"]) for t in TASKS)
    frag = Counter(r["fragment"] for t in TASKS for r in t["rubric"] if r["fragment"])
    print(f"{len(TASKS)} tasks, {n} rubric items, {sum(1 for t in TASKS for r in t['rubric'] if r['fragment'])} fragment-traceable, {len(frag)} distinct fragments covered")
    print("oracle skill counts:", Counter(s for t in TASKS for s in t["oracle_skills"]))
