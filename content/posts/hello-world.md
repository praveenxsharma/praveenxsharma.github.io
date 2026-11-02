---
title: Hello World
date: 2026-02-26
tags: [misc]
summary: First post. Setting up the blog and figuring out what to write about.
---

first post. not entirely sure what i'm going to write about yet, but that's kind of the point.
this is my space to dump thoughts, writeups, and notes — mostly around security, linux,
and whatever i'm poking at on a given week.

---

# Why

i've been meaning to do this for a while. there's a lot of things i figure out by breaking stuff
or just spending too many hours in a terminal, and most of it lives in my head or scattered across notes.
writing it down forces me to actually understand it properly.

expect writeups, ctf notes, linux things, maybe some aosp stuff. no promises on frequency.

# How This Works

plain HTML and CSS. no frameworks, no client-side routing. everything is generated from markdown
by a small python script and served by GitHub Pages.

to add a post: create `content/posts/your-slug.md`, fill in the frontmatter, write the body,
then run `python3 scripts/build.py`. the page and the card on the blog index are generated for you.

```plaintext
content/posts/*.md          <-- you write here
scripts/build.py            <-- renders the html
blog/<slug>/index.html      <-- generated, do not edit
```
