# -*- coding: utf-8 -*-
"""Full statistical treatment across the three studies.

Adds to the bootstrap already computed: exact Wilcoxon signed-rank tests, Holm correction within
each study's family of contrasts, paired effect sizes, quadratic-weighted kappa and Krippendorff's
alpha for the grader panels, and a two-proportion test on the merge-adjudication change.
"""
import json, math, random, itertools, statistics as st
from collections import Counter

# ------------------------------------------------------------------ exact Wilcoxon signed-rank
def wilcoxon(d):
    """Exact two-sided signed-rank test. n<=20, ties handled by average ranks (exact null then
    approximate; we report it as such)."""
    nz = [x for x in d if x != 0]
    n = len(nz)
    if n == 0:
        return dict(n=0, W=0.0, p=1.0, rb=0.0)
    a = sorted(range(n), key=lambda i: abs(nz[i]))
    ranks = [0.0] * n
    i = 0
    while i < n:
        j = i
        while j + 1 < n and abs(nz[a[j + 1]]) == abs(nz[a[i]]):
            j += 1
        r = (i + j) / 2 + 1
        for k in range(i, j + 1):
            ranks[a[k]] = r
        i = j + 1
    Wp = sum(ranks[i] for i in range(n) if nz[i] > 0)
    Wm = sum(ranks[i] for i in range(n) if nz[i] < 0)
    W = min(Wp, Wm)
    total = n * (n + 1) / 2
    # exact null distribution over sign assignments
    counts = Counter({0.0: 1})
    for r in ranks:
        nxt = Counter()
        for s, c in counts.items():
            nxt[s] += c; nxt[s + r] += c
        counts = nxt
    tot = 2 ** n
    p = sum(c for s, c in counts.items() if s <= W or s >= total - W) / tot
    rb = (Wp - Wm) / total          # rank-biserial correlation
    return dict(n=n, W=W, p=min(1.0, p), rb=rb)

def holm(pvals):
    idx = sorted(range(len(pvals)), key=lambda i: pvals[i])
    out = [0.0] * len(pvals); prev = 0.0
    for k, i in enumerate(idx):
        adj = min(1.0, (len(pvals) - k) * pvals[i])
        prev = max(prev, adj); out[i] = prev
    return out

def boot(d, n=20000, seed=13):
    rng = random.Random(seed); bs = []
    for _ in range(n):
        bs.append(sum(d[rng.randrange(len(d))] for _ in d) / len(d))
    bs.sort()
    return bs[int(.025 * n)], bs[int(.975 * n)]

def dz(d):
    s = st.pstdev(d) if len(d) > 1 else 0.0
    sd = st.stdev(d) if len(d) > 1 else 0.0
    return st.mean(d) / sd if sd > 0 else float('nan')

# ------------------------------------------------------------------ reliability
def weighted_kappa(pairs, k=3):
    """Quadratic-weighted Cohen's kappa on ordinal 0..k-1 scores."""
    n = len(pairs)
    O = [[0] * k for _ in range(k)]
    for a, b in pairs: O[a][b] += 1
    ra = [sum(O[i]) / n for i in range(k)]
    rb = [sum(O[i][j] for i in range(k)) / n for j in range(k)]
    W = [[((i - j) ** 2) / ((k - 1) ** 2) for j in range(k)] for i in range(k)]
    num = sum(W[i][j] * O[i][j] / n for i in range(k) for j in range(k))
    den = sum(W[i][j] * ra[i] * rb[j] for i in range(k) for j in range(k))
    return 1 - num / den if den > 0 else float('nan')

def krippendorff_ordinal(pairs, k=3):
    """Krippendorff's alpha for two coders, ordinal metric, complete data."""
    n = len(pairs)
    vals = [v for p in pairs for v in p]
    freq = Counter(vals); N = len(vals)
    def dist(a, b):
        lo, hi = min(a, b), max(a, b)
        s = sum(freq[g] for g in range(lo, hi + 1)) - (freq[a] + freq[b]) / 2
        return s ** 2
    Do = sum(dist(a, b) for a, b in pairs) / n
    De = sum(freq[a] * freq[b] * dist(a, b) for a in range(k) for b in range(k) if a != b)
    De /= (N * (N - 1))
    return 1 - Do / De if De > 0 else float('nan')

# ------------------------------------------------------------------ two-proportion test
def two_prop(x1, n1, x2, n2):
    p1, p2 = x1 / n1, x2 / n2
    p = (x1 + x2) / (n1 + n2)
    se = math.sqrt(p * (1 - p) * (1 / n1 + 1 / n2))
    z = (p2 - p1) / se if se > 0 else 0.0
    pv = 2 * (1 - 0.5 * (1 + math.erf(abs(z) / math.sqrt(2))))
    sed = math.sqrt(p1 * (1 - p1) / n1 + p2 * (1 - p2) / n2)
    return dict(p1=p1, p2=p2, diff=p2 - p1, z=z, p=pv,
                ci=(p2 - p1 - 1.96 * sed, p2 - p1 + 1.96 * sed))

OUT = {}

def study(name, path, conds, contrasts, key="rubric"):
    E = json.load(open(path)); rows = E['per_run']
    by = {}
    for r in rows: by.setdefault(r['cond'], {})[r['task']] = r
    res = {}
    raw = []
    for a, b in contrasts:
        ts = sorted(set(by[a]) & set(by[b]))
        d = [by[b][t][key] - by[a][t][key] for t in ts]
        w = wilcoxon(d); lo, hi = boot(d)
        raw.append(dict(pair=f"{b}-{a}", delta=st.mean(d), lo=lo, hi=hi, dz=dz(d),
                        p=w['p'], rb=w['rb'], n=w['n'],
                        wins=sum(1 for x in d if x > 0), losses=sum(1 for x in d if x < 0)))
    adj = holm([r['p'] for r in raw])
    for r, a in zip(raw, adj): r['p_holm'] = a
    res['contrasts'] = raw
    res['means'] = {c: dict(rubric=st.mean(v[t]['rubric'] for t in v),
                            ctx=st.mean(v[t]['ctx'] for t in v),
                            overall=st.mean(v[t]['overall'] for t in v))
                    for c, v in by.items() if c in conds}
    if 'agreement' in E: res['agreement_raw'] = E['agreement']
    OUT[name] = res
    print(f"\n=== {name} ===")
    print(f"{'contrast':34s} {'delta':>7} {'95% CI':>18} {'d_z':>6} {'p':>8} {'p(Holm)':>8} {'rb':>6} W/L")
    for r in raw:
        print(f"{r['pair']:34s} {r['delta']:+7.3f} [{r['lo']:+6.3f},{r['hi']:+6.3f}] {r['dz']:+6.2f} "
              f"{r['p']:8.4f} {r['p_holm']:8.4f} {r['rb']:+6.2f} {r['wins']}/{r['losses']}")
    return res

study("study1_synthetic", "results/experiment.json",
      ["A_none","B_concat","C_composed","D_random"],
      [("A_none","C_composed"),("B_concat","C_composed"),("D_random","C_composed"),
       ("A_none","B_concat"),("A_none","D_random")])
study("study2_real", "results/v2_experiment.json",
      ["A_none","B_concat","C_composed","D_random","E_matched"],
      [("A_none","C_composed"),("B_concat","C_composed"),("D_random","C_composed"),
       ("C_composed","E_matched"),("B_concat","E_matched"),("A_none","B_concat")])
study("study4_scale", "results/scale504_experiment.json",
      ["B_concat","G_lessons","H_routed","J_scale"],
      [("G_lessons","J_scale"),("H_routed","J_scale"),("B_concat","J_scale"),
       ("H_routed","G_lessons"),("B_concat","G_lessons"),("B_concat","H_routed")])
study("study3_atoms", "results/v3_lessons_experiment.json",
      ["B_concat","C_composed","F_v3","G_lessons"],
      [("F_v3","G_lessons"),("C_composed","G_lessons"),("C_composed","F_v3"),
       ("B_concat","G_lessons"),("B_concat","C_composed")])

print("\n=== grader reliability ===")
import glob, os, sys
sys.path.insert(0,'v2/eval'); sys.path.insert(0,'eval')
def rel_v1():
    from tasks import TASKS
    key = json.load(open('grading/key.json')); got = {}
    for panel in (1,2):
        for t in TASKS:
            p = f"grading/P{panel}_{t['id']}.json"
            if not os.path.exists(p): continue
            g = json.load(open(p))
            for lab, cond in key[f"P{panel}_{t['id']}"].items():
                if lab in g:
                    sc = g[lab].get('scores', [])
                    sc = [min(2, max(0, int(x))) for x in (list(sc)+[0]*len(t['rubric']))[:len(t['rubric'])]]
                    got[(panel, t['id'], cond)] = sc
    return [(a, b) for (t, c) in {(k[1], k[2]) for k in got}
            for a, b in zip(got.get((1, t, c), []), got.get((2, t, c), []))]
def rel_v(keyfile, tag):
    from tasks2 import TASKS2
    key = json.load(open(keyfile)); got = {}
    for panel in (1, 2):
        for t in TASKS2:
            p = f"v2/grading/{tag}{panel}_{t['id']}.json"
            if not os.path.exists(p): continue
            g = json.load(open(p))
            na = len(json.load(open(f"v2/rubrics/{t['id']}_rubric_task.json"))['criteria'])
            nb = len(json.load(open(f"v2/rubrics/{t['id']}_rubric_skill.json"))['criteria'])
            for lab, cond in key[f"{tag}{panel}_{t['id']}"].items():
                if lab not in g: continue
                fix = lambda v, n: [min(2, max(0, int(x))) for x in (list(v)+[0]*n)[:n]]
                got[(panel, t['id'], cond)] = fix(g[lab].get('a', []), na) + fix(g[lab].get('b', []), nb)
    return [(a, b) for (t, c) in {(k[1], k[2]) for k in got}
            for a, b in zip(got.get((1, t, c), []), got.get((2, t, c), []))]

# The per-item grading transcripts these recompute from embed real skill text and are not
# redistributed (see NOTICE); when they are absent, fall back to the reliability figures already
# stored in results/stats_all.json rather than crash.
try:
    for nm, pr in (("study1_synthetic", rel_v1()),
                   ("study2_real", rel_v('v2/grading/key2.json', 'Q')),
                   ("study3_atoms", rel_v('v2/grading/key4.json', 'S'))):
        ex = sum(1 for a, b in pr if a == b) / len(pr)
        kw = weighted_kappa(pr); ka = krippendorff_ordinal(pr)
        OUT[nm]['reliability'] = dict(items=len(pr), exact=ex, kappa_qw=kw, alpha=ka)
        print(f"{nm:20s} n={len(pr):5d} exact={ex:.3f}  weighted kappa={kw:.3f}  Krippendorff alpha={ka:.3f}")
except (ModuleNotFoundError, FileNotFoundError) as e:
    print(f"grading transcripts not in this release ({e}); reusing stored reliability from results/stats_all.json")
    stored = json.load(open('results/stats_all.json')) if os.path.exists('results/stats_all.json') else {}
    for nm in ("study1_synthetic", "study2_real", "study3_atoms"):
        if nm in stored and 'reliability' in stored[nm]:
            OUT[nm]['reliability'] = stored[nm]['reliability']
            r = stored[nm]['reliability']
            print(f"{nm:20s} n={r['items']:5d} exact={r['exact']:.3f}  weighted kappa={r['kappa_qw']:.3f}  Krippendorff alpha={r['alpha']:.3f}  (stored)")

M2 = json.load(open('results/v2_merge_validation.json'))
M3 = json.load(open('results/v3_merge_validation.json'))
tp = two_prop(M2['tp'], M2['merged'], M3['tp'], M3['merged'])
OUT['merge_precision_test'] = tp
print(f"\n=== merge precision, v2 vs v3 ===")
print(f"v2 {M2['tp']}/{M2['merged']} = {tp['p1']:.3f}   v3 {M3['tp']}/{M3['merged']} = {tp['p2']:.3f}")
print(f"difference {tp['diff']:+.3f}  95% CI [{tp['ci'][0]:+.3f},{tp['ci'][1]:+.3f}]  z={tp['z']:.2f}  p={tp['p']:.2e}")
json.dump(OUT, open('results/stats_all.json', 'w'), indent=1)
print("\nwrote results/stats_all.json")
