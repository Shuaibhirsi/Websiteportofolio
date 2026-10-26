# Visual design: placement, views, icons

How a page looks decides whether the person opens it again. This file covers where things go (placement), how each list is shown (views) and how types are recognised at a glance (icons). It draws on Tana's official docs and on what community creators do. Read it with `second-brain-design.md` before designing any day page, dashboard or entity page.

## What creators do (research, 26 Oct 2026)

| Source | Tier | Pattern worth copying |
|---|---|---|
| Tana docs: Views, Related content, Nodes & references, Daily notes (outliner.tana.inc, read directly) | 🟢 | View types and options; related content beside or below a node, set once on a supertag; icons and banners per node or as a supertag default; a "#task NOT DONE" search moved to the day's related content |
| Tana daily-notes showcase (tana.inc, blocked here; search summary only) | 🟠 | Day pages serve six jobs: overview, tasks/habits, input/do work, self-reflect, serendipity, aesthetics. Simplest real setup: two searches (recent tasks, recent quick notes). A random verse or quote from your own collection at the top. A "timeline" search of things edited in the last 7 days |
| Tana home-node showcase (blocked; summary only) | 🟠 | Dashboards belong on the Home node, which "reduces the burden of your daily notes template". Notes fall into capturing, doing, reflecting and building |
| Ev Chapman (evchapman.com, blocked; summaries only) | 🟠 | "No Inbox": capture straight onto the day page and sort with tags. Related-content sections such as Today's tasks, Task inbox, Capture inbox, Daily agenda, Current projects, Today's accomplishments, Open loops and Horizon. A "Focus mode" toggle filters those sections (work/personal, weekday/weekend). A 5-minute daily plan that keeps the day realistic |
| Kam Simpson (Substack, blocked; summary only) | 🟠 | Review the weekly and monthly plan on the day page; resurface 2 random highlights a day |
| Fis Fraga, Holistic Home Node (Substack, blocked; summary only) | 🟠 | A Home node with hubs (Vision, Plans, Notes, Areas, Routines, Projects, Tasks), each reachable from several others; a Vision → Plan → Execute → Review cycle |
| Tana "simple task management" guide (summary only) | 🟠 | Keep the Doing list to 2–3 tasks; pin "All tasks" to the sidebar |
| Bri Ballard (Medium, blocked; summary only) | 🟠 | Hide empty fields so one tag stays tidy for two uses |
| Sharmarke Hujale (hujale.dk, summary only) | 🟠 | Start with one small capture-to-content system and grow it; reorganise later with PARA |
| Monica Rysavy (Substack, summary only) | 🟠 | Extend `#day` with tracking fields (log, meals, exercise, meeting notes) |

🟠 rows come from search-result summaries because the hosts were blocked in this environment. Treat them as leads. To read them, the person can allow tana.inc, evchapman.com, substack.com and medium.com under the environment's Network access.

## Placement: three zones and a home

1. **Main column: write and plan.** Template prompts in the order of the day (morning plan, then free capture, then evening close), plus whatever the person writes. Keep it short, so the page is a workbench and not a dashboard.
2. **Right side (Related content): awareness.** Up to about four live searches that matter today, such as tasks due, today's meetings and open loops. Related content set on the `#day` tag renders on every day dynamically. That includes days created before a template change, or created empty by calendar sync and navigation. So anything that must be on every day belongs here, not in the template.
3. **Bottom (Related content, "Prefer area: bottom"): review.** Done today, the week ahead, a quote or highlight. These are glanceable and don't compete with writing.
4. **Home node: dashboards.** Deep views, such as all projects, all patterns and the schema hub, go on Home or on pinned nodes, never on the day.

Rules of thumb:
- **Top to bottom follows time.** ☀️ plan comes before ✍️ capture, which comes before 🌙 close.
- **At most 3–5 boxes on a day.** More becomes noise; move it to Home or behind tabs.
- **Every list needs a stop condition** (NOT DONE, a date window, a status filter, or a result limit), so it stays short on day 100.
- **Day templates don't always apply.** Days opened before a template change keep their old content. Days created in the background seem to get the template only when first opened (observed, not documented). Use related content for must-see lists and the template for prompts.

## Views: pick by the job

| Job | View | Notes |
|---|---|---|
| Write, quick lists | Outline (default) | No marker needed |
| Compare a few fields | Table | 2–4 columns via Display; number columns can sum, average or count |
| Move work through stages | Cards + Group by status | A board: drag a card to change its status. Cards show banners as images |
| Anything with a date | Calendar | Plots date fields; week granularity suits a day page |
| Switch between sections | Tabs (top) / Side menu (left) | On a **child** node only: tabs can't be set on the `#day` template itself. Each tab keeps its own view |
| Browse items with a preview | List (navigation) | Two panels: list left, content right |
| Narrow side panels | Outline + Display | Field values show as grey text under each title, which beats a squeezed table |

Options to always set:
- **Display:** the 1–2 fields that matter.
- **Sort:** by date or status.
- **Group:** by status or by project.
- **Page size or result limit:** e.g. 7 for side boxes.

Content width: Auto gives Full width for table, cards, calendar and tabs, and Medium for outline.

## Icons: one symbol per type

- **One emoji per type, everywhere.** Use it as the supertag's default icon (it replaces the bullet on every node of that tag), as the first character of section titles, and in the hub's groups. Example legend:
  - ☀️ morning
  - 🌙 evening
  - 🎯 focus and tasks
  - 🤝 meetings
  - 🔁 patterns
  - 🧪 experiments
  - ✅ done
  - 📥 inbox
  - 📅 calendar
  - 💬 quote
- **Status by colour emoji** (🔴🟡🟢) and **progress by blocks** (▱▰) in options, so tables and cards read at a glance.
- **Banners** for aesthetics: a default banner on `#day`, or Unsplash day banners (experimental, needs the person's API key). Banners on entity tags (project, book) become card images.
- Use emoji to open titles only; keep body text plain. Icons are anchors, not decoration.

## What the MCP can and can't set (verified 26 Oct 2026)

- **Can:**
  - Views, via Tana Paste markers on a node or search: `%%view:tabs%%`, `%%view:table%%`, `%%view:cards%%`, `%%view:sidemenu%%`, `%%view:calendar%%`. `list` and `outline` are **not** recognised and stay in the name as text; leave Outline unmarked.
  - Headings with `!!`.
  - Emoji in names.
  - Searches anywhere, including in templates.
- **Can't (click list):**
  - Group by, Sort, Display and page size;
  - the List (navigation) view;
  - node and supertag icons, and banners;
  - related content and its placement;
  - focus modes and command menus.

## Design check for visual work

- [ ] Each zone has one job: main = write, side = aware, bottom = review, Home = dashboards.
- [ ] Every must-see list is in related content, so it shows on every day.
- [ ] Every list has a stop condition and a fitting view.
- [ ] Each type has one emoji, used for its tag icon, section titles and hub group.
- [ ] Show a preview (text mock-up) before building, and a click list for what the MCP can't set.
