# -*- coding: utf-8 -*-
"""v3 index: atoms of one obligation plus one lesson.

v2 clustered whole fragments and kept a single representative, which meant a merge deleted the
losing fragment's content. An independent panel rejected 56 of 60 such merges. v3 separates the
comparable part of a fragment (the obligation) from the part that carries the teaching (the
lesson), compares only the former, and unions the latter. Merging now restates rather than deletes.
"""
import glob, json, math, os
from collections import Counter
from .text import tokenize, tfidf_vectors, agglomerative, leader_cluster, cosine

def load_atoms(atoms_dir):
    out = []
    for p in sorted(glob.glob(os.path.join(atoms_dir, "*.json"))):
        try:
            d = json.load(open(p))
        except Exception:
            continue
        sk = d.get("skill") or os.path.splitext(os.path.basename(p))[0]
        for i, a in enumerate(d.get("atoms", [])):
            ob = (a.get("obligation") or "").strip()
            le = (a.get("lesson") or "").strip()
            if not ob or len(le) < 20:
                continue
            out.append(dict(skill=sk, obligation=ob, lesson=le,
                            kind=("pinned" if a.get("kind") == "pinned" else "prose"),
                            refs=[r for r in (a.get("refs") or []) if isinstance(r, str)],
                            anchor=(a.get("anchor") or "").strip(), ord=i))
    return out

def validate_refs(atoms, skills_meta):
    """Drop reference paths that do not exist on disk.

    The fidelity audit caught the reformatter emitting a bare `recalc.py` where the skill actually
    ships `scripts/recalc.py`. An invented path is the most dangerous kind of distortion -- it reads
    as authoritative and fails only when someone runs it -- and it is the one class of error we can
    eliminate without a model, so we do.
    """
    dirs = {s["name"]: s.get("dir", "") for s in skills_meta}
    kept = dropped = 0
    for a in atoms:
        d = dirs.get(a["skill"], "")
        good = []
        for r in a["refs"]:
            if r.startswith("..") or not d:
                continue
            if os.path.exists(os.path.join(d, r)):
                good.append(r); kept += 1
            else:
                base = os.path.basename(r)
                hits = [f for f in glob.glob(os.path.join(d, "**", base), recursive=True)]
                if len(hits) == 1:
                    good.append(os.path.relpath(hits[0], d)); kept += 1
                else:
                    dropped += 1
        a["refs"] = sorted(set(good))
    return kept, dropped

def build_index3(atoms_dir, skills_meta, sim_threshold=0.25, cross_skill=True, top_tags=10):
    """skills_meta: list of {name, description, dir, expansions} reused from the v2 index."""
    atoms = load_atoms(atoms_dir)
    ref_kept, ref_dropped = validate_refs(atoms, skills_meta)
    docs = [tokenize(a["obligation"]) for a in atoms]
    vecs = tfidf_vectors(docs)
    order = sorted(range(len(atoms)), key=lambda i: (atoms[i]["skill"], atoms[i]["ord"]))
    if cross_skill:
        clusters = leader_cluster(vecs, sim_threshold, order)
    else:
        clusters = []
        for sk in sorted({a["skill"] for a in atoms}):
            local = [i for i in order if atoms[i]["skill"] == sk]
            sub = leader_cluster([vecs[i] for i in local], sim_threshold, range(len(local)))
            clusters += [[local[x] for x in c] for c in sub]

    N = len(docs); df = Counter()
    for d in docs:
        for t in set(d): df[t] += 1

    units = []
    for ci, members in enumerate(sorted(clusters, key=lambda c: -len(c))):
        obs = [atoms[i]["obligation"] for i in members]
        avg = []
        for a in members:
            s = [cosine(vecs[a], vecs[b]) for b in members if b != a]
            avg.append(sum(s) / len(s) if s else 1.0)
        mx = max(avg) if avg else 1.0
        cand = [k for k, v in enumerate(avg) if v >= 0.9 * mx] or list(range(len(members)))
        rep = min(cand, key=lambda k: len(obs[k]))
        tok = Counter()
        for i in members: tok.update(docs[i])
        def sc(kv):
            t, f = kv
            if len(t) < 4: return -1e9
            return (1 + math.log(f)) * math.log((1 + N) / (1 + df.get(t, 1)))
        tags = [t for t, _ in sorted(tok.items(), key=lambda kv: -sc(kv))][:top_tags]
        # every contributing lesson is kept, labelled with its source. nothing is deleted.
        lessons = [dict(skill=atoms[i]["skill"], text=atoms[i]["lesson"], kind=atoms[i]["kind"],
                        refs=atoms[i]["refs"], anchor=atoms[i]["anchor"],
                        obligation=atoms[i]["obligation"]) for i in members]
        skills = sorted({l["skill"] for l in lessons})
        units.append(dict(uid=f"U{ci:04d}", obligation=obs[rep], lessons=lessons,
                          skills=skills, support=len(skills), tags=tags,
                          kinds=sorted({l["kind"] for l in lessons}),
                          refs=sorted({r for l in lessons for r in l["refs"]})))
    return dict(units=units, skills=skills_meta, atoms=len(atoms),
                refs=dict(kept=ref_kept, dropped=ref_dropped),
                params=dict(sim_threshold=sim_threshold, cross_skill=cross_skill))
