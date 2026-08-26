# The atom: one obligation, one lesson

v2 failed because merging deleted content. It asked "can one instruction replace both?" and, when
the answer was yes for the *imperative* but no for the *substance*, it kept the imperative and threw
the substance away. An independent panel rejected 56 of 60 such merges.

v3 separates the two axes that were being conflated.

    atom = {
      obligation : ONE imperative sentence. What the practitioner must DO, and the condition under
                   which they must do it. Written to be comparable across skills: plain verbs, no
                   tool names, no product names, no file names. This is the ONLY field that is ever
                   compared or merged.
      lesson     : the specific knowledge that makes the obligation actionable HERE — the reason,
                   the mechanism, the exact command, the failure it prevents, the numbers, the
                   names. Verbatim where the source was verbatim. NEVER merged, NEVER paraphrased
                   into another skill's wording, NEVER dropped when its obligation merges.
      kind       : "prose" | "pinned"  (pinned = contains code, a table, an invocation, or a path)
      refs       : files the lesson points at, relative to the source skill directory
      skill      : source skill name
      anchor     : the heading trail it came from
    }

Merging rule: two atoms merge iff their obligations express the same requirement. The merged atom
carries ONE obligation and EVERY contributing lesson, each labelled with its source skill. Content
is never lost by merging — only restated once instead of N times.

Budget rule at composition time: the obligation is cheap and always included; lessons are ranked and
included as budget allows, starting with lessons from routed skills. Under a tight budget a reader
gets the obligation plus the best lesson; under a generous one, all of them. v2 had no such lever —
it could only drop whole fragments.
