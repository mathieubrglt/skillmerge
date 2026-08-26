# -*- coding: utf-8 -*-
"""Render the synthetic skill corpus from the ground-truth fragment library.

Produces corpus/<skill>.md (realistic SKILL.md files) and corpus/ground_truth.json
(which fragment concept, in which surface variant, sits in which skill).
Deterministic: seeded, no wall-clock dependence.
"""
import json, os, random, sys, textwrap
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fragments_lib import FRAGMENTS

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CORPUS = os.path.join(ROOT, "corpus")
SEED = 20260825

SKILLS = {
"pipeline-incident-response": dict(
  title="Pipeline incident response",
  description="Triage, contain and communicate a broken or suspect data pipeline. Use when a scheduled job fails, when served values look wrong, or when a consumer reports stale or implausible data.",
  noun="incident", actor="on-call engineer",
  frags=["U-incident","C-timebox","T-stakeholder","T-provenance","T-rollback","C-monitor","C-deps","T-pii","T-dod"]),
"backfill-planning": dict(
  title="Backfill planning",
  description="Plan and execute a historical reprocessing run. Use when a fix must be applied to past periods, when a new field needs populating retroactively, or when a vendor restates upstream data.",
  noun="backfill", actor="pipeline owner",
  frags=["U-backfill","C-window","C-cost","C-baseline","T-repro","T-provenance","T-rollback","T-units","T-dod"]),
"sensor-ingest-onboarding": dict(
  title="Sensor feed onboarding",
  description="Bring a new satellite or sensor feed into the platform. Use when evaluating a new data vendor, adding a constellation, or replacing an existing source.",
  noun="feed", actor="ingest engineer",
  frags=["U-onboard","C-cloudmask","C-window","C-monitor","T-units","T-provenance","T-licensing","T-pii","T-assumptions"]),
"qa-validation-report": dict(
  title="Indicator validation report",
  description="Produce a defensible validation of a derived indicator. Use when publishing accuracy claims, when a client questions a number, or before a new indicator version is released.",
  noun="validation", actor="analyst",
  frags=["U-qa","C-goldenset","C-significance","C-cloudmask","C-timebox","T-uncertainty","T-units","T-repro","T-provenance","T-assumptions"]),
"model-retraining": dict(
  title="Model retraining",
  description="Retrain and evaluate a detection or estimation model. Use when accuracy drifts, when new labelled data arrives, or when extending a model to a new region or sensor.",
  noun="retraining", actor="ML engineer",
  frags=["U-retrain","C-significance","C-baseline","C-goldenset","C-cost","T-repro","T-uncertainty","T-licensing","T-pii","T-dod"]),
"api-change-review": dict(
  title="Public API change review",
  description="Review a proposed change to a customer-facing API or data contract. Use when adding or altering endpoints, fields, or response semantics that external consumers depend on.",
  noun="change", actor="reviewer",
  frags=["U-apireview","C-schemacompat","C-deps","C-staged","T-rollback","T-assumptions","T-dod"]),
"cost-optimization": dict(
  title="Compute and storage cost reduction",
  description="Reduce infrastructure spend on data processing and storage. Use when a budget line is over, when a new large workload is proposed, or during a periodic cost review.",
  noun="cost review", actor="platform engineer",
  frags=["U-cost","C-cost","C-baseline","C-deps","C-staged","T-stakeholder","T-dod"]),
"client-data-request": dict(
  title="Ad-hoc client data request",
  description="Answer a one-off data or analysis request from a client or commercial team. Use when someone asks for an extract, a custom aggregation, or a quick answer from platform data.",
  noun="request", actor="analyst",
  frags=["U-clientreq","C-scoping","C-timebox","T-uncertainty","T-licensing","T-pii","T-units","T-stakeholder"]),
"schema-migration": dict(
  title="Schema migration",
  description="Change the shape of a stored dataset or table safely. Use when adding, renaming, retyping or removing fields in a dataset that has downstream readers.",
  noun="migration", actor="data engineer",
  frags=["U-schema","C-schemacompat","C-staged","C-deps","C-window","T-rollback","T-repro"]),
"benchmark-design": dict(
  title="Benchmark design",
  description="Design an evaluation that can actually distinguish approaches. Use when comparing methods, vendors or model versions, or when defining acceptance criteria for a new capability.",
  noun="benchmark", actor="researcher",
  frags=["U-benchmark","C-significance","C-goldenset","C-scoping","T-repro","T-uncertainty","T-units","T-assumptions"]),
"release-readiness": dict(
  title="Indicator release readiness",
  description="Decide whether a new or updated indicator is ready to publish. Use before a version bump reaches customers, or when signing off a new product surface.",
  noun="release", actor="product engineer",
  frags=["U-release","C-staged","C-monitor","T-dod","T-stakeholder","T-rollback","T-licensing","T-uncertainty"]),
"data-license-compliance": dict(
  title="Data licence and redistribution review",
  description="Determine what may be published from a licensed input. Use before releasing derived products, sharing extracts externally, or signing a new data agreement.",
  noun="review", actor="reviewer",
  frags=["U-license","C-scoping","T-licensing","T-pii","T-provenance","T-stakeholder","T-assumptions"]),
}

HEAD_TMPL = [
 "{title}",
 "{tag0} and {tag1}",
 "{title} for this {noun}",
 "{tag0}: what is required",
 "{title} — non-negotiable",
]
INTRO_TMPL = [
 "This section applies to every {noun} without exception.",
 "The {actor} owns this step.",
 "Skipping this is the most common way a {noun} goes wrong.",
 "Apply this before the {noun} leaves your hands.",
 "",
]
OUTRO_TMPL = [
 "If you cannot satisfy this, stop and escalate.",
 "Record the outcome of this step in the {noun} notes.",
 "",
 "",
]

def title_case(s):
    return s[0].upper() + s[1:]

def render():
    rng = random.Random(SEED)
    os.makedirs(CORPUS, exist_ok=True)
    gt = {"seed": SEED, "skills": {}, "fragments": {
        fid: {"kind": f["kind"], "title": f["title"], "tags": f["tags"], "n_variants": len(f["variants"])}
        for fid, f in FRAGMENTS.items()}}

    for sid, sk in SKILLS.items():
        frags = list(sk["frags"])
        # unique fragment stays first (it is the skill's raison d'etre); rest shuffled
        rest = frags[1:]
        rng.shuffle(rest)
        ordered = frags[:1] + rest
        lines = []
        lines.append("---")
        lines.append(f"name: {sid}")
        lines.append(f"description: {sk['description']}")
        lines.append("---")
        lines.append("")
        lines.append(f"# {sk['title']}")
        lines.append("")
        lines.append(textwrap.fill(
            f"This skill guides the {sk['actor']} through a {sk['noun']} end to end. "
            f"Work the sections in order; each one names an obligation you can be held to.", 88))
        lines.append("")
        placed = []
        for i, fid in enumerate(ordered, start=1):
            f = FRAGMENTS[fid]
            vi = rng.randrange(len(f["variants"]))
            body = " ".join(f["variants"][vi].split())
            ht = HEAD_TMPL[rng.randrange(len(HEAD_TMPL))]
            heading = ht.format(title=f["title"], tag0=title_case(f["tags"][0].replace("-", " ")),
                                tag1=f["tags"][1].replace("-", " "), noun=sk["noun"])
            lines.append(f"## {i}. {heading}")
            lines.append("")
            intro = INTRO_TMPL[rng.randrange(len(INTRO_TMPL))].format(noun=sk["noun"], actor=sk["actor"])
            if intro:
                lines.append(textwrap.fill(intro, 88)); lines.append("")
            lines.append(textwrap.fill(body, 88))
            lines.append("")
            outro = OUTRO_TMPL[rng.randrange(len(OUTRO_TMPL))].format(noun=sk["noun"])
            if outro:
                lines.append(textwrap.fill(outro, 88)); lines.append("")
            placed.append({"fragment_id": fid, "variant": vi, "section": i, "heading": heading})
        lines.append("## Closing checklist")
        lines.append("")
        for p in placed:
            lines.append(f"- [ ] {FRAGMENTS[p['fragment_id']]['title']}")
        lines.append("")
        text = "\n".join(lines)
        d = os.path.join(CORPUS, sid)
        os.makedirs(d, exist_ok=True)
        with open(os.path.join(d, "SKILL.md"), "w") as fh:
            fh.write(text)
        gt["skills"][sid] = {"title": sk["title"], "description": sk["description"],
                             "actor": sk["actor"], "noun": sk["noun"], "placements": placed}

    with open(os.path.join(CORPUS, "ground_truth.json"), "w") as fh:
        json.dump(gt, fh, indent=2)
    return gt

if __name__ == "__main__":
    gt = render()
    from collections import Counter
    c = Counter(p["fragment_id"] for s in gt["skills"].values() for p in s["placements"])
    print("skills:", len(gt["skills"]), "placements:", sum(c.values()), "distinct fragments:", len(c))
    for k in sorted(c, key=lambda x: -c[x]):
        print(f"  {k:18s} {FRAGMENTS[k]['kind']:10s} in {c[k]} skills")
