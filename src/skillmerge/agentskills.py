# -*- coding: utf-8 -*-
"""Native reader for the Agent Skills format (SKILL.md + progressive-disclosure assets).

v1 indexed a corpus we generated ourselves. v2 indexes skills as they are actually written:
YAML frontmatter of varying shape, headings at several levels, fenced code, tables, ASCII
diagrams, argument placeholders, and links into references/ and scripts/.

Two fragment classes come out of this:

  guidance : prose obligations. Mergeable across skills; this is where redundancy lives.
  pinned   : anything whose value depends on the skill it came from - fenced code, tables,
             invocation syntax, and any text pointing at a file that ships with the skill.
             Never merged, never paraphrased, carried verbatim with its asset pointers.

Getting that split right is the whole difference between composing skills and mangling them.
"""
import os, re, glob, hashlib
try:
    import yaml
except ImportError:
    yaml = None

FENCE = re.compile(r"^(```|~~~)")
FENCE_ANY = re.compile(r"^(```|~~~)", re.M)
HEAD = re.compile(r"^(#{1,6})\s+(.*?)\s*#*\s*$")
LINKPATH = re.compile(r"\]\(([^)]+\.(?:md|py|sh|js|ts|json|ya?ml|csv|txt))\)")
BAREPATH = re.compile(r"(?:^|[\s`(])((?:\./|\.\./)?(?:scripts|references|assets|examples|templates)/[\w\-./]+)")
ARGPH = re.compile(r"@?\$\d|\{\{[^}]+\}\}|<[A-Z_]{3,}>")
ASSET_DIRS = ("references", "scripts", "assets", "examples", "templates")
TABLE = re.compile(r"^\s*\|.*\|\s*$", re.M)
ASCIIBOX = re.compile(r"[─-╿]{3,}")

def split_frontmatter(raw):
    if not raw.startswith("---"):
        return {}, raw
    end = raw.find("\n---", 3)
    if end == -1:
        return {}, raw
    block, body = raw[3:end], raw[end + 4:]
    meta = {}
    if yaml is not None:
        try:
            meta = yaml.safe_load(block) or {}
        except Exception:
            meta = {}
    if not meta:  # tolerant fallback for frontmatter YAML will not take
        for line in block.splitlines():
            if ":" in line and not line.startswith(" "):
                k, v = line.split(":", 1)
                meta[k.strip()] = v.strip().strip('"')
    return meta, body.lstrip("\n")

def _blocks(body):
    """Yield (kind, text) top-level blocks, never splitting inside a fence."""
    lines, out, buf, fence = body.splitlines(), [], [], None
    for ln in lines:
        m = FENCE.match(ln)
        if fence:
            buf.append(ln)
            if m and ln.strip().startswith(fence):
                out.append(("fence", "\n".join(buf))); buf, fence = [], None
            continue
        if m:
            if buf:
                out.append(("text", "\n".join(buf))); buf = []
            fence = m.group(1); buf = [ln]; continue
        buf.append(ln)
    if buf:
        out.append(("fence" if fence else "text", "\n".join(buf)))
    return out

def _sections(body):
    """Split into (level, heading, content) at any heading, fences kept intact."""
    secs, cur = [], [0, None, []]
    for kind, text in _blocks(body):
        if kind == "fence":
            cur[2].append(text); continue
        for ln in text.splitlines():
            h = HEAD.match(ln)
            if h:
                secs.append(cur); cur = [len(h.group(1)), h.group(2), []]
            else:
                cur[2].append(ln)
    secs.append(cur)
    return [(l, h, "\n".join(c).strip()) for l, h, c in secs if "\n".join(c).strip() or h]

def _is_pinned(text):
    if FENCE_ANY.search(text):
        return True
    if ASCIIBOX.search(text) or len(TABLE.findall(text)) >= 2:
        return True
    if LINKPATH.search(text) or BAREPATH.search(text) or ARGPH.search(text):
        return True
    return False

def _refs(text):
    r = set(LINKPATH.findall(text)) | set(m for m in BAREPATH.findall(text))
    return sorted(x.lstrip("./") for x in r)

def _split_long(text, max_chars=1400):
    """Sub-split an oversized prose section on blank lines, keeping fences whole."""
    if len(text) <= max_chars:
        return [text]
    parts, buf, n = [], [], 0
    for kind, chunk in _blocks(text):
        pieces = [chunk] if kind == "fence" else re.split(r"\n\s*\n", chunk)
        for p in pieces:
            p = p.strip()
            if not p:
                continue
            if n + len(p) > max_chars and buf:
                parts.append("\n\n".join(buf)); buf, n = [], 0
            buf.append(p); n += len(p)
    if buf:
        parts.append("\n\n".join(buf))
    return parts

def read_skill(skill_dir):
    path = os.path.join(skill_dir, "SKILL.md")
    raw = open(path, encoding="utf-8", errors="replace").read()
    meta, body = split_frontmatter(raw)
    name = str(meta.get("name") or os.path.basename(skill_dir))
    assets = []
    for d in ASSET_DIRS:
        p = os.path.join(skill_dir, d)
        if os.path.isdir(p):
            for f in sorted(glob.glob(os.path.join(p, "**", "*"), recursive=True)):
                if os.path.isfile(f):
                    assets.append(os.path.relpath(f, skill_dir))
    frags, trail = [], []
    for level, heading, content in _sections(body):
        if not content.strip():
            continue
        trail = trail[:max(0, level - 1)] + ([heading] if heading else [])
        crumb = " > ".join(x for x in trail if x)
        for i, piece in enumerate(_split_long(content)):
            if len(piece.strip()) < 40:
                continue
            frags.append(dict(
                skill=name, dir=skill_dir, heading=heading or "(intro)", crumb=crumb,
                level=level, part=i, text=piece.strip(),
                kind="pinned" if _is_pinned(piece) else "guidance",
                refs=_refs(piece),
                id=hashlib.sha1((name + crumb + str(i) + piece[:80]).encode()).hexdigest()[:12]))
    return dict(name=name, dir=skill_dir, meta=meta,
                description=str(meta.get("description", "")).strip(),
                assets=assets, fragments=frags, raw=raw)

def discover(roots):
    out = []
    for root in roots:
        for p in sorted(glob.glob(os.path.join(root, "**", "SKILL.md"), recursive=True)):
            out.append(read_skill(os.path.dirname(p)))
    seen, uniq = set(), []
    for s in out:                      # de-duplicate skills that are synced in two places
        if s["name"] in seen:
            continue
        seen.add(s["name"]); uniq.append(s)
    return uniq
