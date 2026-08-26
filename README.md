# SkillMerge

Index a library of Agent Skills once. Return, per request, a single composite skill scoped to one
task and capped at a token budget. Composition on the request path is deterministic and makes no
model call.

The method and its measured limits are in [`paper/article.pdf`](paper/article.pdf). The short
version, from three studies and 156 blind-graded deliverables:

- Composition does **not** improve deliverables. No variant matched or exceeded loading the skills
  a practitioner would have chosen; the shortfall ranged from about 2 rubric points on a corpus
  built to flatter composition to about 12 points on a real library.
- It reduces injected context by 46% to 60%, and it abstains when the library does not cover the
  task.
- **It scales.** Growing the library from 45 to 504 skills leaves composite quality unchanged
  (+0.010, 95% CI [−0.042, +0.074]) and its cost unchanged. Whole-skill loading pays for every
  description in the library on every request, so total per-request context favours composition by
  5.9x at 45 skills and 25x at 500. Obligations available to merge grow as n^1.53.
- Splitting each unit into a general **obligation** and the specific **lesson** that makes it
  actionable raises cross-skill merge precision from 0.067 to 0.817, judged by an independent
  panel. That is what makes a heterogeneous library de-duplicable without losing content.
- Obligations are an index key, not a payload. Printing them costs quality, because a capable model
  already holds them. The composer merges on obligations and emits lessons.

## Install

```bash
git clone https://github.com/mathieubrglt/skillmerge
cd skillmerge
pip install -e ".[mcp]"
npm --prefix tools install          # token counting bridge
```

## Try it on the demo corpus

`corpus/` holds twelve skills written for this project, and `build/` holds an index already built
from them, so this works with no further setup:

```bash
skillmerge compose "our nightly job produced silently wrong totals for days and a customer noticed first"
```

You get a complete `SKILL.md`: each item an obligation, each with the specific knowledge under it,
labelled with the skill it came from.

Ask it something the corpus does not cover and it declines rather than guessing:

```bash
skillmerge compose "review this pull request before I merge it"
# No skill in the library matches this task with enough confidence.
```

The demo corpus is about satellite-derived commodity indicators, so that is the right answer. The
floor is calibrated on in-corpus probes against out-of-corpus ones and catches 14 of 15 negatives
while keeping 95% of positives.

## Point it at your own library

```bash
skillmerge discover /path/to/skills          # -> build/skills.json (metadata and hashes only)
skillmerge jobs                              # -> build/jobs/*.md
# run each job with any agent that can read a file and write JSON
skillmerge build                             # -> build/index.json
skillmerge compose "the task, in the words a person would use"
```

Two steps need a language model and both are offline, once per library change: refactoring each
`SKILL.md` into atoms, and writing trigger phrasings for each skill description so a lexical router
matches the vocabulary people actually type. `skillmerge jobs` writes both as plain prompt files.
Nothing in this repository calls a model itself or needs an API key.

## Serve it over MCP

```bash
cp .mcp.json.example .mcp.json
python -m skillmerge.server                  # stdio
```

| Tool | What it returns |
|---|---|
| `compose_skill_tool` | a task-scoped `SKILL.md` plus token accounting |
| `explain_composition_tool` | the selection trace: routing, confidence, obligations, lesson counts |
| `search_obligations_tool` | one obligation, every skill that imposes it, every lesson |
| `list_skills_tool` | the indexed library |

`search_obligations_tool` is the library-hygiene view. It answers the question a maintainer has and
currently cannot: where do my skills actually overlap?

## How it works

**Atoms.** An obligation is one imperative sentence, in plain verbs with tool and file names
stripped, and it is the only field ever compared between skills. A lesson is the substance: the
reason, the mechanism, the exact command, the paths and gotchas, kept in the source's own words. A
lesson is never merged, never paraphrased, and never dropped when its obligation merges. See
[`docs/atom-spec.md`](docs/atom-spec.md).

**Merging.** A merged atom carries one obligation and every contributing lesson, each labelled with
its source. Merging restates instead of deleting.

**Pinned material.** Code, tables, invocations and anything naming a file that ships with a skill
are never merged or paraphrased, are offered only when their own skill is routed, and are carried
verbatim. Relative paths are resolved and checked against files that exist. On the 45-skill
production library this was 36% of corpus tokens.

**Selection.** An obligation and its best lesson are chosen as one package, so no item ever appears
as a naked checklist entry. Remaining budget buys the other skills' lessons for the same obligation.

**Three guards.** The server abstains when no skill clears a calibrated floor. A composite is capped
at 90% of the cost of the skills it drew on, so composing can never cost more than loading them.
Every emitted reference path is validated.

## Reproducing the paper

`tools/stats_all.py` regenerates every contrast, effect size and reliability coefficient.
`tools/verify_article.py` checks all 325 numbers in the article against `results/` and fails on
mismatch. `tools/scale_analysis.py`, `tools/scale_routing.py` and `tools/scale_cost.py` reproduce
the scaling study, but need the production library's index and atoms and its raw run manifests,
none of which are redistributed; see [`NOTICE`](NOTICE) and
[`docs/reproducing.md`](docs/reproducing.md).

```bash
python tools/verify_article.py
python tools/stats_all.py
```

## Licensing

Code and the demo corpus: MIT ([`LICENSE`](LICENSE)). The paper: CC BY 4.0
([`LICENSE-PAPER`](LICENSE-PAPER)). Skills from other people's libraries are not redistributed
here; [`NOTICE`](NOTICE) says what is absent and why, and `docs/SKILLS-MANIFEST.json` records what
the study read, by content hash.

## Citing

```bibtex
@misc{bourgault2026skillmerge,
  author = {Mathieu Bourgault},
  title  = {Task-Scoped Composition of Agent Skills: Three Strategies Measured
            Against Loading the Whole Skill},
  year   = {2026},
  url    = {https://github.com/mathieubrglt/skillmerge}
}
```
