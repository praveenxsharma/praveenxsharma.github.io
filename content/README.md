# Writing posts

Every `.md` file in `content/posts/` becomes `blog/<filename>/index.html` and a card on
`blog/index.html`.

1. Create `content/posts/my-slug.md`
2. Fill in the frontmatter and write the body
3. Run `python3 scripts/build.py`
4. Commit — the generated HTML is what GitHub Pages serves

```markdown
---
title: My Post Title
date: 2026-11-02
tags: [security, linux]
summary: One sentence that shows up on the blog card.
---

Body goes here. Normal markdown: headings, **bold**, `code`, lists, tables, images.
```

- `title`, `date`, `summary` are required. `date` (`YYYY-MM-DD`) decides the card order, newest first.
- `tags` picks the card colour from: `security` `linux` `android` `aosp` `ctf` `writeup` `tools` `misc`.
  Anything unrecognised renders as `misc`.
- `draft: true` keeps a post out of the build entirely.
- Fenced code gets a language tab automatically. Add a filename header with
  `~~~{.python data-filename="exploit.py"}`.
- Never edit `blog/*/index.html` by hand — the next build overwrites it.
