# Designing a technical second brain in Tana

The person wants a second brain that **works for them**. Notes should connect themselves, and the right things should show up where they are needed, with little upkeep. Tana does this through supertags, not through hand-made pages. Use this file for every design proposal, and run the design check at the end before you show a plan.

## The loop: capture → connect → surface

1. **Capture** should be fast. The person writes a title, adds a tag and fills a few fields, on the day page, in the Inbox or by voice. Nothing needs filing.
2. **Connect** means each record links to what it belongs to through **instance fields**: Project, Area, Person, Linked pattern. A mention in plain text doesn't count, because searches and views can't use it. Loose text left over gets connected later by the scan skill (`tana-knowledge-scan`).
3. **Surface** means that what matters appears by itself, through searches **inside tag templates**:
   - the day shows today's open loops;
   - a project shows its tasks and notes;
   - a person shows their meetings and open asks.

   A design that skips a step breaks the second brain: things pile up uncaptured, sit unconnected, or never come back.

## Principles

- **Supertag first.** Anything that repeats becomes a tag, and anything that should appear on every X goes in X's template (`#day`, `#project`, `#person`). Never build one-off structures on a single node and ask the person to copy or move them by hand. That is the mistake this file exists to prevent.
- **One concept, one tag; one property, one field.** Before creating anything:
  - search tags (`hasType SYS_T01`) and fields (`is: field`) by name;
  - reuse a field across tags with `- [[^fieldId]]::` under the tag;
  - use Extend for families (`#task` → `#project task`).

  Same-name copies split every search and view, which is why Shuaib's workspace has Date ×7 and Status ×4.
- **Link both ways with one field.** A field on the record (e.g. Linked pattern on `#Journaling`) plus a search in the target tag's template ("everything where Linked pattern = PARENT", or LINKS TO PARENT) means each target page assembles itself. Put that search in the target's template once, and every instance gets it.
- **Reuse the person's own tags before making new ones.** Their daily, journaling, meeting and task tags carry their habits. Extend or link them; don't run a parallel system beside them. Search for real instances (`hasType`) to see which tags they actually use.
- **Keep friction low.** Quick fields come first, at most about five before the person sees value. Deeper fields and ✨ AI fields go last. Use defaults (e.g. Task Status = 🟡 In Backlog) and auto-initialized dates. Make status options emoji-first with a ❔ "Not sure".
- **Few surfaces, each with a job.** That means the day page, the entity pages (project, person, area) and one hub. Prefer one live search in the right template over a dashboard of ten lists. Stacked dashboards are why people stop opening a page.
- **Automation belongs to the tag**: templates, AI fields, and commands on the tag. Triggers don't fire when the MCP creates nodes, so give the person a click list for those, and test the flow by hand.
- **Design for day 100, not day 1.** Ask how this looks with 300 entries. Lists need a time window or a status filter (NOT DONE, NOT 🟢, CREATED LAST 30 DAYS). Hubs need a 🧾 review group, and a monthly scan catches loose notes.
- **Safe to clean.** Definitions live in the Schema, and dashboards hold references to them. Then deleting a dashboard never breaks data (see `repair-playbook.md`).

## Design check (answer before proposing)

| Question | Good answer |
|---|---|
| Does a tag for this already exist, and is it used? | Reuse or extend it; a new tag only if nothing fits |
| Which existing fields can be reused? | Listed by ID; each new field has a reason |
| What does each record link to? | At least one instance field to a project, area, person or topic |
| Where does it surface, and in which template? | Named template plus search; no one-off nodes |
| What does the person type to capture one? | Title + tag + ≤5 quick fields |
| What stops lists growing forever? | A status, done or date filter on every search |
| What can't the MCP do here? | A click list, kept short |
| Will deleting a dashboard break anything? | No: definitions live in the Schema |

If a row has no good answer, fix the design before showing it. When presenting, show a small preview of the day or record as the person will see it, as in the daily-page preview that the person picked on 25 Oct 2026.
