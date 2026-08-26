# -*- coding: utf-8 -*-
"""Dependency-free text utilities: tokenisation, BM25, TF-IDF cosine, agglomerative clustering."""
import math, re
from collections import Counter, defaultdict

STOP = set("""a an the and or but if then than that this these those of in on at to for from by with without
as is are was were be been being it its it's we you they he she i not no do does did done have has had can
could should would may might must will shall over under between into out up down about above below again
further once here there when where why how all any both each few more most other some such only own same so
too very s t just don now which who whom what your our their his her them us me my""".split())

WORD = re.compile(r"[a-z0-9][a-z0-9\-_/\.]*")

def tokenize(text, keep_stop=False):
    toks = WORD.findall(text.lower())
    out = []
    for t in toks:
        t = t.strip(".-_/")
        if not t or len(t) < 2:
            continue
        if not keep_stop and t in STOP:
            continue
        out.append(t)
    return out

class BM25:
    def __init__(self, docs, k1=1.5, b=0.75):
        self.k1, self.b = k1, b
        self.docs = [Counter(d) for d in docs]
        self.len = [sum(c.values()) for c in self.docs]
        self.avg = sum(self.len) / max(1, len(self.len))
        self.df = Counter()
        for c in self.docs:
            for t in c:
                self.df[t] += 1
        self.N = len(self.docs)

    def idf(self, t):
        n = self.df.get(t, 0)
        return math.log(1 + (self.N - n + 0.5) / (n + 0.5))

    def score(self, query_tokens, i):
        c, dl, s = self.docs[i], self.len[i], 0.0
        for t in query_tokens:
            f = c.get(t, 0)
            if not f:
                continue
            s += self.idf(t) * (f * (self.k1 + 1)) / (f + self.k1 * (1 - self.b + self.b * dl / self.avg))
        return s

    def scores(self, query_tokens):
        return [self.score(query_tokens, i) for i in range(self.N)]

def tfidf_vectors(docs):
    """docs: list[list[str]] -> list[dict[str,float]] L2-normalised tf-idf."""
    N = len(docs)
    df = Counter()
    for d in docs:
        for t in set(d):
            df[t] += 1
    vecs = []
    for d in docs:
        tf = Counter(d)
        v = {}
        for t, f in tf.items():
            v[t] = (1 + math.log(f)) * math.log((1 + N) / (1 + df[t]))
        n = math.sqrt(sum(x * x for x in v.values())) or 1.0
        vecs.append({t: x / n for t, x in v.items()})
    return vecs

def cosine(a, b):
    if len(a) > len(b):
        a, b = b, a
    return sum(x * b.get(t, 0.0) for t, x in a.items())

def agglomerative(vecs, threshold):
    """Average-linkage agglomerative clustering on cosine similarity. O(n^2 log n), fine at our scale."""
    n = len(vecs)
    sim = [[0.0] * n for _ in range(n)]
    for i in range(n):
        for j in range(i + 1, n):
            s = cosine(vecs[i], vecs[j])
            sim[i][j] = sim[j][i] = s
    clusters = {i: [i] for i in range(n)}
    while True:
        best, bi, bj = threshold, None, None
        keys = list(clusters)
        for x in range(len(keys)):
            for y in range(x + 1, len(keys)):
                a, b = clusters[keys[x]], clusters[keys[y]]
                s = sum(sim[p][q] for p in a for q in b) / (len(a) * len(b))
                if s > best:
                    best, bi, bj = s, keys[x], keys[y]
        if bi is None:
            break
        clusters[bi] = clusters[bi] + clusters[bj]
        del clusters[bj]
    return [sorted(v) for v in clusters.values()]


def leader_cluster(vecs, threshold, order=None):
    """Deterministic leader (canopy) clustering: O(n*k), no chaining.

    Agglomerative average-linkage is O(n^3) in this implementation and does not scale past a few
    hundred items. Leader clustering assigns each item to the first existing cluster whose LEADER is
    within threshold, otherwise starts a new one. Because membership is judged against the leader
    only, a cluster can never chain out to items dissimilar from its centre - which is the failure
    mode that matters when the thing being clustered is a one-sentence obligation.

    `order` fixes the visit order so the result is reproducible across index rebuilds.
    """
    idx = list(range(len(vecs))) if order is None else list(order)
    leaders, clusters = [], []
    for i in idx:
        best, bj = threshold, None
        for j, lead in enumerate(leaders):
            s = cosine(vecs[i], vecs[lead])
            if s >= best:
                best, bj = s, j
        if bj is None:
            leaders.append(i); clusters.append([i])
        else:
            clusters[bj].append(i)
    return [sorted(c) for c in clusters]
