# -*- coding: utf-8 -*-
"""Skill-level routing, confidence and abstention.

The Agent Skills format already carries an authored routing signal: the description. Expansions
help, but at corpus scale their generic situational vocabulary collides across domains, so the two
are scored separately and the expansions down-weighted rather than concatenated.

`b` in the description index is set near zero on purpose. BM25's length normalisation assumes long
documents are verbose; here description length tracks scope, so penalising it demotes exactly the
skills that cover the most ground.
"""
import os
from .text import tokenize, BM25
from .tokens import count_many


class SkillRouter:
    def __init__(self, skills, route_b=0.0, abstain=None):
        """skills: list of {name, description, dir, expansions}."""
        self.skills = skills
        self.name_idx = {s["name"]: i for i, s in enumerate(skills)}
        self.desc = [tokenize(" ".join([s["name"].replace("-", " ")] * 2
                                       + [s.get("description") or ""])) for s in skills]
        self.exp = [tokenize(" ".join(s.get("expansions") or [])) for s in skills]
        self.bm25 = BM25(self.desc, b=route_b)
        self.bm25_exp = BM25(self.exp, b=route_b)
        self.cal = abstain or {}
        paths, names = [], []
        for s in skills:
            p = os.path.join(s.get("dir") or "", "SKILL.md")
            if p and os.path.exists(p):
                paths.append(open(p, encoding="utf-8", errors="replace").read())
                names.append(s["name"])
        self.skill_tokens = dict(zip(names, count_many(paths))) if paths else {}

    # ---------------------------------------------------------------- scoring
    def scores(self, query, beta=1.0):
        q = tokenize(query)
        a = self.bm25.scores(q)
        b = self.bm25_exp.scores(q)
        return [x + beta * y for x, y in zip(a, b)]

    def confidence(self, query, beta=1.0):
        """Best skill score. Calibrated on in-corpus probes against out-of-corpus ones; the raw top
        score separated those better than a z-score or a length-normalised ratio."""
        sc = self.scores(query, beta)
        return max(sc) if sc else 0.0

    def route(self, query, k_max=3, alpha=0.55, beta=1.0):
        sc = self.scores(query, beta)
        order = sorted(range(len(sc)), key=lambda i: -sc[i])
        mx = sc[order[0]] if sc and sc[order[0]] > 0 else 1.0
        sel = [i for i in order[:k_max] if sc[i] >= alpha * mx] or order[:1]
        return [(self.skills[i]["name"], sc[i]) for i in sel]

    def route_adaptive(self, query, beta=1.0, narrow=(3, 0.55), wide=(7, 0.30)):
        """Hedge when the corpus does not clearly single out a skill.

        A confident query routes narrowly, because extra skills only dilute the budget. An uncertain
        one routes wide: fragment selection can still find the right material inside a larger
        candidate set, but only if that material is in the set at all.
        """
        hi = self.cal.get("conf_hi", 20.58)
        lo = self.cal.get("conf_lo", 15.11)
        c = self.confidence(query, beta)
        if c >= hi:
            k, a = narrow
        elif c <= lo:
            k, a = wide
        else:
            f = (c - lo) / max(1e-9, hi - lo)
            k = int(round(wide[0] + f * (narrow[0] - wide[0])))
            a = wide[1] + f * (narrow[1] - wide[1])
        return self.route(query, k_max=k, alpha=a, beta=beta), c, k, a

    def should_abstain(self, query, beta=1.0):
        floor = self.cal.get("floor", 0.0)
        return bool(floor) and self.confidence(query, beta) < floor
