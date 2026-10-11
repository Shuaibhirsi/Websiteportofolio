---
name: tana-supertag-systems
description: Research, design, build and verify a supertag system in Tana (tags, typed fields, emoji options, AI fields, voice set-up, reference cards, live searches, a tabbed dashboard) through the Tana Outliner MCP, with every factual claim sourced and confidence-labelled. Use this whenever someone wants to build, extend or fix a Tana system, template, tracker, dashboard or "operating system" built on supertags (journaling, habits, self-reflection, learning, research libraries, CRM-style trackers), or hands over a Tana build plan or handoff document, even if they never say "supertag". Use it especially when the content must be research-backed or touches mental health and self-reflection.
---

# Tana supertag systems

Turn a request like "build me a research-backed system in Tana for X" into a working, verified set of supertags, content and searches, plus an honest report of what is sourced, what is not, and what the person still has to click.

The workflow below is ordered on purpose. Tana's MCP is create-heavy and update-light: Tana Paste cannot edit existing nodes, field order is creation order, and searches over a brand-new tag return nothing. Most mistakes come from doing steps out of order.

## 1. Preflight (read before you write)

1. `list_workspaces`: note the workspace ID and home node.
2. `list_tags`: check every planned tag name for collisions, and note the colours already in use. Reuse that palette so the new tags look native.
3. Read the person's own rules and conventions. Many people keep a node like "Operating rules" or "How I use Tana". Follow it: it may cap how much work fits in one sitting, or say where new templates go. Ignore AI-notes inside it that belong to other projects.
4. `get_tag_schema` on one or two tags they clearly like (a journaling or weekly-review tag is ideal). Copy their style: emoji in options, how AI field instructions are phrased (`${sys:context}`), and the structure of `voiceGreeting` and `voiceInstructions`.
5. Check the network before planning research. Run `curl -sS "$HTTPS_PROXY/__agentproxy/status"` and test one source URL. If source hosts return 403 or 000, the environment's network policy blocks them. Tell the person which hosts and that they can allow them under the environment's Network access setting. Then carry on with search-summary leads and label them Low, rather than stalling or guessing.
6. Make one cheap write early (for example the first `create_tag`). If it fails with "No approval received", the write tools were never allowed. Stop and ask for permission rather than retrying.

`read_node` deeper than 3 levels can time out on big outlines; read in slices.

## 2. Research with confidence tiers

Every concept that goes into Tana as a fact needs a source and a tier. The rubric, the fallback wording and the label format are in `references/sources-and-safety.md`; read it before writing any card text.

The short version:
- 🟢 High: peer-reviewed article, NCBI/StatPearls or the primary book, read directly (by you or a prior session that recorded it).
- 🟡 Medium: university teaching material, or several consistent secondary sources.
- 🟠 Low: search snippets, flashcards, blogs, or anything you could not open.

Fan out research when you can: one agent per source cluster, then an adversarial reviewer told to refute every claim and lower any tier the evidence does not support. Verification falls back instead of blocking: an unreadable source becomes a labelled Low claim, never a silent gap and never an invented citation.

## 3. Design

- Split reference cards from working records. Reference cards are pre-filled instances (for example 8 stage cards). Working tags are what the person logs (check-ins, patterns, experiments).
- Link working records to reference cards with `instance` fields. Then each card can hold live searches of everything linked to it.
- If the person wants to see "both sides" of something, give each card two child groups (🌿 healthy side, ⚠️ risky side) and make the working tags feed one side each.
- Aesthetics that work in Tana: one colour per tag from the existing palette; an emoji at the start of descriptions and option labels; progress bars as options (▱▱▱▱▱ to ▰▰▰▰▰); status as 🔴/🟡/🟢 options; card titles like "🌱 Stage 1 · Trust vs Mistrust · Hope".
- Field descriptions are shown when filling a field. Make each one say what to write, with a short example in brackets.
- Prefer multi-value options when the honest answer can be "several" (for example possible causes), and always include a ❔ "Not sure" option.

## 4. Build order

1. `create_tag` for every tag: name, colour, description, `showCheckbox` where something gets "done". Voice text can be set now or later with `set_tag_metadata`.
2. `add_field_to_tag`, **one field at a time per tag**. Field order in Tana is creation order, so never add two fields to the same tag in parallel. Different tags can go in parallel. Create the tag an instance field points to first.
3. AI fields: create a `plain` field, then set its instructions (`aiInstructions` on create, or `set_field_metadata` later). Follow the person's existing instruction style.
4. `get_tag_schema` on every tag and record all field and option IDs. Everything after this references IDs, not names.
5. `import_tana_paste` for content, with tags and fields by ID (`#[[^tagId]]`, `[[^fieldId]]:: value`). Keep each import bounded: one card or one dashboard section per call is safer than everything at once. No numbered lists. Headings only for long-form text. Each node is one line.
6. Searches and dashboard: `%%search%%` nodes, with the view on the search node itself (`%%view:table%%` and so on). A parent with `%%view:tabs%%` turns its children into tabs. Searches cannot nest. Operator IDs are in `references/tana-mcp-notes.md`.
7. Test: create one realistic test node per working tag, fill the fields, link it to a card, and confirm with `search_nodes` that each search would pick it up. Then `trash_node` every test node (soft delete).
8. Re-run `get_tag_schema` on all tags and `read_node` (depth 3 or less) on the dashboard. Confirm nothing is empty, mislabelled or missing a source.

## 5. What the MCP cannot do: hand over a click list

There is no MCP tool for command nodes, adding commands to a tag's menu, or supertag event triggers ("On added", "On removed", checkbox events). Build everything else, then give the person a numbered click-by-click checklist for these. Include:
- the "Run AI fields" command on each working tag,
- Ask AI help commands with prompts written out in full (they paste them in),
- event triggers such as "On added: set Status to 🟡, set First noticed to today",
- any cross-node automation, flagged as optional and fiddly.

Never claim these are done.

## 6. Report

Finish with a short report:
- what was built, with tag and node IDs,
- the click list,
- sources with tiers, and which claims are Low and why,
- caveats (blocked hosts, unread transcripts, empty searches until real entries exist),
- the scope line for self-reflection systems (see `references/sources-and-safety.md`).

"Done" means every item in the definition of done below is true, not a confidence percentage.

Definition of done:
- every tag's schema matches the design, including AI instructions;
- every reference card has its fields, both sides and a sources line with tiers;
- every search returned its test node before the test nodes were trashed;
- nothing unverified is labelled 🟢;
- the click list is delivered.

## Reference files

- `references/tana-mcp-notes.md`: tool-by-tool notes, Tana Paste syntax for views, searches, dates and checkboxes, and known pitfalls. Read it before the first `import_tana_paste`.
- `references/sources-and-safety.md`: the confidence rubric, how to label claims inside Tana, fallback wording, and safety and scope wording for self-reflection and mental-health systems. Read it before writing card text.
