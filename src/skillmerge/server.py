# -*- coding: utf-8 -*-
"""SkillMerge MCP server: a skill library in, one task-scoped Agent Skill out.

Environment:
  SKILLMERGE_BUILD   build directory holding index.json (default: build)
  SKILLMERGE_BUDGET  default token ceiling for a composite (default: 1500)
"""
import json, os
from .router import SkillRouter
from .compose3 import Composer3
from .tokens import count

BUILD = os.environ.get("SKILLMERGE_BUILD", "build")
BUDGET = int(os.environ.get("SKILLMERGE_BUDGET", "1500"))
_s = {}


def composer():
    if "c" not in _s:
        ix = json.load(open(os.path.join(BUILD, "index.json")))
        _s["ix"] = ix
        _s["c"] = Composer3(ix, SkillRouter(ix["skills"], abstain=ix.get("abstain")))
    return _s["c"]


def compose_skill(task, budget_tokens=None):
    c = composer()
    floor = _s["ix"].get("abstain", {}).get("floor", 0.0)
    plan = c.compose(task, budget_tokens=int(budget_tokens or BUDGET), confidence_floor=floor)
    doc = c.render_skill(plan)
    srcs = [n for n, _ in plan["routed"]]
    full = sum(c.router.skill_tokens.get(n, 0) for n in srcs)
    used = count(doc) if doc else 0
    return dict(skill_md=doc, abstained=bool(plan.get("abstained")),
                accounting=dict(composed_tokens=used, source_skill_tokens=full,
                                reduction_pct=round(100 * (1 - used / full), 1) if full and used else None,
                                obligations=len(plan["units"]), lessons=len(plan["lessons"]),
                                merged_obligations=sum(1 for ui in plan["units"]
                                                       if c.units[ui]["support"] > 1),
                                source_skills=srcs,
                                routing_confidence=round(plan.get("confidence", 0), 2),
                                budget_tokens=int(budget_tokens or BUDGET)))


def main():
    from mcp.server.fastmcp import FastMCP
    mcp = FastMCP("skillmerge")

    @mcp.tool()
    def compose_skill_tool(task: str, budget_tokens: int = 0) -> str:
        """Compose a task-scoped Agent Skill from the indexed library.

        Returns a complete SKILL.md. Each item is an obligation drawn from the library, and under
        it sits the specific knowledge that makes it actionable, labelled with the skill it came
        from. Where several skills impose the same obligation it is stated once and every skill's
        lesson is kept. Load the result as you would any skill.
        """
        r = compose_skill(task, budget_tokens or None)
        if r["abstained"]:
            return ("No skill in the library matches this task with enough confidence to compose "
                    "from. Proceed without skill guidance, or call list_skills_tool and pick one.")
        return r["skill_md"] + "\n<!-- skillmerge " + json.dumps(r["accounting"]) + " -->\n"

    @mcp.tool()
    def explain_composition_tool(task: str, budget_tokens: int = 0) -> str:
        """Selection trace: routing scores, confidence, and each obligation with its lesson count."""
        c = composer()
        plan = c.compose(task, budget_tokens=budget_tokens or BUDGET)
        return json.dumps(dict(confidence=round(plan.get("confidence", 0), 2),
                               abstained=bool(plan.get("abstained")),
                               routed=[dict(skill=n, score=round(s, 2)) for n, s in plan["routed"]],
                               selected=c.explain(plan)), indent=1)

    @mcp.tool()
    def search_obligations_tool(query: str, k: int = 8) -> str:
        """Search obligations. Each result lists every skill that imposes it and their lessons.

        This is the library-hygiene view: it shows where skills genuinely overlap.
        """
        c = composer()
        from .text import tokenize
        sc = c.u_bm25.scores(tokenize(query))
        order = sorted(range(len(sc)), key=lambda i: -sc[i])[:k]
        return json.dumps([dict(uid=c.units[i]["uid"], score=round(sc[i], 2),
                                obligation=c.units[i]["obligation"],
                                skills=c.units[i]["skills"],
                                lessons=[l["text"][:300] for l in c.units[i]["lessons"]])
                           for i in order], indent=1)

    @mcp.tool()
    def list_skills_tool() -> str:
        """List the source skills currently indexed."""
        c = composer()
        return json.dumps([dict(name=s["name"], description=(s.get("description") or "")[:300])
                           for s in c.ix["skills"]], indent=1)

    mcp.run()


if __name__ == "__main__":
    main()
