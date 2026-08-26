# -*- coding: utf-8 -*-
"""Mechanical pass over a LaTeX draft for the writing skill's invariants."""
import re, sys, unicodedata
path = sys.argv[1]
raw = open(path, encoding='utf-8').read()
# strip the bibliography, where page ranges follow their own convention
body = raw.split(r'\bibliographystyle')[0]
lines = body.splitlines()
issues = []
def flag(kind, ln, text): issues.append((kind, ln, text.strip()[:120]))

DASHES = ['—', '–', '‒', '−']
for i, ln in enumerate(lines, 1):
    for d in DASHES:
        if d in ln: flag('unicode dash', i, ln)
    if '---' in ln or re.search(r'(?<![0-9])--(?![0-9])', ln): flag('latex dash', i, ln)
    if re.search(r'\s[-]\s', ln): flag('spaced hyphen', i, ln)
    if re.search(r'\s[!?;:]', ln): flag('space before punctuation', i, ln)

FLIP = [r"it'?s not\b", r"is not about\b", r"\bnot about\b", r"\bless by\b.*\bthan by\b",
        r"what actually matters", r"\bisn'?t\b.*\bit'?s\b", r"\bnot because\b.*\bbut because\b"]
BANNED = ['leverage', 'ecosystem', 'landscape', 'the space', 'synergy', 'paradigm', 'journey',
          'stakeholder', 'insane', 'wild', 'crazy', 'mind-blowing', 'game-changer',
          'revolutionary', 'massive', 'huge', 'incredibly', 'extremely', 'novel',
          'it should be noted', 'plays a crucial role', 'sheds light on',
          'growing body of literature', 'delve', 'realm', 'tapestry', 'testament']
FRENCH = [r'\bactually\b', r'\beventually\b', r'\binformations\b', r'\badvices\b',
          r'\bfeedbacks\b', r'\bresearches\b', r'\bdo not hesitate\b', r'\bindeed\b',
          r'\bpermits to\b', r'\bpossibility to\b', r'\bassist to\b', r'\bto precise\b']
low = body.lower()
for i, ln in enumerate(lines, 1):
    l = ln.lower()
    for p in FLIP:
        if re.search(p, l): flag('possible contrast-flip', i, ln)
    for w in BANNED:
        if re.search(r'\b' + re.escape(w), l): flag(f'banned: {w}', i, ln)
    for p in FRENCH:
        if re.search(p, l): flag('francophone check', i, ln)

# "significant" used outside a statistical sense
for i, ln in enumerate(lines, 1):
    if re.search(r'\bsignifican', ln.lower()) and not re.search(r'signific.*(level|5\\%|statistic)', ln.lower()):
        flag('significant (check statistical)', i, ln)

# thousands separators and decimal points
for m in re.finditer(r'\b\d{4,}\b', body):
    s = m.group(0)
    ctx = body[max(0, m.start()-40):m.start()]
    if 'tokens' in ctx or 'total' in ctx: flag('unseparated thousand', 0, s + ' near: ' + ctx[-50:])
for m in re.finditer(r'\d+,\d{1,2}\b(?!\d)', body):
    flag('decimal comma?', 0, m.group(0))

if not issues:
    print("clean: no invariant violations found")
else:
    for k, ln, t in issues: print(f"{k:34s} L{ln:<5d} {t}")
print(f"\n{len(issues)} flags")
