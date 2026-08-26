# -*- coding: utf-8 -*-
"""v2 evaluation suite over the real skill corpus.

Half the tasks sit in the engineering plugin's territory, half in document production, so the
suite spans two very different skill genres. `oracle_skills` names the skills a practitioner
would load. Rubrics are NOT written here: they are produced by two independent agent panels
(task-derived and skill-derived) so that rubric provenance can be reported separately.
"""

TASKS2 = [
dict(id="E1", genre="engineering", oracle_skills=["code-review","testing-strategy"],
 prompt=("A colleague opened a PR that adds a `/export` endpoint: it takes a customer id, queries "
   "orders for that customer, loops over them fetching each order's line items, builds a CSV in "
   "memory and returns it. There are no tests. Review it and say what must change before merge.")),
dict(id="E2", genre="engineering", oracle_skills=["incident-response","debug"],
 prompt=("Checkout is failing for roughly 10% of users since a deploy 40 minutes ago. Error rates are "
   "up but not to 100%, and it does not reproduce in staging. Take it from here.")),
dict(id="E3", genre="engineering", oracle_skills=["architecture","system-design"],
 prompt=("We need to pick between a managed message queue and running our own Kafka cluster for a new "
   "event pipeline handling about 50k events a minute. Two engineers disagree. Produce the decision "
   "record.")),
dict(id="E4", genre="engineering", oracle_skills=["deploy-checklist","testing-strategy"],
 prompt=("We ship v4.2 tomorrow morning. It includes a database migration that drops a column, and a "
   "new pricing feature behind a flag. Decide whether we are ready and produce what the team should "
   "work through.")),
dict(id="E5", genre="engineering", oracle_skills=["tech-debt","architecture"],
 prompt=("Our billing module is the part of the codebase everyone is afraid to touch: 4,000-line files, "
   "no tests, three ways of representing money. Leadership will fund one quarter of cleanup. Tell them "
   "what to do with it.")),
dict(id="E6", genre="engineering", oracle_skills=["debug","incident-response"],
 prompt=("A nightly report job has produced silently wrong totals for an unknown number of days. It "
   "runs fine, exits zero, and nobody noticed until a customer queried an invoice. Work the problem.")),
dict(id="E7", genre="engineering", oracle_skills=["documentation","incident-response"],
 prompt=("After last month's outage we promised a runbook for the payment gateway timeouts that caused "
   "it. Write what the on-call engineer needs at 3am.")),

dict(id="D1", genre="documents", oracle_skills=["docx"],
 prompt=("Legal sent back our 60-page master services agreement as a .docx with their edits. I need to "
   "see exactly what they changed, accept the harmless formatting ones, and leave the substantive ones "
   "for review. Explain precisely how you would do this, naming the specific tools, libraries or "
   "scripts you would run and in what order.")),
dict(id="D2", genre="documents", oracle_skills=["pptx","docx"],
 prompt=("Turn our 20-page quarterly review document into a 12-slide board deck that follows our "
   "existing corporate template, with speaker notes. Explain precisely how you would do this, naming "
   "the specific tools, libraries or scripts you would run and in what order.")),
dict(id="D3", genre="documents", oracle_skills=["xlsx"],
 prompt=("I have a CSV export where the header row is on line 7, there are three junk rows at the "
   "bottom, dates are in two different formats and amounts have currency symbols mixed in. I need a "
   "clean spreadsheet with a summary tab and a chart. Explain precisely how you would do this, naming "
   "the specific tools, libraries or scripts you would run and in what order.")),
dict(id="D4", genre="documents", oracle_skills=["pdf","xlsx"],
 prompt=("We have 40 scanned supplier invoices as PDFs and need the line items in a spreadsheet. Some "
   "are photographs of paper. Explain precisely how you would do this, naming the specific tools, "
   "libraries or scripts you would run and in what order, and where it will go wrong.")),
dict(id="D5", genre="documents", oracle_skills=["mcp-builder","documentation"],
 prompt=("We want our internal inventory API available to Claude as an MCP server. It has about 15 "
   "endpoints, some paginated, some slow. Plan the server and say how you would decide what to expose.")),
]

if __name__ == "__main__":
    from collections import Counter
    print(len(TASKS2), "tasks;", Counter(t["genre"] for t in TASKS2))
    print("oracle skills:", Counter(s for t in TASKS2 for s in t["oracle_skills"]))
