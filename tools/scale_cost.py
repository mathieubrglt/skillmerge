# -*- coding: utf-8 -*-
"""Total per-request context cost against library size.

Agent Skills keep every skill's name and description resident so the model can decide what to load.
That is linear in library size and paid on every request. SkillMerge replaces it with one tool
description and one call whose output is capped by construction.
"""
import json, statistics as st
SC=json.load(open('results/scale_analysis.json'))
EX=json.load(open('results/scale_experiment.json'))['summary']
man=[r for r in json.load(open('v2/runs/manifest.json'))['runs']]
H=[r for r in man if r['cond']=='H_routed']
per=SC['description_tokens']['median']; tool=SC['compose_tool_tokens']
whole=EX['H_routed']['ctx']; comp=EX['G_lessons']['ctx']
print(f"router-selected whole skills: {st.mean(r['n_frag'] for r in H):.1f} skills, "
      f"{whole:,.0f} tokens loaded (max {max(r['ctx_tokens'] for r in H):,})")
print(f"SkillMerge composite: {comp:,.0f} tokens, hard cap 1,500\n")
print(f"{'library':>8} {'whole skills total':>19} {'SkillMerge total':>17} {'ratio':>7} "
      f"{'pts/1k tok':>21}")
rows=[]
for n in (10,45,100,250,500,1000):
    w=per*n+whole; s=tool+comp
    pw=EX['H_routed']['rubric']/(w/1000); ps=EX['G_lessons']['rubric']/(s/1000)
    rows.append(dict(n=n, whole_total=w, sm_total=s, ratio=w/s,
                     whole_pts_per_1k=pw, sm_pts_per_1k=ps, advantage=ps/pw))
    print(f"{n:8d} {w:19,.0f} {s:17,.0f} {w/s:7.1f}x   {pw:8.3f} vs {ps:6.3f}  ({ps/pw:4.1f}x)")
json.dump(dict(rows=rows, per_skill_description=per, compose_tool=tool,
               whole_loaded=whole, composite=comp,
               rubric_whole=EX['H_routed']['rubric'], rubric_sm=EX['G_lessons']['rubric']),
          open('results/scale_cost.json','w'), indent=1)
print("\nquality: whole skills router-selected %.3f, composite %.3f (delta %.3f)"
      % (EX['H_routed']['rubric'], EX['G_lessons']['rubric'],
         EX['G_lessons']['rubric']-EX['H_routed']['rubric']))
