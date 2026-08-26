# -*- coding: utf-8 -*-
"""Token counting via the Anthropic BPE tokenizer (node bridge), with an on-disk cache."""
import hashlib, json, os, subprocess, sys
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
CLI = os.path.join(ROOT, "tools", "count_tokens.js")
CACHE_PATH = os.environ.get("SKILLMERGE_TOKEN_CACHE",
                           os.path.join(os.environ.get("SKILLMERGE_BUILD", "build"), ".token_cache.json"))
_cache = None

def _load():
    global _cache
    if _cache is None:
        try:
            _cache = json.load(open(CACHE_PATH))
        except Exception:
            _cache = {}
    return _cache

def _save():
    os.makedirs(os.path.dirname(CACHE_PATH), exist_ok=True)
    json.dump(_cache, open(CACHE_PATH, "w"))

_warned = [False]


def _estimate(text):
    """Fallback when the node bridge is unavailable.

    Roughly four characters per token, corrected for whitespace. Good enough to keep the budget
    honest to within a few percent; install the bridge for exact counts.
    """
    words = text.split()
    return max(1, int(round(len(text) / 4.2 + len(words) * 0.06)))


def count_many(texts, which="anthropic"):
    c = _load()
    need = [t for t in texts if hashlib.sha1(t.encode()).hexdigest() not in c]
    if need:
        uniq = list(dict.fromkeys(need))
        try:
            out = subprocess.run(["node", CLI], input=json.dumps({"texts": uniq}),
                                 capture_output=True, text=True, check=True).stdout
            r = json.loads(out)
        except Exception:
            if not _warned[0]:
                sys.stderr.write("skillmerge: token bridge unavailable, using an estimate. "
                                 "Run `npm --prefix tools install` for exact counts.\n")
                _warned[0] = True
            r = {"anthropic": [_estimate(t) for t in uniq],
                 "o200k": [_estimate(t) for t in uniq]}
        for t, a, o in zip(uniq, r["anthropic"], r["o200k"]):
            c[hashlib.sha1(t.encode()).hexdigest()] = [a, o]
        _save()
    i = 0 if which == "anthropic" else 1
    return [c[hashlib.sha1(t.encode()).hexdigest()][i] for t in texts]

def count(text, which="anthropic"):
    return count_many([text], which)[0]
