# Tana Outliner MCP: notes and pitfalls

## Tools that matter for building systems

| Tool | Use | Notes |
|---|---|---|
| `list_workspaces`, `list_tags` | Preflight | `list_tags` shows colours, so reuse the palette |
| `get_tag_schema` | Read fields, option IDs, AI instructions | Run after every batch of field changes; IDs are needed for Tana Paste |
| `create_tag` | New supertag | name, color (hex OK), description, showCheckbox, aiInstructions, voiceGreeting, voiceInstructions |
| `add_field_to_tag` | New field | Types: plain, number, date, url, email, checkbox, user, instance (needs sourceTagId), options (needs options[]). isMultiValue, description and aiInstructions are optional |
| `set_tag_metadata` | Edit tag | Including voice text and AI instructions; null clears |
| `set_field_metadata` | Edit field | Name, description, AI instructions |
| `set_tag_checkbox` | Done checkbox | Can map done to an options field value |
| `import_tana_paste` | Create content | Create-only; bounded size; returns created node IDs |
| `edit_node` | Rename or describe a node | Search-and-replace semantics; HTML formatting, not markdown |
| `set_field_content`, `set_field_option` | Fill fields on existing nodes | Use for test nodes |
| `search_nodes` | Verify searches would match | Structured JSON query, not Tana Paste |
| `trash_node` | Soft delete | Clean up test nodes |

There is no tool for command nodes, tag command menus or event triggers. These are UI steps for the person.

## Pitfalls seen in practice

- **Field order = creation order.** Add fields to one tag sequentially. Parallel calls on the same tag scramble the order.
- **Tana Paste cannot update.** To change a node made by paste, use `edit_node` or the field tools, or trash and re-import. Plan content so it is right the first time: draft, review, then paste.
- **Searches over new tags are empty.** That's expected. Prove them with a test node, then trash the test node.
- **`read_node` depth 4+ can time out.** Use depth 3 or less and read sub-trees separately.
- **Write approval.** "No approval received" means the person never allowed the tool. Ask; don't loop.
- **Two Tana connectors may exist.** The Outliner MCP (app.tana.inc) writes directly. The meetings-focused Tana MCP (home.tana.inc) turns writes into proposals the person approves. Build systems with the Outliner one.
- **AI fields and Ask AI commands need Tana AI** (a paid plan with credits). Confirm this before building them.
- **Instance fields:** create the target tag first. Values must be real instance nodes, never the tag definition.
- **Names and descriptions are one line.** Line breaks go into child nodes via Tana Paste.

## Tana Paste syntax cheat-sheet

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
    - Plain child line
- [ ] A todo
```

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

Searches cannot nest. A search inside a card that should show "everything linked to this card" uses LINKS TO the card's own node ID, or the instance field equal to the card's ID. The card has to exist first, so import cards, read back their IDs, then import each card's searches under it.

## Useful system commands (for the click list)

- "Run AI fields" (`SYS_M016`): wrap it in a command node on each working tag.
- "Insert relative date" (`SYS_M026`): sets today's date in "On added" triggers.
