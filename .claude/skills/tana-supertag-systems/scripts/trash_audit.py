"""Turn a saved get_children(<workspace>_TRASH) result into a trash inventory
and ready-to-send search_nodes queries that find live nodes linking to trashed ones.

Usage: python3 -I trash_audit.py trash.json [--batch 20]
trash.json: the raw get_children output ({"children": [...], "total": n}).
Prints an inventory, then one JSON query per line. Send each query to
search_nodes (limit 100, workspaceIds [<workspace>]); any hit is a live node
that still points at something in the trash.
"""
import json
import sys
from collections import Counter

RISKY = {"tagDef": "supertag", "attrDef": "field", "command": "command", "search": "search"}
SKIP_PREFIXES = ("[[^", "**_async_container", "**_new_exploration")


def main():
    path = sys.argv[1]
    size = int(sys.argv[sys.argv.index("--batch") + 1]) if "--batch" in sys.argv else 20
    data = json.load(open(path))
    children = data["children"]
    print(f"# {len(children)} top-level items in trash (total reported: {data.get('total')})")
    print("# by type:", dict(Counter(c["docType"] for c in children)))
    tags = Counter(t.get("name") or "?" for c in children for t in c.get("tags", []))
    print("# by tag:", dict(tags.most_common(15)))

    print("\n# High-risk items (definitions and automations; check these first)")
    for c in children:
        if c["docType"] in RISKY:
            print(f"- {RISKY[c['docType']]}: {c['name'][:70]!r} {c['id']} (created {c['created'][:10]})")

    print("\n# Tagged items (records other nodes may point to)")
    for c in children:
        names = [t.get("name") for t in c.get("tags", []) if t.get("name") not in ("supertag", "field-definition")]
        if names and c["docType"] not in RISKY:
            print(f"- #{', #'.join(n or '?' for n in names)}: {c['name'][:60]!r} {c['id']}")

    candidates = [
        c["id"] for c in children
        if c["docType"] != "tuple" and c["name"].strip() and not c["name"].startswith(SKIP_PREFIXES)
    ]
    print(f"\n# {len(candidates)} candidates -> {(len(candidates) + size - 1) // size} search_nodes queries")
    for i in range(0, len(candidates), size):
        batch = candidates[i:i + size]
        query = {"and": [
            {"linksTo": batch},
            {"not": {"childOf": {"nodeIds": ["<WORKSPACE>_TRASH"], "recursive": True}}},
        ]}
        print(json.dumps(query, ensure_ascii=False))


if __name__ == "__main__":
    main()
