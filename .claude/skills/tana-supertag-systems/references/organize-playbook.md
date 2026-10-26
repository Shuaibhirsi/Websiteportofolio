# Organize playbook: a second brain the person can find their way around

Use this when someone wants to tidy their Tana, build a second brain, or "organize my supertags, fields and commands". Organizing changes no data. It adds **references** in a hub so every definition is easy to find, and leaves each definition where it is owned.

## Principles (from Tana's docs, see `tana-concepts.md`)

- **Capture, then structure.** Daily notes and the Inbox are for capture. The Home node holds the wiki and dashboards. Apply supertags to what matters, and let search nodes bring it together. Don't file things by hand.
- **One type per "is a", one field per "has a".** Reuse a field such as Date, Status or Project across tags instead of making a new one with the same name; then one search or view covers every tag. Use Extend for families (`#task` → `#project task`, `#personal task`).
- **Definitions stay owned; organizing uses references.** A definition's owner is its single source of truth: the Schema, a template, or wherever it was created. Show it elsewhere as a reference. Deleting a reference is harmless; deleting an owner trashes what it owns.
- **Start small, grow on demand.** A few core tags (PARA or GTD) and a handful of searches come before any automation.

## The hub pattern

Follow the person's own hub if they have one. If not, propose this shape under Home, tabs view, with one tab per list:

```
⚙️ Supertags, Fields, Searches           (hub)
  🗂️ Organized Supertags                 → references to tag definitions
  🧱 Organized Fields                    → references to field definitions
  ⚡ Organized Commands                  → references to command nodes (and command groups)
  🔎 Organized Searches                  → references to search nodes
  🧩 Templates & extensions              → references to installed template roots
```

- **Use the same categories, with the same emoji, in every list.** A tag's fields, commands and searches then sit in the matching group of each list. Keep the person's category names exactly, even where the wording differs between lists.
- Every list ends with a **"🧾 … to review"** group for anything not yet sorted. Nothing is left out, and nothing is guessed into a wrong group.
- Template plumbing (internal command steps, storage containers) is never listed one by one. List the template's entry points (the commands a person actually runs) and one reference to the template root.

### Worked example: Shuaib's workspace

His hub is Home → DASHBOAD → **Supertags, Fields, Searches**. His categories are:

| Emoji | Supertags group | Fields group |
|---|---|---|
| 🎯 | Core PARA & Action | PARA & Action fields |
| 🧠 | Notes, Reflection & Journaling | Notes & Reflection fields |
| 🤝 | Meetings, Events & People | People, Meetings & Connections |
| 📚 | Resources & Education | Learning & Research fields |
| 💼 | Work, Companies & Connections | Work, Companies & Connections fields |
| 🌱 | Habits & Personal Growth | Habits fields |
| 🎨 | Creative & Outputs | Creative & Outputs fields |
| 🧩 | System & Automation | System & other fields |
| 🧾 | Other existing supertags to review | Other fields to review |
| 📅 / 🔗 / 🧭 | (field-only) | Dates & Scheduling / Links & Sources / Inner work fields (one sub-list per tag) |

- **⚡ Organized Commands** and **🔎 Organized Searches** sit in the same hub (built 25 Oct 2026). They use the supertag group names exactly, and include only the groups that have members, plus 🧾.
- Date fields go to 📅 and URL fields to 🔗, whatever their tag. That was already his own rule.
- A self-contained system, such as the 🧭 inner-work tags, keeps its fields together.
- His own commands live under Home → **SH's Commands**, grouped by the place they serve ("In #link Super tag:", "Daily page"). His saved searches live under Home → **⏩ Fast Info**.
- His older **Core Supertags** and **Fields → Structure → ALL Fields(Chaos)** sections used to *own* definitions. On 25 Oct 2026, with his approval, all 45 tags and 85 fields moved to the Schema, and those sections now hold references. If new definitions appear there, they are new ad-hoc creations: offer to move them the same way.

## The daily page: let the `#day` supertag do the work

The point of supertags is to define something once and reuse it everywhere, so build the daily page in the `#day` tag, never as one-off nodes on a single day. (A first attempt here put searches on one day and asked the person to move them by hand. They rejected it, rightly.)

- **Find the person's own daily tags first.** Look for morning and evening tags they already use (`search_nodes` for instances), e.g. #Daily prep or #Journaling. Reuse them before creating anything.
- **The `#day` template** is the tag's non-field children; every new day gets a copy. Put in:
  - tagged nodes of their daily tags, e.g. `- ☀️ Morning #[[^dailyPrepId]]` and `- 🌙 Evening #[[^journalingId]]`. Their fields appear on each day, ready to fill;
  - a few live searches as direct children, using PARENT for "this day" (e.g. tasks with Due date < PARENT+1). Lists that must show on **every** day are better in the tag's Related content, which renders on all days, including ones created before the template changed. See `visual-design.md`.
- **Clear out the old.** Move old template children to an archive node such as "🗄️ Old day dashboards" with `move_node`. Days already written keep their own copies, which have different IDs.
- **Link working tags in with shared fields.** Add existing instance fields to the daily tag (`- [[^fieldId]]::`, e.g. Linked pattern → `#life pattern`) rather than new look-alikes. In a field, typing a new title creates the linked node, so writing on the day creates the record.
- **Put quick fields first** on each working tag, with the deeper and ✨ AI fields last (reorder by moving the tag's field tuples).
- **Today's page** was created before the change, so it doesn't get the new template. Import the same nodes onto it so it matches.
- **Check every template import:** auto-initialized dates get baked in (see `tana-mcp-notes.md`).

Worked example (Shuaib, 25 Oct 2026):
- The `#Day` template had 4 stacked dashboards. They now sit in DASHBOAD → 🗄️ Old day dashboards.
- The template is now ☀️ Morning #Daily prep, 🌙 Evening #Journaling, 🔴 Still on autopilot (`#life pattern`, NOT 🟡, NOT 🟢) and 🎯 Tasks today (`#task`, NOT DONE, Due date < PARENT+1).
- `#Journaling` gained the shared Linked pattern field plus a new Linked experiment field (instance of `#corrective experience`).

## Procedure

1. **Read the hub.**
   - Call `get_children` on each list and each group. Record the group names, emoji, IDs and current members (`inTrash`!).
   - Note empty rows and dead links for the repair list, but don't touch them.
2. **Inventory.** Scope everything to the workspace and save big results to the scratchpad.
   - `list_tags` (limit 500).
   - `search_nodes {"is":"field"}` (limit 1000).
   - `search_nodes {"is":"command"}`.
   - `search_nodes {"is":"search"}`.
   - Always add `{"not":{"childOf":{"nodeIds":["<ws>_TRASH"],"recursive":true}}}`, then drop anything with `inTrash: true`.
3. **Classify.**
   - **Tags:** by meaning and base type. Unsorted tags go to 🧾. Duplicates go to 🧾 with a note; compare breadcrumbs to tell template copies apart.
   - **Fields:** follow their tags. Run `get_tag_schema` on each organized tag (with `includeEditInstructions: false`). A field goes to the category of the tag that uses it. A field used across categories goes to the most specific shared group (🔗, 📅 or 🧩). Fields used by no tag go to 🧾: these are often AI-extracted one-offs from a document; give a count only, don't list hundreds.
   - **Commands:** follow the tag or place they serve, as shown by their breadcrumb (`SH's Commands > In #link` → the category of #link). Template commands go to the template's category. Post-process and meeting commands go to 🤝.
   - **Searches:** follow the tag they gather. Dashboard searches (PARA, Note Flow) go to 🎯. Skip Tana-made "References to X" searches and searches that are template plumbing.
4. **Show the plan** as a table, list by group, before writing. If the person has already asked you to build the lists, build them and show the result instead; the work only adds reference rows, and they can rename or move groups afterwards.
5. **Write.**
   - Create any missing list or group with `import_tana_paste` under the hub, using the same emoji and names.
   - Fill each group with reference rows, `- [[^<id>]]`, one import per group, in display order.
   - Don't use `move_node` on definitions to organize them.
   - Test one group first, and check with `get_children` that the rows are references (they report the original's ID and `docType`).
6. **Verify.** Call `get_children` on every group you wrote: the expected count, nothing with `inTrash: true`, and no duplicate rows.
7. **Upkeep.** Add two searches to the hub's 🧾 groups:
   - "🆕 New tags" (`IS TAG` + `CREATED LAST 30 DAYS`);
   - "🆕 New fields" (`IS FIELD` + `CREATED LAST 30 DAYS`).

   Suggest a monthly 10-minute review that sorts new items into groups. This is the "stray tag" search from Tana's schema-audit guide.

## Second-brain checks to offer (advice, not edits)

- Is there one capture path? Daily notes or Inbox, plus a "Inbox to process" search.
- Do tasks belong to projects, and projects to areas or goals? Check the fields and their "Used in" counts.
- Are there same-name fields that should be one (Date ×7, Status ×4)? These are candidates for Merge node in the UI.
- Are there tags no one uses ("Used 0 times")? Archive or merge them.
- Does each core tag have a home-page search, and a supertag-page tab with instructions?
