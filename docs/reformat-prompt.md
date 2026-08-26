You are refactoring one professional "skill" document into atoms. An atom pairs a general
obligation with the specific lesson that makes it actionable.

  obligation — ONE imperative sentence, 10-25 words. What the reader must DO and when. Write it so
    that if another skill imposes the same requirement in different words, the two sentences come
    out nearly identical: use plain verbs and plain nouns, and strip tool names, product names,
    file names, formats and domain nouns. This field is the ONLY thing that will ever be compared
    between skills.

  lesson — the substance. Everything that makes the obligation actionable in THIS skill: the reason
    it exists, the mechanism, the exact commands, the failure it prevents, specific names, numbers,
    paths, gotchas. Keep the source's own wording and formatting. If the source had a fenced code
    block, a table, or a file path, reproduce it EXACTLY inside the lesson — do not summarise it,
    do not reformat it, do not invent paths. A lesson may be several paragraphs. This field is
    never merged with another skill's, so do not generalise it.

The split test: strip every lesson from the document and you should be left with a checklist that
is true but useless. Strip every obligation and you should be left with knowledge nobody knows when
to apply. Both halves must be able to fail that way — that means you divided in the right place.

Rules:
  - Cover the whole document. Every instruction, gotcha, table, command and reference must land in
    some atom's lesson. Coverage matters more than elegance.
  - One obligation per atom. If a passage carries three requirements, emit three atoms; they may
    share overlapping lesson text if genuinely needed.
  - Do NOT invent obligations the document does not state, and do NOT invent lessons.
  - Frontmatter, the title, and pure navigation ("see below", a table of contents) are not atoms.
  - kind is "pinned" if the lesson contains a fenced block, a table, a shell/python invocation or a
    file path; otherwise "prose".
  - refs lists any files the lesson points at, exactly as written in the source (e.g.
    "scripts/thumbnail.py"). Empty list if none.
  - anchor is the heading the material came from, verbatim.
