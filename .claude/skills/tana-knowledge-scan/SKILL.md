---
name: tana-knowledge-scan
description: Scan a Tana Outliner workspace for loose text and connect it to existing knowledge. Loose text means untagged, unlinked notes on day pages, in the Inbox and the Library, plus bare links. Existing knowledge means the person's projects, areas, people, companies, meetings, events, life patterns and other tagged nodes. The scan is read-only and ends in a proposal table; changes happen only after the person approves them, least invasive first. Use this whenever someone asks to scan or sweep their Tana, find loose, orphan or untagged notes, clean or process the Inbox, do a weekly review, connect or combine notes with what they already have, or asks "what did I forget to file", even if they never say "scan".
---

# Tana knowledge scan: find loose text, connect it

A second brain only helps if notes are connected. Notes written quickly on a day page or sent to the Inbox often stay loose: no tag, no link. Nothing can find them, and they never come back. This skill finds them and proposes the smallest change that connects each one to knowledge the person already has.

Before starting, read these from the `tana-supertag-systems` skill:
- `references/tana-mcp-notes.md`, for tool pitfalls, especially "a reference row reports the original's ID";
- `references/second-brain-design.md`, for the capture → connect → surface loop this skill serves.

## Rules

1. **The scan is read-only.** Collect, read and match; then show a proposal table and wait for the OK, group by group.
2. **Use the smallest change that connects.** Adding a link beats tagging, and tagging beats moving. Never rewrite the person's text, never trash their notes, never merge them yourself (Merge node is a UI step).
3. **Use existing knowledge.** Link to tags and nodes the person already uses. Propose a new node or tag only when two or more notes share something that has no home yet, and say so explicitly.
4. **Every match carries evidence and a confidence level:** the matched words and where they were found. 🟢 means an exact name of an existing node, 🟡 a shared topic or event, 🟠 a guess, which becomes a question.
5. **Log every change** (note ID, action, target ID) in the scratchpad so it can be undone.

## 1. Collect candidates

Use the workspace ID `<ws>` from `list_workspaces`. The default scope is the last 30 days of day pages, plus the Inbox and the Library's top level; ask if the person wants more. Always add `{"not":{"childOf":{"nodeIds":["<ws>_TRASH"],"recursive":true}}}`.

| Source | Call |
|---|---|
| Day pages (direct children of day nodes) | `search_nodes {"and":[{"is":"onDayNode"},{"not":{"has":"tag"}},{"created":{"last":30}},{"not":{"is":"chat"}},{"not":{"is":"search"}}, <not trash>]}`, limit 200 |
| Inbox | `get_children <ws>_CAPTURE_INBOX` (keep untagged rows, and tagged rows that are only parked there) |
| Library top level | `search_nodes {"and":[{"childOf":{"nodeIds":["<ws>_STASH"],"recursive":false}},{"not":{"has":"tag"}}]}` |

Save the rows as a JSON list in the scratchpad (e.g. `scan/loose.json`). Big results go to a file, not into the conversation.

The Library's top level also holds integration containers, such as Readwise, Google Calendar Events and Contacts, and AI chats. Never propose moving or tagging these. The script counts the common ones as noise; add any others the person has to `NOISE_NAMES`.

## 2. Plan with the script

```
python3 -I scripts/scan_plan.py plan scan/loose.json --ws <ws>
```

It sorts the candidates into:
- **noise**: empty rows, old dashboard copies, transcript lines, system nodes. Report a count only.
- **links**: bare URLs, by domain.
- **notes**: with their key terms.

It then prints two kinds of ready-to-send queries:
- `linksTo` batches, which show whether something already points at a note;
- one match query per note.

Before running the match queries, prune terms that are too generic (e.g. "Request", "Policy").

## 3. Drop what is already connected

Run the `linksTo` batches. A note that something links to is already connected: drop it, unless it sits in the Inbox (then propose filing it).

## 4. Read each note

Call `read_node` (depth 2) on each remaining note. A title like "Mikkel" only makes sense once you've read its description and children. Cap one run at about 40 notes and offer to continue. While reading, note what the text is:
- a task;
- a meeting note;
- a reflection;
- an idea;
- a reference or link;
- a question for someone.

## 5. Match against existing knowledge

1. **Know the person's map.** Use `list_tags`, plus instances of their core tags: projects, areas, goals, person, company or organization, meetings, events, life patterns, ideas, resources. Which tags they really use comes from `hasType` counts. Title expressions make names long ("ILLUSENIA ||| 💼|${Project Status}…"); the script's `clean()` trims them.
2. **Run the note's match query**, save the result, and filter it:
   ```
   python3 -I scripts/scan_plan.py filter scan/<noteId>.json "term1,term2"
   ```
   `textContains` matches inside words and also inside a node's content: "frak" finds "Frau", and "andrea" finds "Sandra". The filter keeps whole-word matches in the name or description only, and drops transcript lines.
3. **Decide the action and its confidence:**
   - **🟢 Link:** the note names an existing person, project, company or event (e.g. "Mikkel" → `#person` Mikkel).
   - **🟢 Tag:** a bare URL → the person's link tag, with its Source field (e.g. Inbox). A clear task → their task tag. A reflection → their journaling tag.
   - **🟡 Link or field:** the note shares a topic or event with an existing node (e.g. "Opgaver med skatte basse Andrea" ↔ event "Modtage Andrea"). Ask.
   - **🟠 Question:** there's no match but it clearly matters (e.g. "FRAK": what is it?).

   When the target tag has a link field (Linked pattern, Project, Attendees), fill that field instead of adding a plain link.
4. **Find duplicates.** If two loose notes share a title or most of their terms, propose Merge node, as a UI step.

AI-extracted companies such as Google, Apple and LinkedIn, created by meeting agents, are weak targets. Prefer nodes the person made.

## 6. Report and wait

One table per action group, most certain first:

| Note (where) | What it is | Proposed action | Target | Evidence | Confidence |
|---|---|---|---|---|---|

Then give:
- the noise counts;
- the questions;
- one line on what each action changes.

Ask which groups to apply. Approving one group doesn't approve the others.

## 7. Apply approved groups (least invasive first)

| Action | How | Undo |
|---|---|---|
| Link | `import_tana_paste` under the note: `- [[^targetId]]`. The note now links to the target, and the target's References section shows the note. | Remove the reference row with the temporary-node method (`tana-mcp-notes.md`) |
| Fill a link field | `tag` the note if needed, then `set_field_content` (instance field: content = node ID, `mode: append` for multi-value) | Clear the field (`content: null`) |
| Tag | `tag` (add) with an existing tag ID, then `set_field_option` and `set_field_content` from `get_tag_schema`. Triggers on the tag don't fire through the MCP, so tell the person which tag command to run (e.g. their link-tag commands). | `tag` (remove) |
| File | Only if asked: `move_node` under the target with `keepSourceReference: true`, so the day page keeps a reference | Move back |
| Merge | Click list: select both, then Merge node | — |
| New node | Only if approved: `import_tana_paste` with the person's tag, then link the notes to it | Trash the new node |

After each group:
- `read_node` a sample to check the result;
- update the log;
- report what changed, with IDs.

## 8. Keep it going

Offer to run the scan weekly or monthly, for example as part of the person's weekly reflection tag. Suggest one habit that keeps notes from going loose: write "Title #tag" and fill the link field while capturing.

## Definition of done

- Every candidate in scope is counted as noise, already connected, proposed, or a question.
- Every proposal has evidence and a confidence level, and nothing was changed without the OK for its group.
- Applied changes are verified and logged with IDs, and UI-only steps are given as a click list.

## Worked example (Shuaib's workspace, 25 Oct 2026, read-only test)

- **Day pages, last 60 days:**
  - empty rows and old dashboard copies were noise;
  - "Mikkel" (15 Oct, about being a good friend) → 🟢 link to `#person` Mikkel;
  - "Opgaver med skatte basse Andrea" (19 Sep) → 🟡 event "Modtage Andrea";
  - "noter fra møde … landbrug ved FRAK" (1 Sep) → 🟠 no node for FRAK (ask); likely `#meetings`.
- **Inbox:**
  - about 15 Instagram and YouTube URLs → 🟢 tag `#link`, with Source = Inbox;
  - "Grundstammen for strategier" (empty) → 🟠 ask;
  - two `#meetings` nodes parked there (e.g. "Carbon Dry Wash video strategy meeting") → 🟢 link to `#Company` Carbon Dry wash, and file out of the Inbox if wanted.
- **`linksTo`:** none of the loose notes was linked from anywhere.
