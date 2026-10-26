---
name: tana-supertag-systems
description: Build, repair and organize a Tana Outliner workspace through the Tana Outliner MCP. Covers research-backed supertag systems (tags, typed fields, AI fields, voice, reference cards, live searches, dashboards); auditing the trash and fixing broken references, trashed tags, fields or commands, duplicate templates and dead links; and organizing a second brain so supertags, fields, commands and searches sit in the person's own category structure. Use this whenever someone mentions Tana, supertags, fields, live searches, commands, their trash, broken or trash-can links, a messy schema or daily page, cleaning up, PARA, GTD or a "second brain", or hands over a Tana build plan, even if they never say "supertag". Use it especially when content must be research-backed or touches mental health and self-reflection.
---

# Tana: build, repair, organize

Most requests are one of three jobs, and many are a mix:

| Job | Typical request | Main reference |
|---|---|---|
| **Build** | "Make me a system for X in Tana" | this file, sections 4 to 6 |
| **Repair** | "I cleaned up and links broke", "check my trash" | `references/repair-playbook.md` |
| **Organize** | "Help me organize my second brain", "sort my fields and commands", "my daily page is messy" | `references/organize-playbook.md` |
| **Scan** | "Find my loose notes", "process my Inbox", "connect notes to what I have" | the separate `tana-knowledge-scan` skill |

How Tana itself behaves (owners, references, trash, Schema, fields, commands, searches) is in `references/tana-concepts.md`, taken from Tana's official docs. Read it before the first write of a session.

## 0. Rules that apply to every job

1. **Read before you write.** Inventory first; propose; then change.
2. **Separate adding from changing.** Additive work the person asked for can go ahead: new tags, new nodes, reference rows in a hub. Anything that moves, renames, trashes or restores *existing* content needs the person's OK on a concrete list.
3. **Organize with references, never by moving definitions.** A definition's owner is its source of truth. Deleting an owner trashes everything it owns, which is the most common way people break their own Tana.
4. **Never empty the trash, or advise emptying it, while anything live still points into it.** Once emptied, those links can't be restored.
5. **A reference row reports the original's ID.** Never `trash_node`, `edit_node` or `move_node` (without `sourceParentId`) an ID you got from a list of references. Doing so changes the original.
6. **Back up before a cleanup.** Ask for Export workspace as JSON before repairs or large reorganizations.
7. **Log every change** (ID, before, after) so it can be undone, and never claim a UI-only step is done.
8. **Design in supertags.** Before proposing anything, run the design check in `references/second-brain-design.md`: reuse, link, surface in a template, keep friction low.

## 1. Preflight (read before you write)

1. `list_workspaces`: note the workspace ID and home node. The trash is `<ws>_TRASH`, the Schema `<ws>_SCHEMA`, the Library `<ws>_STASH`, the Inbox `<ws>_CAPTURE_INBOX`.
2. Read the person's own rules and conventions. Many people keep a node like "Operating rules" or "How I use Tana". Follow it: it may cap how much work fits in one sitting, or say where new templates go.
3. **Find their hub.** This is where they list supertags, fields, commands and searches, for example a "Supertags, Fields, Searches" node on a dashboard. Read its groups with `get_children`. New tags, fields, commands and searches you create get a reference row in the matching group, using the same emoji and category names.
4. `list_tags` (limit 500): check planned names for collisions and reuse the colour palette. Search for existing fields by name before making new ones; reuse a Date, Status or Project field rather than making a second one.
5. `get_tag_schema` on one or two tags they like (a journaling or weekly-review tag is ideal). Copy their style: emoji in options, how AI field instructions are phrased (`${sys:context}`), and the structure of `voiceGreeting` and `voiceInstructions`.
6. Check the network before planning research. Run `curl -sS "$HTTPS_PROXY/__agentproxy/status"` and test the hosts you need. Tana's docs are on `outliner.tana.inc`. If a host returns 403 or 000, name it and tell the person they can allow it under the environment's Network access setting. Then carry on with what works, and label anything you couldn't open as Low.
7. Make one cheap write early, but only if the job writes. If it fails with "No approval received", stop and ask rather than retrying.

Big outputs (trash, `IS FIELD`, `IS COMMAND`) overflow the tool result. Save them to the scratchpad and process them with `python3 -I`.

## 2. Repair: trash and broken links

Follow `references/repair-playbook.md`. The short version:

1. Inventory the trash: `get_children(<ws>_TRASH, limit 1000)`, saved to a file. Then run `python3 -I scripts/trash_audit.py trash.json` to list the high-risk items (trashed tags, fields, commands, searches) and get `linksTo` query batches.
2. Run the batches to find live nodes that point into the trash, then pinpoint each target.
3. Call `get_children` on every hub group and flag rows with `inTrash: true` and "unknown (or no access)".
4. Read each broken definition (`read_node` depth 2 or 3) to learn what it did. Find live duplicates by name with `hasType SYS_T01/SYS_T02` and compare breadcrumbs.
5. Report the findings by risk (🔴 in use, 🟠 cosmetic, 🟡 duplicates, 🟢 safe), each with a proposed fix. Wait for the OK.
6. Repair in order. Restore trashed originals with `move_node` out of the trash: the ID is kept, so references heal. Add references to live copies. Leave reference removals, merges and tag-config checks to the person, as a click list.
7. Verify (`inTrash: false`, hub groups clean), and say when it is safe to empty the trash.

## 3. Organize a second brain

Follow `references/organize-playbook.md`. The short version:

1. Read the person's hub and categories exactly as they are.
2. Inventory tags, fields (`is: field`), commands (`is: command`) and searches (`is: search`). Leave out trashed items and template plumbing.
3. Classify:
   - tags by meaning;
   - fields by the tags that use them (`get_tag_schema`);
   - commands by the tag or place they serve;
   - searches by the tag they gather.

   Unsorted items go to the "🧾 … to review" group.
4. Show the plan, or the result if the person already asked you to build it. Fill each group with reference rows (`- [[^id]]`), one import per group. Mirror the same emoji categories across Supertags, Fields, Commands and Searches. To place a new group, `move_node` it with `position: before/after`; only ever move group nodes you created.
5. Verify with `get_children`, and add "new tags" and "new fields" searches for monthly upkeep.
6. Offer second-brain advice (capture path, PARA links, duplicate fields to merge) as advice, not edits.
7. Build the daily page in the `#day` supertag, never as one-off nodes on a single day. Its template reuses the person's own daily tags and holds live searches that use PARENT. See "The daily page" in the playbook.

## 4. Build: research with confidence tiers

Every concept that goes into Tana as a fact needs a source and a tier. The rubric, the fallback wording and the label format are in `references/sources-and-safety.md`; read it before writing any card text.

- 🟢 High: peer-reviewed article, NCBI/StatPearls, the primary book, or official product docs, read directly.
- 🟡 Medium: university teaching material, or several consistent secondary sources.
- 🟠 Low: search snippets, flashcards, blogs, or anything you could not open.

Verification falls back instead of blocking: an unreadable source becomes a labelled Low claim, never a silent gap and never an invented citation.

## 5. Build: design and build order

Design:
- **For any page people look at** (day page, dashboard, entity page), also read `references/visual-design.md`: placement zones, views by job, one icon per type, and what the MCP can set.
- **First read `references/second-brain-design.md` and answer its design check.** Every structure lives in a supertag or its template, reuses the person's own tags and fields, links records with instance fields, and surfaces through searches in templates. Never build one-off structures on a single node.
- Split reference cards (pre-filled instances) from working records (what the person logs). Link records to cards with `instance` fields, so each card can hold live searches of everything linked to it.
- Use the workspace palette and emoji-first descriptions and options. Show progress as options (▱▱▱▱▱ to ▰▰▰▰▰) and status as 🔴/🟡/🟢. Include a ❔ "Not sure" option, and allow several values where the honest answer can be "several".
- Make each field description say what to write, with a short example in brackets.
- Use Extend for families of tags instead of copying fields.

Build order:
1. `create_tag` for every tag (name, colour, description, `showCheckbox` where something gets done).
2. `add_field_to_tag`, **one field at a time per tag**, because field order is creation order. Reuse existing fields where they mean the same thing. Create the tag an instance field points to first.
3. AI fields: a `plain` field plus `aiInstructions`, in the person's instruction style.
4. `get_tag_schema` on every tag; record all field and option IDs.
5. `import_tana_paste` for content, with tags and fields by ID. Keep each import bounded (one card or one section per call), one line per node, no numbered lists.
6. Searches and dashboard: `%%search%%` nodes with the view on the search node itself, and a parent with `%%view:tabs%%` for tabs. Searches cannot nest. Operator IDs are in `references/tana-mcp-notes.md`.
7. Add a reference row for every new tag, field, command and search to the matching group in the person's hub.
8. Test with one realistic node per working tag under a temporary parent. Verify each search exists as docType "search" and that the equivalent `search_nodes` query returns the test node. Then `trash_node` the temporary parent.
9. Re-run `get_tag_schema` on all tags and read the dashboard (depth 3 or less).

## 6. Build: what the MCP cannot do (hand over a click list)

There is no MCP tool for:
- command nodes, or a tag's command menu;
- event triggers (On added, On removed, checked);
- tag configuration such as audio-enabled tags, post-process commands and Related content;
- a field's type or source supertag;
- Merge node;
- deleting a dead "unknown (or no access)" link (a live reference row can be removed: see `references/tana-mcp-notes.md`);
- emptying the trash.

Build everything else, then give a numbered click-by-click list. Include the "Run AI fields" command, Ask AI prompts written out in full, and triggers such as "On added: set Status to 🟡, set First noticed to today". Remember that triggers don't fire for nodes the MCP creates. Never claim these steps are done.

## 7. Report and definition of done

Finish with a short report:
- what was built, repaired or organized, with IDs;
- the click list;
- sources with tiers (for builds);
- caveats: blocked hosts, unread sources, searches that stay empty until real entries exist, UI settings you couldn't see;
- for self-reflection systems, the scope line from `references/sources-and-safety.md`.

"Done" means the definition of done for the job is true. A confidence percentage doesn't count.

- **Build:**
  - every tag's schema matches the design, including AI instructions;
  - every reference card has its fields, both sides and a sources line with tiers;
  - every search returned its test node before the test nodes were trashed;
  - nothing unverified is labelled 🟢;
  - new items are referenced in the hub;
  - the click list is delivered.
- **Repair:**
  - every 🔴 and 🟠 item is restored, re-pointed, or explicitly left to the person with a click list;
  - re-checks show `inTrash: false` for restored items and clean hub groups;
  - the person knows whether it is safe to empty the trash.
- **Organize:**
  - every live tag, field, command and search is in a group or in 🧾 review (plumbing listed by count);
  - no group row points into the trash;
  - upkeep searches exist.

## Reference files

- `references/second-brain-design.md`: the capture → connect → surface loop, design principles and the design check to run before every proposal.
- `references/visual-design.md`: what Tana creators do (with sources and tiers), placement zones, views by job, icons and banners, and what the MCP can set.
- `references/tana-concepts.md`: how Tana Outliner works, with sources: owners and references, trash, supertags, fields, commands, searches, workspace layout, templates, schema audit, MCP.
- `references/repair-playbook.md`: the trash and broken-link audit, audit traps, the repair table and verification.
- `references/organize-playbook.md`: second-brain principles, the hub pattern (with Shuaib's categories as a worked example), the classification procedure and upkeep.
- `references/tana-mcp-notes.md`: tool notes, pitfalls, Tana Paste and search syntax. Read it before the first `import_tana_paste`.
- `references/sources-and-safety.md`: the confidence rubric, label format, fallback wording, and safety wording for self-reflection systems.
- `scripts/trash_audit.py`: turns a saved trash listing into an inventory and `linksTo` query batches.
