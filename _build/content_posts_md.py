"""Markdown blog posts (BabyLoveGrowth drafts, after editing).

Drop a file in _build/posts/ named <slug>.md:

    ---
    title: How Long Does a Kitchen Renovation Take in NYC?
    description: One or two sentences for Google and the blog card (under ~160 characters).
    date: 2026-10-22
    hero: glass-house-kitchen          # a photo name from /images (no .jpg); optional
    services: kitchens, plumbing, electrical   # service slugs; first 3 shown as related
    intro: Optional lead paragraph shown above the article.
    draft: true                        # remove or set false to publish
    ---
    ## First heading
    Body in Markdown...

Files with draft: true (or names starting with "_") are skipped by the build.
A leading "# Title" line in the body is dropped (the page already shows the title).
"""
import os, re, datetime

POSTS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "posts")


def _front_matter(text):
    m = re.match(r"^---\s*\n(.*?)\n---\s*\n(.*)$", text, re.S)
    if not m:
        return {}, text
    meta = {}
    for line in m.group(1).splitlines():
        line = line.split(" #", 1)[0].rstrip()
        if ":" in line:
            k, v = line.split(":", 1)
            meta[k.strip().lower()] = v.strip().strip('"').strip("'")
    return meta, m.group(2)


def load_md_posts():
    if not os.path.isdir(POSTS_DIR):
        return []
    try:
        import markdown
    except ImportError:
        raise SystemExit("Markdown posts need the markdown package: pip install markdown")
    out = []
    for fn in sorted(os.listdir(POSTS_DIR)):
        if not fn.endswith(".md") or fn.startswith("_"):
            continue
        meta, body = _front_matter(open(os.path.join(POSTS_DIR, fn), encoding="utf-8").read())
        if meta.get("draft", "").lower() in ("true", "yes", "1"):
            continue
        slug = fn[:-3]
        body = re.sub(r"^\s*#\s+[^\n]*\n", "", body, count=1)  # drop duplicate H1
        html = markdown.markdown(body, extensions=["tables", "sane_lists"])
        html = html.replace("<h1>", "<h2>").replace("</h1>", "</h2>")
        html = html.replace("<table>", '<div class="table-wrap"><table>').replace("</table>", "</table></div>")
        for req in ("title", "description"):
            if not meta.get(req):
                raise SystemExit(f"_build/posts/{fn}: missing '{req}' in front matter")
        date = meta.get("date") or datetime.date.today().isoformat()
        datetime.date.fromisoformat(date)
        out.append(dict(
            slug=slug, title=meta["title"], desc=meta["description"], date=date,
            hero=meta.get("hero") or "vaulted-scaffolding",
            services=[x.strip() for x in meta.get("services", "renovations").split(",") if x.strip()],
            intro=meta.get("intro", ""), body_html=html, sections=[],
        ))
    return out
