# Reproducing the studies

## What runs from this repository unchanged

`results/` holds every number the article reports. Two scripts consume it:

```bash
python tools/stats_all.py        # contrasts, exact Wilcoxon, Holm, effect sizes, reliability
python tools/verify_article.py   # 325 assertions against the article; exits non-zero on mismatch
```

`tools/build_corpus.py` regenerates the twelve-skill demo corpus and its ground truth from
`tools/fragments_lib.py`. It is seeded, so the output is byte-identical to `corpus/`.

`eval/tasks_synthetic.py` and `eval/tasks_real.py` are the two task suites, with the oracle skill
sets and, for the synthetic suite, the rubric criteria traceable to planted competencies.

## What needs a corpus you supply

The production study read 45 skills that ship with Anthropic's Claude products. Their text is not
here (see `NOTICE`). To rebuild that side of the work you need the same skills installed, then:

```bash
skillmerge discover /path/to/engineering/skills /path/to/public/skills /path/to/example/skills
python - <<'PY'
import json
man = json.load(open('docs/SKILLS-MANIFEST.json'))['entries']
have = {s['name']: s['sha256'] for s in json.load(open('build/skills.json'))}
same = sum(1 for e in man if have.get(e['name']) == e['sha256'])
print(f"{same} of {len(man)} skills match the versions the study read")
PY
```

A mismatch is expected as those libraries change; the manifest exists so you know whether you are
comparing like with like rather than guessing.

Then `skillmerge jobs`, run the jobs with any agent, and `skillmerge build`.

## What needs agents

Three things in the studies were produced by agent panels and are not deterministic:

1. **Refactoring** each skill into atoms. Prompt in `docs/reformat-prompt.md`, one job per skill.
2. **Expansions** for skill descriptions. Prompt written by `skillmerge jobs`.
3. **Grading and adjudication.** Two independent panels scored every deliverable; eight judges
   adjudicated 120 merge decisions per study. The prompts embed skill text, so they are not here.

Panel agreement was high (weighted kappa 0.913 to 0.940 across the three studies), but agreement is
not correctness, and a rerun with different agents will move the third decimal.

## Calibration protocol

Recorded here because it constrains what the numbers mean.

- The merging threshold for the synthetic study was chosen on six skills and reported on the other
  six.
- Composition hyperparameters were chosen on four development tasks; coverage and ablation figures
  are reported on the remaining eight.
- The abstention floor was calibrated only on in-corpus probes (each skill's own expansions) against
  out-of-corpus probes about cooking, football and gardening. No evaluation task touched it.
- The conjunctive merge rule in the paper's Section 5.3 was fitted on half the adjudication labels
  and reported on the other half.
- Agents that generated expansions and atoms were given only skill text and instructed not to read
  anything else. They had no access to the task suites.
