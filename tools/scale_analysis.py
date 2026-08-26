# -*- coding: utf-8 -*-
"""Scaling properties that do not need agents: resident-description cost and merge yield."""
import json, sys, statistics as st, random, itertools
sys.path.insert(0,'src')
from skillmerge.agentskills import discover
from skillmerge.index3 import load_atoms
from skillmerge.text import tokenize, tfidf_vectors, leader_cluster
from skillmerge.tokens import count_many

ROOTS=json.load(open('v2/roots.json'))
S=discover(ROOTS)
out={}

# ---- 1. resident description cost -------------------------------------------------
# Agent Skills keep every skill's name and description resident so the model can decide what to
# load. That cost is linear in library size and is paid on every request, whether or not a skill
# is used. A compose call replaces it with one tool description.
desc=[f"{s['name']}: {s['description']}" for s in S]
dt=count_many(desc)
per=st.median(dt)
out['description_tokens']=dict(n=len(dt), total=sum(dt), median=per, mean=st.mean(dt),
                               p90=sorted(dt)[int(.9*len(dt))])
TOOLDESC=count_many(["""compose_skill_tool(task, budget_tokens) -> str
Compose a task-scoped Agent Skill from the indexed library. Returns a complete SKILL.md. Each item
is an obligation drawn from the library, and under it sits the specific knowledge that makes it
actionable, labelled with the skill it came from. Where several skills impose the same obligation it
is stated once and every skill's lesson is kept. Load the result as you would any skill."""])[0]
out['compose_tool_tokens']=TOOLDESC
print(f"skill descriptions: n={len(dt)} median={per:.0f} mean={st.mean(dt):.0f} p90={sorted(dt)[int(.9*len(dt))]:.0f} tokens")
print(f"one compose tool description = {TOOLDESC} tokens\n")
print(f"{'library':>8} {'resident descriptions':>22} {'compose tool':>13} {'ratio':>7}")
rows=[]
for n in (10,45,100,250,500,1000):
    res=int(round(per*n))
    rows.append(dict(n=n, resident=res, compose=TOOLDESC, ratio=res/TOOLDESC))
    print(f"{n:8d} {res:22,d} {TOOLDESC:13d} {res/TOOLDESC:7.0f}x")
out['resident_curve']=rows

# ---- 2. merge yield against library size ------------------------------------------
A=load_atoms('v3/atoms')
by={}
for a in A: by.setdefault(a['skill'],[]).append(a)
names=sorted(by)
print(f"\n{'skills':>7} {'atoms':>7} {'units':>7} {'merged units':>13} {'lessons unioned':>16} {'merged/skill':>13}")
curve=[]
rng=random.Random(7)
for n in (5,10,15,20,25,30,35,40,45):
    trials=[]
    for t in range(8 if n<45 else 1):
        sub=rng.sample(names,n) if n<45 else names
        atoms=[a for s in sub for a in by[s]]
        V=tfidf_vectors([tokenize(a['obligation']) for a in atoms])
        order=sorted(range(len(atoms)),key=lambda i:(atoms[i]['skill'],atoms[i]['ord']))
        cl=leader_cluster(V,0.25,order)
        m=[c for c in cl if len({atoms[i]['skill'] for i in c})>1]
        trials.append((len(atoms),len(cl),len(m),sum(len(c) for c in m)))
    a_,u_,m_,l_=[st.mean(x[i] for x in trials) for i in range(4)]
    curve.append(dict(n=n,atoms=a_,units=u_,merged=m_,lessons=l_,merged_per_skill=m_/n))
    print(f"{n:7d} {a_:7.0f} {u_:7.0f} {m_:13.1f} {l_:16.1f} {m_/n:13.2f}")
out['merge_curve']=curve
sl=(curve[-1]['merged_per_skill']-curve[0]['merged_per_skill'])
print(f"\nmerged units per skill: {curve[0]['merged_per_skill']:.2f} at n=5 -> "
      f"{curve[-1]['merged_per_skill']:.2f} at n=45 (change {sl:+.2f})")
json.dump(out,open('results/scale_analysis.json','w'),indent=1)
