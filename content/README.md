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

## Images

Obsidian embeds work, but **the image file has to be in the repo too** — pasting the `.md`
alone leaves the embed pointing at nothing:

```
![[Pasted image 20261109123553.png]]
```

Drop the PNG anywhere under `content/` (`content/posts/` or `content/attachments/` — the
build searches both, and copies the file next to the post). The build prints a warning for
any embed whose file it can't find, so a missing image shows up in the Action log instead
of shipping as a broken box.

Give it alt text with a pipe — it becomes the `<img alt>` and feeds SEO:

```
![[Pasted image 20261109123553.png|Benchmark scores across Code, Web and Office]]
```

A numeric pipe value (`|300`) is treated as an Obsidian size hint and ignored.

## Rules

- Never edit `blog/*/index.html` by hand — the next build overwrites it.
- Renaming or deleting a `.md` removes its generated page on the next build.
- Fenced code gets a language tab automatically. For a filename header use
  `~~~{.python data-filename="exploit.py"}`.
