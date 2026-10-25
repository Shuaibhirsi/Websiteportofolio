# Repair playbook: trash, broken links and leftovers

Use this when someone says "I cleaned up and now things are broken", "check my trash", "my references show a trash can", or before any big cleanup. The audit is read-only. Each repair is a separate, approved step.

## Why links break in Tana

Tana never deletes data that something else still points to. Instead, the pointer is left behind with a trash icon. See `tana-concepts.md`. The usual causes:

1. **A container that owned definitions got deleted.** Many people "organize" by putting tag, field or command definitions under dashboard nodes. Tags made ad hoc can also end up owned by a daily note or a meeting. Deleting such a group or note trashes every definition it owns. Instances keep the tag name with a trash icon, templates lose fields, and buttons and post-process commands stop working.
2. **A template was deleted or installed twice.** Tags from the deleted copy go to the trash, and the second install leaves same-name duplicates. Organized lists can end up pointing at the trashed copy.
3. **People or records were deleted while meetings, fields or AI chats still referenced them.** Calendar sync and meeting agents create many of these.
4. **Pasted links with a wrong or truncated node ID.** They show as "unknown (or no access)", described as "Reference to a node unable to load".
5. **The trash was emptied while references still existed.** These can't be repaired. The link has to be rebuilt by hand, or removed.

## Audit (read-only)

1. **Back up first.** Ask the person to export the workspace as JSON before any repair (Home → … → Export workspace as JSON).
2. **Inventory the trash.**
   - Call `get_children` on `<workspaceId>_TRASH` with limit 1000.
   - The result is large, so save it to the scratchpad and run `python3 -I scripts/trash_audit.py trash.json`.
   - The script lists the high-risk items first: trashed supertags (`tagDef`), fields (`attrDef`), commands and searches. It then prints ready-made `search_nodes` queries in batches of 20 IDs (`linksTo` max is 20).
   - The `created` date is when the node was made, not when it was deleted. There is no deletion date.
3. **Find live nodes that point at trashed ones.**
   - Send each query from the script (replace `<WORKSPACE>`).
   - For every hit, find the exact target: re-query that hit's batch one ID at a time, or in small groups. Add `{"not": {"is": "chat"}}` to drop AI chats, which reference everything and are low-value.
   - Check high-risk items one by one. A trashed command linked from many meetings is a broken post-process command; a trashed tag linked from instances means those instances show a trash icon.
4. **Check the person's organizing hubs.**
   - Call `get_children` on every group node of their schema dashboard (organized supertags, fields, commands, searches).
   - Each child carries `inTrash`, which also applies to the original behind a reference. Flag:
     - `inTrash: true`: the reference points at a trashed definition.
     - name "unknown (or no access)": a dead link.
     - empty nodes: clutter.
5. **Find duplicates that hide the live copy.**
   - Run `search_nodes` with `{"and":[{"hasType":"SYS_T01"},{"textContains":"<name>"}]}`. `SYS_T01` is the supertag type and `SYS_T02` is the field-definition type.
   - Compare breadcrumbs to see which copy belongs to the installed template. Then count real use for each copy with `hasType` (tags) or `field` + `state: "set"` (fields).
6. **Read what the broken thing was.**
   - Call `read_node` on the trashed node with depth 2 or 3. A command shows its system command and parameters, which usually reveals its job. Example: Text processing agent plus Attendees and Action items targets means it is the `#meetings` post-process command.
   - Tag configuration (commands, triggers, post-process settings) is not visible through the MCP. Ask the person to check it in the UI.
7. **Write the findings** to a file. For each finding, record: what is broken, its ID, who points at it (with IDs), the likely cause, the proposed fix and the risk. Group the findings as in the report below.

### Audit traps

- `childOf: <TRASH>, recursive: true` also returns **live** nodes that are only referenced from inside trashed subtrees, even with `includeRefs: false`. Never treat a hit as trashed; trust the `inTrash` flag in the result.
- `read_node` does not show `inTrash`. Use `get_children` on the parent, or `search_nodes`, which both return it.
- `read_node` on the trash or on a busy dashboard at depth 3 or more can exceed the output limit or time out. Use `get_children` with a limit and save big results to the scratchpad.
- Reference rows in the trash (`[[^id]]`), `_async_container` nodes and `tuple` nodes are plumbing. Don't search for links to them.
- Tana creates "References to X" search nodes (under Searches) when someone tries to delete a referenced node. They are leftovers to review, not damage.
- **Check field sources too.** Run `get_tag_schema` on the core tags.
  - `Instance of # (id:…)` with an empty name means the field's source supertag no longer exists. `read_node` on that ID returns nothing. The field's dropdown is then empty, and the fix is a UI step: field config → Supertag.
  - An option list containing "unknown (or no access)" holds a dead value.
- **Pasted links with a cut-short ID.** Compare the dead ID with live IDs: a dead `VLTrGFPS8t` turned out to be field `VLTrP3GFPS8t` with two characters lost.

## Repairs (each one needs the person's OK)

Show the list first, grouped by risk, and wait for approval. After approval, do one group at a time, verify it, and log every change (node ID, before, after) so it can be undone.

| Problem | Repair through the MCP | Notes |
|---|---|---|
| Trashed definition or command still in use | `move_node` the trashed original out of the trash to a safe owner: Schema for tags and fields, the person's commands node for commands | The ID stays the same, so every reference heals at once. Prefer this over rebuilding. Then ask the person to check the tag config in the UI. |
| Organized list points at a trashed duplicate | Import a reference to the live copy next to it. The person then deletes the stale reference in the UI (right-click → Delete reference). | **Never call `trash_node` or `edit_node` on a reference row.** `get_children` and `read_node` report a reference by the original's ID, so the call would act on the original. |
| Dead link "unknown (or no access)" | Ask what it should point to and import the right reference. The person deletes the dead row in the UI. | The reported ID is the broken target, not a real node |
| Trashed record (person, company) still referenced | Restore it with `move_node` to its old area (Library for people), or leave it and tell the person which nodes show a trash icon | Merged-away leftovers ("kept around in case links exist") need nothing |
| Duplicate tags or fields | Recommend **Merge node** in the UI (select both definitions, then run the command) | No MCP tool exists for merging. Merge fields before tags, and only when their fields match. |
| Definitions owned by a dashboard group | Propose moving the definitions to the Schema (`move_node`) and keeping references in the dashboard | This stops the next cleanup from breaking things. Move a few first and verify that nothing changed. |
| Leftover "References to X" searches, empty rows | `trash_node` after the person agrees, but only after `search_nodes` shows the breadcrumb ends at that parent, which proves the parent owns the node | Low risk. If the node is a reference, ask the person to delete it in the UI. |

**Never:**
- empty the trash, or ask the person to, before the repairs are verified;
- use "Hard delete including references" while repairing;
- trash a node that owns definitions;
- edit a template's internal nodes;
- claim that a UI-only setting is fixed.

## Verify

- Re-run the `linksTo` query for each repaired ID. Hits should still exist (the references), and the target should now have `inTrash: false` (check with `get_children` on its new parent).
- Call `get_children` on each hub group again: no `inTrash: true`, and no "unknown (or no access)" rows.
- Ask the person to open one repaired item in the UI and confirm the trash icon is gone.

## Report

Group the report as follows:
- 🔴 broken and in use (commands, tags, fields);
- 🟠 broken but cosmetic (dead links in lists, references to trashed records);
- 🟡 duplicates and clutter;
- 🟢 safe to empty later.

For each item, give the fix and whether it was done. End with when it will be safe to empty the trash: only after every 🔴 and 🟠 item is restored or deliberately let go.
