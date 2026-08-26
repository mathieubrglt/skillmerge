# -*- coding: utf-8 -*-
"""The offline pipeline: discover skills, emit refactoring jobs, build the index.

Two steps need a language model and both happen here, once per library change:

  1. refactoring each SKILL.md into obligation/lesson atoms (docs/reformat-prompt.md)
  2. writing trigger phrasings for each skill description, so a lexical router can match the
     vocabulary a person actually types

Neither runs at request time. `jobs` writes both as plain prompt files, so any agent runner can
execute them; nothing here calls a model itself or requires an API key.
"""
import glob, hashlib, json, os
from .agentskills import read_skill

ROOT_ENV = "SKILLMERGE_ROOTS"


def discover(roots, build_dir="build"):
    """Read every SKILL.md under `roots` and record metadata plus a content hash.

    Only metadata is written. Skill text stays where it is: a library's skills belong to whoever
    wrote them, and this project does not redistribute them.
    """
    skills, seen = [], set()
    for root in roots:
        for p in sorted(glob.glob(os.path.join(root, "**", "SKILL.md"), recursive=True)):
            s = read_skill(os.path.dirname(p))
            if s["name"] in seen:
                continue
            seen.add(s["name"])
            skills.append(dict(name=s["name"], dir=s["dir"],
                               description=s["description"],
                               sections=len(s["fragments"]),
                               assets=len(s["assets"]),
                               sha256=hashlib.sha256(s["raw"].encode("utf-8")).hexdigest()))
    os.makedirs(build_dir, exist_ok=True)
    json.dump(skills, open(os.path.join(build_dir, "skills.json"), "w"), indent=1)
    return skills


def jobs(build_dir="build", prompt_path=None):
    """Write one refactoring prompt per skill, plus one expansion prompt per batch of skills."""
    skills = json.load(open(os.path.join(build_dir, "skills.json")))
    here = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    prompt_path = prompt_path or os.path.join(here, "docs", "reformat-prompt.md")
    spec = open(prompt_path).read()
    jd = os.path.join(build_dir, "jobs")
    os.makedirs(jd, exist_ok=True)
    os.makedirs(os.path.join(build_dir, "atoms"), exist_ok=True)
    for s in skills:
        out = os.path.join(build_dir, "atoms", s["name"] + ".json")
        body = (spec + "\n\n---\n\n## This job\n\n"
                f"Source document: `{os.path.join(s['dir'], 'SKILL.md')}`\n\n"
                f"Write the result as JSON to `{os.path.abspath(out)}` with exactly this shape:\n\n"
                '{"skill": "%s", "atoms": [{"obligation": "...", "lesson": "...", '
                '"kind": "prose"|"pinned", "refs": ["..."], "anchor": "..."}, ...]}\n\n'
                "Read only the source document and this prompt. Validate the JSON parses before "
                "finishing.\n" % s["name"])
        open(os.path.join(jd, f"atoms_{s['name']}.md"), "w").write(body)
    batch = 20
    for i in range(0, len(skills), batch):
        part = skills[i:i + batch]
        listing = "\n".join(f"- {s['name']}: {s['description'][:400]}" for s in part)
        open(os.path.join(jd, f"expansions_{i//batch}.md"), "w").write(
            "You are building a retrieval index over a library of professional skills.\n\n"
            "For EACH skill below write 14 \"expansions\": short phrasings (3-10 words, lowercase, "
            "no punctuation beyond hyphens) of real situations in which a person would need it. "
            "Favour concrete situational vocabulary a requester would actually type: the artefact "
            "they are holding, the symptom they see, the verb they would use, the role they are in. "
            "Vary the wording widely. Do not restate the description.\n\n"
            f"## Skills\n\n{listing}\n\n## Output\n\n"
            f"Write JSON to `{os.path.abspath(os.path.join(build_dir, 'expansions_%d.json' % (i//batch)))}`:\n"
            '[{"name": "<copied exactly>", "expansions": [14 strings]}, ...]\n\n'
            "Cover every skill, in order. Validate the JSON parses.\n")
    return len(skills), (len(skills) + batch - 1) // batch


def collect_expansions(build_dir="build"):
    out = {}
    for p in sorted(glob.glob(os.path.join(build_dir, "expansions_*.json"))):
        try:
            for r in json.load(open(p)):
                out[r["name"]] = r.get("expansions") or []
        except Exception:
            continue
    return out


def skills_meta(build_dir="build"):
    skills = json.load(open(os.path.join(build_dir, "skills.json")))
    exp = collect_expansions(build_dir)
    for s in skills:
        s["expansions"] = exp.get(s["name"], [])
    return skills


def build(build_dir="build", sim_threshold=0.25, cross_skill=True):
    from .index3 import build_index3
    meta = skills_meta(build_dir)
    ix = build_index3(os.path.join(build_dir, "atoms"), meta,
                      sim_threshold=sim_threshold, cross_skill=cross_skill)
    cal = os.path.join(build_dir, "abstain.json")
    if os.path.exists(cal):
        ix["abstain"] = json.load(open(cal))
    json.dump(ix, open(os.path.join(build_dir, "index.json"), "w"))
    return ix
