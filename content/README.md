# Writing posts

Paste a `.md` into `content/posts/` and push. GitHub Actions renders it into
`blog/<filename>/index.html` and rebuilds the card list on `blog/index.html`.

To build locally instead:

```bash
pip install -r requirements.txt
python3 scripts/build.py          # writes blog/
python3 scripts/build.py --check  # self-check only
```

## Frontmatter is optional

```markdown
---
title: My Post Title
date: 2026-11-02
tags: [security, linux]
summary: One sentence that shows up on the blog card.
---
```

Anything you leave out is derived: `title` from the filename, `date` from the file's
last commit date, `summary` from the first paragraph. `draft: true` keeps a post out
of the build.

Tags (one decides the card colour): `security` `linux` `android` `aosp` `ctf`
`writeup` `tools` `misc`. Unknown tags render as `misc`.

> Tags must not start with `#` in frontmatter — YAML reads `#` as the start of a
> comment. Use `tags: [security, linux]`, not `tags: security, #linux`.

## Obsidian syntax

Straight from the vault, no cleanup needed:

| Obsidian | Becomes |
|---|---|
| `[[Hello World]]` | a link if `hello-world.md` is a post, plain text if not |
| `[[Note\|label]]` | same, with `label` as the text |
| `![[shot.png]]` | `<img>` — the file is copied next to the post |
| `==text==` | `<mark>text</mark>` |
| `%%comment%%` | removed |
| `> [!note]` | stays a blockquote (callout title is visible) |

## Rules

- Never edit `blog/*/index.html` by hand — the next build overwrites it.
- Renaming or deleting a `.md` removes its generated page on the next build.
- Fenced code gets a language tab automatically. For a filename header use
  `~~~{.python data-filename="exploit.py"}`.
