# -*- coding: utf-8 -*-
"""Routing and composition as the library grows from 45 to ~500 skills.

The 45 real skills keep their real atoms and expansions. Distractors are synthetic skills from 20
unrelated professional domains, each with a description, eight expansions and four atoms, so they
compete for both routing and lesson selection rather than sitting inert.
"""
import glob, json, random, statistics as st, sys, time
sys.path.insert(0,'src'); sys.path.insert(0,'v2/eval')
from skillmerge.router import SkillRouter
from skillmerge.compose3 import Composer3
from skillmerge.index3 import load_atoms
from skillmerge.text import tokenize, tfidf_vectors, leader_cluster
from skillmerge.tokens import count_many
from tasks2 import TASKS2
from collections import Counter
import math

REAL = json.load(open('v3/index3.json'))
real_atoms = load_atoms('v3/atoms')
real_names = {s['name'] for s in REAL['skills']}
real_meta = {s['name']: s for s in REAL['skills']}

dis = []
for p in sorted(glob.glob('scale/skills/*.json')):
    try: rows = json.load(open(p))
    except Exception: continue
    for r in rows:
        if not isinstance(r, dict) or 'name' not in r: continue
        nm = r['name']
        if nm in real_names or any(d['name'] == nm for d in dis): continue
        dis.append(r)
print(f"{len(real_names)} real skills, {len(dis)} distractors, {len(real_names)+len(dis)} total")

def build(n, seed=3):
    """Library of the 45 real skills plus (n-45) distractors."""
    rng = random.Random(seed)
    extra = rng.sample(dis, min(max(0, n - len(real_names)), len(dis)))
    skills = [dict(real_meta[s['name']]) for s in REAL['skills']]
    atoms = list(real_atoms)
    for d in extra:
        skills.append(dict(name=d['name'], description=d.get('description',''), dir='',
                           expansions=d.get('expansions') or []))
        for i, a in enumerate(d.get('atoms') or []):
            atoms.append(dict(skill=d['name'], obligation=(a.get('obligation') or '').strip(),
                              lesson=(a.get('lesson') or '').strip(), kind='prose', refs=[],
                              anchor='', ord=i))
    atoms = [a for a in atoms if a['obligation'] and len(a['lesson']) >= 20]
    docs = [tokenize(a['obligation']) for a in atoms]
    V = tfidf_vectors(docs)
    order = sorted(range(len(atoms)), key=lambda i: (atoms[i]['skill'], atoms[i]['ord']))
    cl = leader_cluster(V, 0.25, order)
    units = []
    for ci, m in enumerate(sorted(cl, key=lambda c: -len(c))):
        obs = [atoms[i]['obligation'] for i in m]
        rep = min(range(len(m)), key=lambda k: len(obs[k]))
        tok = Counter()
        for i in m: tok.update(docs[i])
        lessons = [dict(skill=atoms[i]['skill'], text=atoms[i]['lesson'], kind=atoms[i]['kind'],
                        refs=[], anchor='', obligation=atoms[i]['obligation']) for i in m]
        sk = sorted({l['skill'] for l in lessons})
        units.append(dict(uid=f"U{ci:05d}", obligation=obs[rep], lessons=lessons, skills=sk,
                          support=len(sk), tags=[t for t,_ in tok.most_common(10)],
                          kinds=['prose'], refs=[]))
    ix = dict(units=units, skills=skills, atoms=len(atoms), refs=dict(kept=0, dropped=0),
              params=dict(sim_threshold=0.25, cross_skill=True), abstain=REAL.get('abstain', {}))
    return ix

import os
SIZES = [int(x) for x in sys.argv[1:]] or [45]
outp = 'results/scale_routing.json'
prev = json.load(open(outp)) if os.path.exists(outp) else dict(rows=[], real=len(real_names), distractors=len(dis))
rows = [r for r in prev['rows'] if r['n'] not in SIZES]
print(f"\n{'n':>5} {'atoms':>6} {'units':>6} {'merged':>7} {'route P':>8} {'route R':>8} "
      f"{'route F1':>9} {'skills/req':>11} {'lesson purity':>14} {'abstain':>8} {'ms/req':>7}")
for n in SIZES:
    ix = build(n)
    R = SkillRouter(ix['skills'], abstain=ix.get('abstain'))
    C = Composer3(ix, R)
    C.compose(TASKS2[0]['prompt'], budget_tokens=1500)   # warm caches
    P = Rc = 0.0; nsk = []; pur = []; opur = []; ab = 0; lat = []
    for t in TASKS2:
        gold = set(t['oracle_skills'])
        routed, conf, k, a = R.route_adaptive(t['prompt'])
        got = {x for x, _ in routed}
        P += len(got & gold) / len(got) if got else 0
        Rc += len(got & gold) / len(gold)
        nsk.append(len(got))
        if R.should_abstain(t['prompt']): ab += 1
        t0 = time.time()
        plan = C.compose(t['prompt'], budget_tokens=1500)
        lat.append(1000 * (time.time() - t0))
        ls = [C.units[ui]['lessons'][li]['skill'] for ui, li in plan['lessons']]
        if ls:
            pur.append(sum(1 for s in ls if s in real_names) / len(ls))
            opur.append(sum(1 for s in ls if s in gold) / len(ls))
    m = len(TASKS2); P /= m; Rc /= m
    f1 = 2*P*Rc/(P+Rc) if P+Rc else 0
    merged = sum(1 for u in ix['units'] if u['support'] > 1)
    row = dict(n=n, atoms=ix['atoms'], units=len(ix['units']), merged=merged,
               P=P, R=Rc, F1=f1, skills_per_req=st.mean(nsk),
               lesson_purity=st.mean(pur), oracle_purity=st.mean(opur),
               false_abstain=ab/m, ms=st.mean(lat))
    rows.append(row)
    print(f"{n:5d} {ix['atoms']:6d} {len(ix['units']):6d} {merged:7d} {P:8.3f} {Rc:8.3f} {f1:9.3f} "
          f"{st.mean(nsk):11.1f} {st.mean(pur):14.3f} {ab/m:8.2f} {st.mean(lat):7.0f}")
rows.sort(key=lambda r: r['n'])
json.dump(dict(rows=rows, real=len(real_names), distractors=len(dis)), open(outp,'w'), indent=1)
