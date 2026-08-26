# -*- coding: utf-8 -*-
"""Command line for the offline pipeline and a one-shot composer.

    skillmerge discover /path/to/skills [more...]
    skillmerge jobs
    skillmerge build
    skillmerge compose "the task, in the words a person would use"
    skillmerge serve
"""
import argparse, json, os, sys
from . import pipeline


def _load(build_dir):
    from .router import SkillRouter
    from .compose3 import Composer3
    ix = json.load(open(os.path.join(build_dir, "index.json")))
    return Composer3(ix, SkillRouter(ix["skills"], abstain=ix.get("abstain")))


def main(argv=None):
    ap = argparse.ArgumentParser(prog="skillmerge", description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--build-dir", default=os.environ.get("SKILLMERGE_BUILD", "build"))
    sub = ap.add_subparsers(dest="cmd", required=True)
    d = sub.add_parser("discover", help="read every SKILL.md under the given roots")
    d.add_argument("roots", nargs="+")
    sub.add_parser("jobs", help="write the refactoring and expansion prompts")
    b = sub.add_parser("build", help="build the index from build/atoms and build/expansions_*.json")
    b.add_argument("--tau", type=float, default=0.25)
    b.add_argument("--no-cross-skill", action="store_true")
    c = sub.add_parser("compose", help="print a composite skill for one task")
    c.add_argument("task")
    c.add_argument("--budget", type=int, default=1500)
    sub.add_parser("serve", help="run the MCP server on stdio")
    a = ap.parse_args(argv)

    if a.cmd == "discover":
        s = pipeline.discover(a.roots, a.build_dir)
        print(f"{len(s)} skills -> {a.build_dir}/skills.json")
    elif a.cmd == "jobs":
        n, m = pipeline.jobs(a.build_dir)
        print(f"{n} refactoring jobs and {m} expansion jobs -> {a.build_dir}/jobs/")
        print("Run each with any agent that can read a file and write JSON, then: skillmerge build")
    elif a.cmd == "build":
        ix = pipeline.build(a.build_dir, a.tau, not a.no_cross_skill)
        merged = sum(1 for u in ix["units"] if u["support"] > 1)
        print(f"{ix['atoms']} atoms -> {len(ix['units'])} units, {merged} merged across skills")
        print(f"reference paths: {ix['refs']['kept']} kept, {ix['refs']['dropped']} dropped as invalid")
    elif a.cmd == "compose":
        C = _load(a.build_dir)
        floor = C.ix.get("abstain", {}).get("floor", 0.0)
        plan = C.compose(a.task, budget_tokens=a.budget, confidence_floor=floor)
        if plan.get("abstained"):
            print("No skill in the library matches this task with enough confidence.", file=sys.stderr)
            return 1
        sys.stdout.write(C.render_skill(plan))
    elif a.cmd == "serve":
        from .server import main as serve
        serve()
    return 0


if __name__ == "__main__":
    sys.exit(main())
