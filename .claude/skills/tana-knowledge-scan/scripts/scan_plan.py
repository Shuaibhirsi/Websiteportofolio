"""Plan and filter a Tana loose-notes scan.

Usage:
  python3 -I scan_plan.py plan loose.json [--batch 20] [--ws WORKSPACE]
  python3 -I scan_plan.py filter results.json TERM[,TERM...]

plan:   loose.json is a list of nodes (search_nodes rows, get_children children,
        or a {"children": [...]} object). Optional extra keys per node: "text"
        (the note's outline from read_node). Prints noise to skip, links to tag,
        the notes to match with their key terms, then ready-to-send search_nodes
        queries: linksTo batches (is anything already pointing at the note?) and
        one match query per note (which tagged nodes mention its terms?).
filter: results.json is a search_nodes result for the TERMs. Keeps whole-word matches
        only (textContains also matches inside words), drops transcript lines and
        unfilled title expressions, and prints clean names for the match table.
"""
import json
import re
import sys
from collections import Counter, defaultdict
from urllib.parse import urlparse

# Old dashboard copies that day pages pick up, and integration containers in the Library.
NOISE_NAMES = {
    "dashboard", "📊 dashboard", "📊 day dashboard", "📊 day dashboard — live",
    "task dashboard", "mind dump", "brainstorming task", "check boxes", "ai chat",
    "ai chats", "readwise", "google calendar events", "google calendar contacts",
}
TRANSCRIPT_CRUMBS = ("raw transcript", "transcript", "raw")
STOPWORDS = set("""
a an and are as at be but by for from has have i in is it its my of on or so that the this to
was we what when with you your about into just not our out than then them they will would
og i at er en et den det der de du jeg med til på for af som har var vil kan skal ikke men
om fra så hvad hvor hvordan når noget nogle mine min mit vores jeres være blev bliver også
noter note notes møde meeting sep oct nov dec jan feb mar apr may jun jul aug today idag
""".split())
WORD = re.compile(r"[\w][\w.&'-]*", re.UNICODE)
TAG_HTML = re.compile(r"<[^>]+>")


def rows(path):
    data = json.load(open(path))
    return data["children"] if isinstance(data, dict) and "children" in data else data


def clean(name):
    """Drop HTML and Tana title-expression tails such as ' ||| 💼|${Project Status}'."""
    name = TAG_HTML.sub("", name or "")
    for sep in ("|||", " | ", "${"):
        if sep in name:
            name = name.split(sep)[0]
    return name.strip()


def kind(node):
    name = clean(node.get("name", ""))
    crumbs = [c.lower() for c in node.get("breadcrumb", [])]
    if node.get("docType") in ("tuple", "search", "chat", "command"):
        return "noise", "system node"
    if any(c in TRANSCRIPT_CRUMBS for c in crumbs):
        return "noise", "transcript line"
    if not name and not node.get("description") and not node.get("childCount"):
        return "noise", "empty row"
    if name.lower() in NOISE_NAMES:
        return "noise", "old template copy"
    if node.get("docType") == "url" or name.startswith(("http://", "https://")):
        return "link", urlparse(name).netloc.removeprefix("www.") or "url"
    return "note", ""


def terms(node, limit=5):
    """Distinctive words: capitalised words and long words, minus stopwords."""
    text = " ".join([clean(node.get("name", "")), node.get("description") or "", node.get("text") or ""])
    seen, picked = set(), []
    for w in WORD.findall(text):
        w = w.strip(".'-")
        key = w.lower()
        if len(w) < 3 or key in STOPWORDS or key in seen or w.isdigit():
            continue
        if w[0].isupper() or len(w) >= 7:
            seen.add(key)
            picked.append(w)
    return picked[:limit]


def plan(path, size, ws):
    nodes = rows(path)
    groups = defaultdict(list)
    for n in nodes:
        k, why = kind(n)
        groups[k].append((n, why))

    noise = Counter(why for _, why in groups["noise"])
    print(f"# {len(nodes)} candidates: {len(groups['note'])} notes, {len(groups['link'])} links, "
          f"{len(groups['noise'])} noise {dict(noise)}")

    if groups["link"]:
        print("\n# Links to tag (by domain)")
        for domain, count in Counter(why for _, why in groups["link"]).most_common():
            print(f"- {domain}: {count}")

    print("\n# Notes to match")
    all_terms = []
    for n, _ in groups["note"]:
        t = terms(n)
        all_terms += t
        where = " > ".join(n.get("breadcrumb", [])[-2:])
        print(f"- {n['id']} {clean(n.get('name', ''))[:60]!r} [{where}] terms: {', '.join(t) or '-'}")

    ids = [n["id"] for n, _ in groups["note"] + groups["link"]]
    trash = {"not": {"childOf": {"nodeIds": [f"{ws}_TRASH"], "recursive": True}}}
    print(f"\n# linksTo batches ({(len(ids) + size - 1) // size}): a hit means the note is already linked")
    for i in range(0, len(ids), size):
        print(json.dumps({"and": [{"linksTo": ids[i:i + size]}, trash]}, ensure_ascii=False))

    print("\n# Match queries, one per note: tagged nodes that mention any of its terms."
          "\n# Prune generic terms first; then run `filter` on each result with the same terms.")
    for n, _ in groups["note"]:
        t = [w.lower() for w in terms(n)]
        if t:
            query = {"and": [{"or": [{"textContains": w} for w in t]}, {"has": "tag"}, trash]}
            print(f"{n['id']}\t{','.join(t)}\t{json.dumps(query, ensure_ascii=False)}")


def filter_results(path, term):
    alts = "|".join(re.escape(t.strip()) for t in term.split(",") if t.strip())
    word = re.compile(rf"(?<!\w)(?:{alts})(?!\w)", re.IGNORECASE | re.UNICODE)
    kept = 0
    for n in rows(path):
        name = clean(n.get("name", ""))
        crumbs = [c.lower() for c in n.get("breadcrumb", [])]
        if any(c in TRANSCRIPT_CRUMBS for c in crumbs) or not name:
            continue
        if not (word.search(name) or word.search(n.get("description") or "")):
            continue
        tags = ", ".join("#" + t["name"] for t in n.get("tags", []) if t.get("name"))
        print(f"- {n['id']} {name[:60]!r} {tags} [{' > '.join(n.get('breadcrumb', [])[-2:])}]")
        kept += 1
    print(f"# {kept} whole-word matches for {term!r}")


def main():
    if len(sys.argv) < 3 or sys.argv[1] not in ("plan", "filter"):
        sys.exit(__doc__)
    if sys.argv[1] == "plan":
        size = int(sys.argv[sys.argv.index("--batch") + 1]) if "--batch" in sys.argv else 20
        ws = sys.argv[sys.argv.index("--ws") + 1] if "--ws" in sys.argv else "<WORKSPACE>"
        plan(sys.argv[2], size, ws)
    else:
        filter_results(sys.argv[2], sys.argv[3])


if __name__ == "__main__":
    main()
