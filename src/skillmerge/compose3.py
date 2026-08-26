# -*- coding: utf-8 -*-
"""v3 composition: obligations are cheap and always affordable; lessons are the budget.

The composer now has a lever v2 did not: it can include an obligation with none, one, or every one
of its lessons. Under a tight budget the reader gets the checklist plus the single most relevant
piece of teaching; under a generous one, the teaching from every skill that imposed the same
requirement.
"""
import os, re
from .text import tokenize, BM25
from .tokens import count, count_many

PHASES = [
    ("Scope and inputs", ["scoping","requirements","clarification","intake","assumptions","context",
        "audience","constraints","discovery","triage","severity","prioritisation","dependencies",
        "stakeholders","compliance","licensing","privacy","cost","budget","baseline","confirm","ask"]),
    ("Doing the work", ["execution","implementation","procedure","steps","workflow","build","create",
        "edit","convert","migration","rollout","deployment","reproduce","isolate","diagnose","fix",
        "design","structure","format","style","tooling","script","command","run","apply","write"]),
    ("Checking the work", ["verification","validation","testing","review","quality","evidence",
        "accuracy","regression","monitoring","observability","metrics","uncertainty","risk",
        "rollback","reversibility","edge","security","check","verify","confirm"]),
    ("Closing and communicating", ["communication","reporting","summary","handover","documentation",
        "completion","announcement","escalation","postmortem","delivery","publish","approval",
        "notify","record"]),
]

def _phase_of(tags, text):
    hay = set(tags) | set(tokenize(text))
    low = text.lower()
    best, bestn = 1, -1
    for i, (_, kws) in enumerate(PHASES):
        n = sum(1 for k in kws if k in hay or k in low)
        if n > bestn: best, bestn = i, n
    return best

def _slug(s, n=44):
    return (re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")[:n].rstrip("-")) or "task"

class Composer3:
    def __init__(self, index, router):
        """router: a SkillRouter over the same skill metadata the index was built from."""
        self.ix = index
        self.units = index["units"]
        self.router = router
        self.by_name = {s["name"]: s for s in index["skills"]}
        self.u_docs = [tokenize(" ".join([u["obligation"]] * 3 + [l["text"] for l in u["lessons"]]
                                         + u["tags"])) for u in self.units]
        self.u_bm25 = BM25(self.u_docs)
        self.ob_tokens = count_many([u["obligation"] for u in self.units])
        flat = [(ui, li) for ui, u in enumerate(self.units) for li in range(len(u["lessons"]))]
        self.les_tokens = {}
        vals = count_many([self.units[ui]["lessons"][li]["text"] for ui, li in flat])
        for (ui, li), v in zip(flat, vals): self.les_tokens[(ui, li)] = v
        self.l_docs = {(ui, li): tokenize(self.units[ui]["lessons"][li]["text"]) for ui, li in flat}
        self.l_bm25 = BM25([self.l_docs[k] for k in flat]); self.l_keys = flat
        self.l_index = {k: i for i, k in enumerate(flat)}

    def compose(self, query, budget_tokens=1500, max_units=24, extra_lesson_floor=0.22,
                confidence_floor=0.0):
        """Select (obligation + its best lesson) as one package, then buy extra lessons.

        An obligation without its lesson is the checklist half of the split: true, and useless.
        So a unit is only ever included together with at least one lesson, and units compete on the
        cost of that package. Additional lessons -- the other skills' takes on the same obligation --
        are bought afterwards with whatever budget remains, which is the merge finally paying off.
        """
        conf = self.router.confidence(query)
        if confidence_floor and conf < confidence_floor:
            return dict(query=query, routed=[], units=[], lessons=[], abstained=True,
                        confidence=conf, budget=budget_tokens)
        routed, _, _, _ = self.router.route_adaptive(query)
        names = {n for n, _ in routed}
        rmax = max((s for _, s in routed), default=1.0) or 1.0
        aff = {n: s / rmax for n, s in routed}
        q = tokenize(query)
        us = self.u_bm25.scores(q); umax = max(us) or 1.0
        ls = self.l_bm25.scores(q); lmax = max(ls) or 1.0

        def lesson_score(ui, li):
            les = self.units[ui]["lessons"][li]
            r = ls[self.l_index[(ui, li)]] / lmax
            if les["skill"] in names: r += 0.30
            if les["kind"] == "pinned" and les["skill"] not in names: r -= 0.45
            return r

        scored = []
        for i, u in enumerate(self.units):
            a = max((aff.get(s, 0.0) for s in u["skills"]), default=0.0)
            s = us[i] / umax + 0.25 * a
            if not (set(u["skills"]) & names): s *= 0.6
            best = max(range(len(u["lessons"])), key=lambda li: lesson_score(i, li))
            scored.append((s + 0.35 * lesson_score(i, best), i, best))
        scored.sort(key=lambda x: (-x[0], self.units[x[1]]["uid"]))
        top = scored[0][0] if scored else 0.0
        scored = [x for x in scored if x[0] >= max(0.12, 0.32 * top)]

        src = sum(self.router.skill_tokens.get(n, 0) for n in names)
        if src: budget_tokens = min(budget_tokens, int(0.9 * src))

        used, units, lessons = 60, [], []
        for _, ui, li in scored[:max_units * 3]:
            if len(units) >= max_units: break
            cost = self.ob_tokens[ui] + self.les_tokens[(ui, li)] + 10
            if used + cost > budget_tokens: continue
            units.append(ui); lessons.append((ui, li)); used += cost
        chosen = set(lessons)
        extra = []
        for ui in units:
            for li in range(len(self.units[ui]["lessons"])):
                if (ui, li) in chosen: continue
                extra.append((lesson_score(ui, li), ui, li))
        extra.sort(key=lambda x: (-x[0], x[1], x[2]))
        for r, ui, li in extra:
            if r < extra_lesson_floor: break
            t = self.les_tokens[(ui, li)] + 8
            if used + t > budget_tokens: continue
            lessons.append((ui, li)); used += t
        units.sort(key=lambda i: (_phase_of(self.units[i]["tags"], self.units[i]["obligation"]),
                                  -self.units[i]["support"], self.units[i]["uid"]))
        plan = dict(query=query, routed=routed, units=units, lessons=lessons, abstained=False,
                    confidence=conf, budget=budget_tokens)
        while count(self.render_skill(plan)) > budget_tokens and len(plan["units"]) > 1:
            drop = plan["units"].pop()
            plan["lessons"] = [(u, l) for u, l in plan["lessons"] if u != drop]
        return plan

    def render_skill(self, plan, name=None, description=None):
        if plan.get("abstained"): return ""
        srcs = [n for n, _ in plan["routed"]]
        q = plan["query"].strip().replace("\n", " ")
        name = name or ("composed-" + _slug(q))
        desc = description or (f"Task-scoped composite assembled for: {q[:170]}"
                               f"{'...' if len(q) > 170 else ''} Sources: {', '.join(srcs)}.")
        by_unit = {}
        for ui, li in plan["lessons"]: by_unit.setdefault(ui, []).append(li)
        out = ["---", f"name: {name}", f"description: {desc.replace(chr(10),' ')}",
               "source-skills: [" + ", ".join(srcs) + "]", "composed-by: skillmerge/3", "---", "",
               f"# {name.replace('-', ' ').capitalize()}", "",
               "Each numbered item is an obligation. Indented notes under it are the specific "
               "knowledge that makes it actionable, labelled with the skill it comes from.", ""]
        cur, n, refs = None, 0, []
        for ui in plan["units"]:
            u = self.units[ui]
            ph = _phase_of(u["tags"], u["obligation"])
            if ph != cur:
                cur = ph; out += [f"## {PHASES[ph][0]}", ""]
            n += 1
            out += [f"{n}. **{u['obligation']}**", ""]
            for li in by_unit.get(ui, []):
                les = u["lessons"][li]
                body = les["text"].strip()
                out.append(f"   *from `{les['skill']}`* — " +
                           (body if "\n" not in body else "")); 
                if "\n" in body:
                    out.append("")
                    out += ["   " + ln for ln in body.splitlines()]
                out.append("")
                refs += [(r, les["skill"]) for r in les["refs"]]
        if refs:
            seen, uniq = set(), []
            for r, sk in refs:
                if (r, sk) in seen: continue
                seen.add((r, sk)); uniq.append((r, sk))
            out += ["## Resources referenced above", "",
                    "These files ship with the source skills and remain authoritative.", ""]
            for r, sk in uniq:
                d = self.by_name.get(sk, {}).get("dir", "")
                out.append(f"- `{r}` — from skill `{sk}`" + (f", at `{os.path.join(d, r)}`" if d and not r.startswith('..') else ""))
            out.append("")
        return "\n".join(out).rstrip() + "\n"

    def explain(self, plan):
        by_unit = {}
        for ui, li in plan["lessons"]: by_unit.setdefault(ui, []).append(li)
        return [dict(uid=self.units[ui]["uid"], obligation=self.units[ui]["obligation"],
                     support=self.units[ui]["support"], skills=self.units[ui]["skills"],
                     lessons_included=len(by_unit.get(ui, [])),
                     lessons_available=len(self.units[ui]["lessons"]))
                for ui in plan["units"]]
