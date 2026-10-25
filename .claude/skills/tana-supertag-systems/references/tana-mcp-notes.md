# Tana Outliner MCP: notes and pitfalls

The connector is Tana Outliner's MCP: hosted at `https://app.tana.inc/mcp` (beta, paid plan) or local at `http://localhost:8262/mcp` (needs the desktop app open). The new Tana product (home.tana.inc) has its own, separate MCP that turns writes into proposals for the person to approve. Build, fix and organize with the Outliner one.

## Tools that matter

| Tool | Use | Notes |
|---|---|---|
| `list_workspaces`, `list_tags` | Preflight | `list_tags` shows colours, so reuse the palette. Pass a limit of up to 500. |
| `get_tag_schema` | Read fields, option IDs, AI and voice set-up | Run after every batch of field changes; IDs are needed for Tana Paste. `includeEditInstructions: false` keeps output small. |
| `get_children` | Paged children with `docType`, `childCount` and **`inTrash`** | The only cheap way to see whether a listed item (including the original behind a reference) is in the trash. Limit up to 1000. |
| `read_node` | Outline as Markdown | No `inTrash` flag. Depth 3 or more on big nodes times out or overflows; read in slices. |
| `search_nodes` | Structured queries | Up to 1000 results on request. `linksTo` takes at most 20 IDs. `hasType: "SYS_T01"` = supertag definitions, `"SYS_T02"` = field definitions; `is` covers field, command, search, chat, entity and more. |
| `create_tag` | New supertag | Name, color (hex OK), description, showCheckbox, aiInstructions, voiceGreeting, voiceInstructions |
| `add_field_to_tag` | New field | Types: plain, number, date, url, email, checkbox, user, instance (needs sourceTagId), options (needs options[]). isMultiValue, description and aiInstructions are optional. |
| `set_tag_metadata`, `set_field_metadata` | Edit a tag or field | Includes voice text and AI instructions; null clears |
| `set_tag_checkbox` | Done checkbox | Can map done to an options field value |
| `import_tana_paste` | Create content | Create-only; keep it small; returns the created node IDs |
| `edit_node` | Rename a node or edit its description | Search-and-replace semantics; HTML formatting, not markdown |
| `set_field_content`, `set_field_option`, `tag`, `check_node` | Fill fields or tag existing nodes | Use for test nodes |
| `move_node` | Move a node; `sourceParentId` picks which parent to move it from | **Restores a trashed node:** moving it out of `<ws>_TRASH` keeps its ID, so every reference heals. With `keepSourceReference: true`, the node moves to a new owner and a reference stays where it was: the safe way to send definitions to the Schema. `position: before/after` with `referenceNodeId` orders your own new nodes. |
| `trash_node` | Soft delete | Only on nodes you have proved are owned where you think (see pitfalls) |

There is no tool for: command nodes, a tag's command menu or event triggers, tag configuration (audio-enabled, post-process command), Merge node, or emptying the trash. These are UI steps for the person.

## Pitfalls seen in practice

- **A reference row reports the original's ID.** Children of a list that holds references come back with the definition's own ID, `docType` and owner. `trash_node`, `edit_node` or `move_node` (without `sourceParentId`) on that ID acts on the original. To drop a reference from a list, ask the person to use Delete reference in the UI.
- **`childOf` the trash, recursive, returns live nodes too:** anything referenced from inside a trashed subtree. That holds even with `includeRefs: false`. Judge trashed-ness only by the `inTrash` field.
- **Field order = creation order.** Add fields to one tag one at a time. Parallel calls on the same tag scramble the order.
- **Reuse fields before creating them.** Search `{"and":[{"is":"field"},{"textContains":"Date"}]}` first. Same-name fields on different tags are separate definitions and split every search and view. (The inner-work build created a second Date, Linked stage and ✨ Reflection; avoid repeating that.)
- **Tana Paste cannot update.** To change a node made by paste, use `edit_node` or the field tools, or trash and re-import. Draft, review, then paste.
- **Searches over new tags are empty.** That's expected. Prove them with a test node, then trash the test node.
- **Write approval.** "No approval received" means the person never allowed the tool. Ask; don't loop.
- **Triggers don't fire through the API.** On added, On removed and child-added commands are skipped when the MCP tags or creates nodes. Run the equivalent steps yourself, or tell the person.
- **AI fields and Ask AI commands need Tana AI** (a paid plan with credits). Confirm before building them.
- **Instance fields:** create the target tag first. Values must be real instance nodes, never the tag definition.
- **Names and descriptions are one line.** Line breaks go into child nodes through Tana Paste.
- **A `#word` in plain text becomes a tag.** Write tag names in text without `#`. Avoid `::` and `[[` in text too.
- **"Create-only" still lets you append.** You can import new children under any existing node. Use this for per-card searches and for filling hub groups with references.
- **Imports under the same parent run in call order.** Import ordered siblings one call at a time. Imports under different parents can run in parallel.
- **Search nodes can't be read back.** `read_node` shows only the title. To verify one:
  1. Confirm it is a real search: `{"is":"search"}` plus `ownedBy` (docType "search").
  2. Run the equivalent structured query against test nodes.
  3. Ask the person to glance at it.
- **Big results:** trash listings, `IS FIELD` and `IS COMMAND` overflow the tool output. Save them to the scratchpad and process them with `python3 -I`.
- **The search index lags after moves.** Right after a `move_node`, `ownedBy` queries can still return the old owner for a few items, while their breadcrumb already shows the new one. Trust the breadcrumb, or re-query a little later.
- **Tag configuration is hidden.** A tag's children are field tuples only. Commands, triggers and post-process settings don't show, so ask the person to check the config panel.
- **Subagents can hit session usage limits mid-workflow.** Keep every Tana write in the main loop.

## Tana Paste cheat-sheet (verified against `/learn/features/tana-paste`)

```
- Parent node %%view:tabs%%
  - Child becomes a tab %%view:cards%%
  - Card #[[^tagId]]
    - [[^fieldId]]:: plain value
    - [[^numberFieldId]]:: 3
    - [[^dateFieldId]]:: [[date:2026-10-11]]
    - [[^optionsFieldId]]:: [[^optionId]]
    - [[^instanceFieldId]]:: [[^nodeId]]
    - [[^checkboxFieldId]]:: [X]
    - [[^urlFieldId]]:: https://example.org
    - !! A heading
    - Plain child line
  - [[^existingNodeId]]
- [ ] A todo
```

- A row that is only `[[^id]]` becomes a reference to that node, and the original keeps its owner (verified 25 Oct 2026). Use it to fill hub groups. The import result lists reference rows under the original's ID, so new nodes are the ones with new IDs.
- `[[name^id]]` falls back to the name if the ID doesn't exist. A bare `[[^id]]` with an unknown ID links to "undefined".
- Dates: `[[date:2021-02-01 20:30]]`, `[[date:2021-W02]]`, `[[date:2021-02]]`, durations `[[date:2021-02/2021-04-05]]`.
- Formatting: `**bold**`, `__italic__`, `^^highlight^^`, links `[name](https://…)`.
- Tana Paste is for small results, not bulk import.

Views: `%%view:list|table|cards|tabs|calendar|sidemenu%%`, placed on the parent whose children are shown (for a search, on the search node).

### Search nodes

```
- %%search%% 🔴 Patterns on autopilot %%view:table%%
  - [[#^patternTagId]]
  - [[^statusFieldId]]:: [[^optionIdRed]]
```

| Operator | Syntax |
|---|---|
| AND (implicit at root) | `[[^SYS_A41]]::` |
| OR | `[[^SYS_A42]]::` with children |
| NOT | `[[^SYS_A43]]::` with children |
| Field is set | `[[^fieldId]]:: [[^SYS_V60]]` |
| Less than / greater than | `[[^SYS_A49]]::` / `[[^SYS_A48]]::` wrapping a field condition |
| Date overlaps | `[[^SYS_203]]::` |
| Links to | `[[^SYS_V49]]:: [[^nodeId]]` |
| Child of | `[[^SYS_V53]]:: [[^nodeId]]` |
| Owned by | `[[^SYS_V55]]:: [[^nodeId]]` |

Searches cannot nest. To make a search inside a card show "everything linked to this card", use LINKS TO with the card's own node ID, or set the instance field equal to the card's ID. The card has to exist first: import the cards, read back their IDs, then import each card's searches under it. Keyword operators such as `IS TAG`, `CREATED LAST 30 DAYS` and `NOT DONE` are written as plain rows.

## Useful system commands (for the click list)

- "Run AI fields" (`SYS_M016`): wrap it in a command node on each working tag.
- "Insert relative date" (`SYS_M026`): sets today's date in "On added" triggers.
- "Text processing agent" (`SYS_M031`): the default meeting post-process command.
- "Ask AI" (`SYS_M001`).
