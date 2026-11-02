#!/usr/bin/env python3
"""Render content/posts/*.md into blog/<slug>/index.html and rebuild the card list.

    python3 scripts/build.py          # build the site
    python3 scripts/build.py --check  # self-check only

Frontmatter fields: title, date, tags, summary, draft (optional).
"""
from __future__ import annotations

import html
import re
import sys
from pathlib import Path
from string import Template

import markdown
import yaml

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "content" / "posts"
BLOG = ROOT / "blog"
INDEX = BLOG / "index.html"
START, END = "<!-- POSTS:START -->", "<!-- POSTS:END -->"

TAG_CLASS = {
    "security": "tag-security", "linux": "tag-linux", "android": "tag-android",
    "aosp": "tag-android", "ctf": "tag-ctf", "writeup": "tag-writeup",
    "tools": "tag-tools", "misc": "tag-misc",
}

PAGE = Template("""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>${title} &mdash; ITACHI</title>
  <meta name="description" content="${summary}" />
  <meta name="theme-color" content="#1e1e2e" />
  <meta property="og:type" content="article" />
  <meta property="og:title" content="${title}" />
  <meta property="og:description" content="${summary}" />
  <link rel="stylesheet" href="../../assets/css/style.css" />
  <link rel="stylesheet" href="../../assets/css/blog.css" />
  <link rel="stylesheet" href="https://unpkg.com/@catppuccin/highlightjs@1.0.1/css/catppuccin-mocha.css" />
</head>
<body>

<nav>
  <div class="wrapper">
    <a class="nav-logo" href="../../">itachi<span>~$$</span></a>
    <ul class="nav-links">
      <li><a href="../../">home</a></li>
      <li><a href="../../blog/" class="active">blog</a></li>
      <li><a href="https://github.com/praveenxsharma" target="_blank" rel="noopener">github &#8599;</a></li>
    </ul>
  </div>
</nav>

<div class="blog-layout">
  <article>

    <header>
      <h1>${title}</h1>

      <div class="post-meta">
        <span class="meta-item">
          <svg class="meta-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <rect x="3" y="4" width="18" height="18" rx="2"/>
            <line x1="16" y1="2" x2="16" y2="6"/>
            <line x1="8" y1="2" x2="8" y2="6"/>
            <line x1="3" y1="10" x2="21" y2="10"/>
          </svg>
          ${date}
        </span>
        <span class="meta-sep">&middot;</span>
        <span class="meta-item">
          <svg class="meta-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M12 20h9"/>
            <path d="M16.5 3.5a2.121 2.121 0 0 1 3 3L7 19l-4 1 1-4L16.5 3.5z"/>
          </svg>
          ${words} words
        </span>
        <span class="meta-sep">&middot;</span>
        <span class="meta-item">
          <svg class="meta-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <circle cx="12" cy="12" r="10"/>
            <polyline points="12 6 12 12 16 14"/>
          </svg>
          ${read} min read
        </span>
      </div>

      <div class="post-tags">
${tags}
      </div>
    </header>

${body}

    <hr>

    <p><a href="../../blog/">&larr; back to all posts</a></p>

  </article>

  <aside class="toc" aria-label="Table of Contents"></aside>
</div>

<footer>
  <div class="wrapper">
    <p>crafted with &#x1F5A4; by <a href="https://github.com/praveenxsharma" target="_blank" rel="noopener">@praveenxsharma</a> &nbsp;&middot;&nbsp; catppuccin mocha &nbsp;&middot;&nbsp; ${year}</p>
  </div>
</footer>

<script src="../../assets/js/site.js"></script>
<script src="../../assets/js/toc.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/highlight.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/highlightjs-line-numbers.js@2.8.0/dist/highlightjs-line-numbers.min.js"></script>
<script src="../../assets/js/hljs-init.js"></script>
</body>
</html>
""")

CARD = Template("""    <a href="${slug}/" class="blog-card">
      <div class="blog-card-meta">
        <span class="blog-card-date">${date}</span>
        <span class="tag-pill ${tag_class}">${tag_label}</span>
      </div>
      <div class="blog-card-title">${title}</div>
      <div class="blog-card-desc">${summary}</div>
      <div class="blog-card-footer">~${words} words &middot; ${read} min read</div>
      <div class="blog-card-arrow">read more &rarr;</div>
    </a>""")


def parse(path: Path) -> dict:
    raw = path.read_text(encoding="utf-8")
    if not raw.startswith("---"):
        raise SystemExit(f"{path.name}: missing frontmatter (--- block)")
    _, front, body = raw.split("---", 2)
    meta = yaml.safe_load(front) or {}
    for key in ("title", "date", "summary"):
        if not meta.get(key):
            raise SystemExit(f"{path.name}: frontmatter needs '{key}'")
    meta["slug"] = meta.get("slug") or path.stem
    meta["body"] = body.strip()
    meta["source"] = path
    return meta


def render(meta: dict) -> str:
    text = markdown.markdown(
        meta["body"],
        extensions=["fenced_code", "tables", "attr_list", "toc", "sane_lists"],
    )
    # hljs-init.js reads data-filename off <pre>; markdown puts it on <code>.
    text = re.sub(
        r'<pre><code class="language-([^"]+)" data-filename="([^"]+)">',
        r'<pre data-filename="\2"><code class="language-\1">',
        text,
    )
    return text


def words_of(meta: dict) -> int:
    plain = re.sub(r"```.*?```", "", meta["body"], flags=re.S)
    return len(re.findall(r"\w+", plain))


def post(meta: dict, year: int) -> str:
    words = words_of(meta)
    tags = meta.get("tags") or ["misc"]
    return PAGE.substitute(
        title=html.escape(meta["title"]),
        summary=html.escape(meta["summary"]),
        date=meta["date"].strftime("%d/%m/%y"),
        words=f"{words:,}",
        read=max(1, round(words / 200)),
        tags="\n".join(
            f'        <span class="tag-pill {TAG_CLASS.get(t, "tag-misc")}">{html.escape(t)}</span>'
            for t in tags
        ),
        body=render(meta),
        year=year,
    )


def card(meta: dict) -> str:
    words = words_of(meta)
    tags = meta.get("tags") or ["misc"]
    first = tags[0]
    return CARD.substitute(
        slug=meta["slug"],
        date=meta["date"].isoformat(),
        tag_class=TAG_CLASS.get(first, "tag-misc"),
        tag_label=html.escape(first),
        title=html.escape(meta["title"]),
        summary=html.escape(meta["summary"]),
        words=f"{words:,}",
        read=max(1, round(words / 200)),
    )


def build() -> int:
    posts = [parse(p) for p in sorted(SRC.glob("*.md"))]
    posts = [p for p in posts if not p.get("draft")]
    posts.sort(key=lambda p: p["date"], reverse=True)
    year = max(p["date"].year for p in posts) if posts else 0

    for meta in posts:
        out = BLOG / meta["slug"] / "index.html"
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(post(meta, year), encoding="utf-8")
        print(f"  blog/{meta['slug']}/index.html")

    index = INDEX.read_text(encoding="utf-8")
    if START not in index or END not in index:
        raise SystemExit(f"blog/index.html: missing {START} / {END} markers")
    head, rest = index.split(START, 1)
    _, tail = rest.split(END, 1)
    cards = "\n\n".join(card(p) for p in posts)
    INDEX.write_text(f"{head}{START}\n\n{cards}\n\n    {END}{tail}", encoding="utf-8")
    print(f"  blog/index.html ({len(posts)} cards)")
    return 0


def check() -> int:
    meta = {
        "title": "T & <x>", "date": __import__("datetime").date(2026, 1, 2),
        "summary": "s", "tags": ["android"], "slug": "s", "body": "# Head\n\n```python\nprint(1)\n```",
    }
    out = post(meta, 2026)
    assert "T &amp; &lt;x&gt;" in out, "title not escaped"
    assert 'id="head"' in out, "toc ids missing"
    assert 'class="language-python"' in out, "fenced code broken"
    assert "tag-android" in out, "tag class broken"
    assert 'href="../../blog/"' in out, "asset/back-link paths broken"
    assert "02/01/26" in out, "date format broken"
    assert card(meta).count('href="s/"') == 1, "card slug broken"
    print("self-check ok")
    return 0


if __name__ == "__main__":
    sys.exit(check() if "--check" in sys.argv else build())
