# How Tana Outliner works: facts that matter when building, fixing and organizing

Source for everything below: Tana Outliner's official docs at `outliner.tana.inc`, read directly on 25 Oct 2026 (🟢). Each section names the page. In March 2026 Tana launched a separate new product and renamed the original app "Tana Outliner". This skill and the Outliner MCP are about Tana Outliner.

## Nodes, owners and references (`/learn/features/nodes-and-references`)

- Everything is a node: fields, views, commands, settings, workspaces, the day page. Every node has a unique ID.
- **Every node has exactly one owner**, its single source of truth. A reference is a mirror of the original: editing it edits the original, but deleting it does not delete the original.
- **When an original is trashed, its references are not trashed.** They stay in place with a trash-can icon, and clicking the icon brings the original back out of the trash.
- "Bring referenced node here" swaps ownership onto a reference, which then becomes the original.
- "Hard delete including references" deletes a node and its references in the current workspace. Inline references, and references in other workspaces, stay behind with a trash icon.
- "Merge node" works on nodes, supertags and fields. It combines children and tags, puts the merged-away node in the trash, and re-points every reference to the survivor. A trashed node that reads "(merged into X) – kept around in case links exist" is this leftover, and it is harmless.
- A node cannot appear twice as a child of the same parent.

## Trash (`/help/getting-started`, `/help/writing-and-editing`, `/help/organizing-workspace`)

- Each workspace has its own trash, opened with the "Open trash (deleted)" command.
- Deleting a node moves it, and everything it owns, to the trash.
- "Empty trash for workspace" deletes permanently, and may need running more than once. After that, references to emptied nodes can no longer be restored.
- Tana's own warning: clearing trashed nodes that have references "can be fiddly, since it's not always obvious what gets removed alongside them."
- "Unknown (or no access)" (now an "unavailable node", shown with a prohibited bullet) is a reference whose source can no longer load.

## Supertags (`/learn/features/supertags`, `/learn/guides/when-to-use-extend-in-supertags`)

- A supertag says what a node **is** ("Oslo is a City"). Think "is a" when choosing tags.
- New supertag definitions go to the Schema by default.
- Before deleting a tag, check "Used X times" in its config. Then untag, or merge into the replacement tag. Deleting a tag still in use leaves trash icons on its instances.
- **Extend** makes a tag build on a base tag, like inheritance in programming. Fields inherited from the base can't be moved or deleted in the extension. Searching the base tag also returns the extensions.
- Base types (meeting, task, organization, person, location, project, topic, event, article, memo, reflection, day, week) help Tana's AI. Setting a tag's base type to meeting unlocks the meeting agent and audio-enabled post-processing.
- **AI and Commands** on a tag:
  - autofill
  - audio-enabled tag, with an optional post-process command
  - command palette buttons
  - event triggers: On capture, On added, On removed, On checked, On unchecked
  - AI instructions and voice chat set-up
- **Triggers do not fire when a tag is added through the API or MCP.**
- Other tag options: "Build title from fields" (`${field}`, `${sys:owner}` and so on), default child supertag, related content, pinned fields, optional fields, and a done-state mapping for the checkbox.

## Fields (`/learn/features/fields`, `/help/troubleshooting`)

- A field says what a node **has** ("a task has a Due date").
- Field types (9): Plain, Options, Options from supertag (formerly "Instance"), Date, Number, Tana Outliner user, URL, Email, Checkbox.
- **The field definition lives where the field was first created.**
  - Delete that definition, or its owner, and every use of the field shows a trash icon.
  - Tana recommends "Make it discoverable", which moves the definition to the Schema.
  - Field definitions owned by the Schema get priority when searching for fields.
- "Used in" shows how many nodes and supertags use a field. Check it before deleting or merging.
- Auto-initialize runs only when a supertag is applied and the field is still a placeholder.
  - It is not live-updating.
  - It does nothing for fields nested under another node in the template.
  - Moving a node does not re-run it.
- To bulk-delete a field's values: put the nodes in a table, show the field as a column, then choose "Delete column and values".
- "Set [field]" only works on Options, Options from supertag, user and checkbox fields.
- Template nodes stay linked to the template until they are edited in an instance. After that, template changes no longer reach them.
- "Fields nested under other nodes" in a template breaks search by field, table columns and title expressions.

## Commands (`/learn/features/command-nodes`, `/learn/tutorials/three-levels-of-tana-commands`)

- A command node is a container of system commands run top to bottom, set up with parameter fields.
  - The same command can't be added twice; to repeat it, wrap it in another command node.
  - "Node filter" (a search query) controls where a command can run. "Node context" (PARENT, GRANDPARENT or a node) controls what it acts on.
- Commands appear in the command line, as buttons on nodes, tags and fields, and on events: tag added or removed, child added or removed.
- Find every command with the search keyword `IS COMMAND`.
- Group commands into menu buttons with "Convert to Group".
- Tana disables its event system if AI-created nodes keep re-triggering the same event within 60 seconds.

## Search nodes (`/learn/features/search-nodes`)

- Results are references. A search runs only while expanded. It returns at most 2500 results.
- Keyword operators:
  - `IS TAG`, `IS FIELD`, `IS COMMAND`, `IS SEARCH NODE`, `IS CALENDAR NODE`, `IS CHAT`, `IS ENTITY`, `IS PUBLISHED`
  - `HAS TAG`, `HAS FIELD`, `HAS MEDIA`, `TODO`, `DONE`, `NOT DONE`, `DONE LAST n DAYS`, `CREATED LAST n DAYS`, `EDITED LAST n DAYS`
  - `IN LIBRARY`, `ON DAY NODE`, `PARENTS DESCENDANTS`, plus the `WITH REFS` variants
- Field operators: `AND`, `OR`, `NOT`, `LT`, `GT`, `LINKS TO`, `CHILD OF`, `OWNED BY`, `DATE OVERLAPS`, `COMPONENTS REC`.
- Field values: `PARENT`/`GRANDPARENT` (with dot notation and date arithmetic such as `PARENT-7`), `FOR RELATIVE DATE`, `Set`, `Not Set`, `Defined`, `Not Defined`.
- **CHILD OF vs OWNED BY:** a node can be the child of many nodes (through references) but is owned by exactly one.

## Workspace layout (`/learn/features/workspaces`, `/help/getting-started`)

- Every workspace has Home, Daily notes, Schema, Library, Settings and Trash.
- The Schema is "a bit of a legacy node"; Tana puts ad-hoc and discoverable definitions there.
- The Library holds nodes with no place: new @-mentions and imports.
- Tana's advice for note-taking:
  - Use the daily notes as a scratchpad for capture.
  - Use Home for the wiki and dashboards.
  - Apply supertags to whatever matters, and surface it with search nodes.
- Keep one workspace until you need to collaborate, import, test templates or publish a template.
- Export the workspace as JSON (TIF2) before a large cleanup. It gives you an editable copy you can import into a new workspace.

## Templates (`/learn/features/tana-templates`)

- Test templates in a separate workspace first.
- Deleting a template node together with its building blocks leaves tagged items whose tags and fields show as deleted. You can restore the building blocks or remove them.
- Building blocks moved out from under the template node survive deleting the template.
- Installing the same template twice creates duplicate tags.

## Schema audit, Tana's own method (`/learn/guides/conduct-a-schema-audit`)

1. Inventory with `IS TAG` and `IS FIELD`, scoped to the workspace.
2. Spot redundancy, for example both `#task` and `#todo`.
3. Group similar items into core categories, which become proto-tags to extend from.
4. Merge duplicate fields first, then tags, and only when their field structures match.
5. Document the result on a schema page.
6. Keep a "stray tag" search for new, uncategorized tags, and review regularly.

## Second-brain frameworks (`/help/knowledge-graph-concepts`, `/learn/tutorials/gtd-in-tana`)

- Tana supports PARA, GTD and Zettelkasten, and mixes of them.
- Start small: a daily note plus one or two tags. Add structure only when you need it.
- GTD pieces map onto supertags and searches: projects, Someday/Maybe, Waiting For, tickler, reference. You don't store things in one place; tags plus searches bring them together.

## MCP (`/learn/features/local-api-mcp`)

- Two servers:
  - Local: `http://localhost:8262/mcp`, needs the desktop app open.
  - Hosted (beta, paid plan): `https://app.tana.inc/mcp`, uses OAuth.
- Documented tools:
  - `list_workspaces`, `search_nodes`, `read_node`, `get_children`, `list_tags`, `get_tag_schema`
  - `import_tana_paste`, `tag`, `set_field_option`, `set_field_content`
  - `create_tag`, `add_field_to_tag`, `set_tag_checkbox`, `check_node`/`uncheck_node`
  - `trash_node`, `get_or_create_calendar_node`, `edit_node`
- The connector in practice also has `move_node`, `set_tag_metadata`, `set_field_metadata` and the attachment tools.
- A workspace must be loaded in the app to be reachable.
