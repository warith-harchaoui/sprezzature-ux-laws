# sprezzature-ux-laws

[![License](https://img.shields.io/badge/license-BSD--3--Clause-blue.svg)](https://github.com/warith-harchaoui/sprezzature-ux-laws/blob/main/LICENSE)
[![Python](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/)

[🇫🇷 LISEZMOI.md](https://github.com/warith-harchaoui/sprezzature-ux-laws/blob/main/LISEZMOI.md) · 🇬🇧 README.md

[![logo](https://raw.githubusercontent.com/warith-harchaoui/sprezzature-ux-laws/main/assets/logo.png)](https://sprezzature.ai/)

A static **Laws-of-UX** auditor for HTML.

The "Laws of UX" are named heuristics from psychology and human-computer-interaction
research: for instance, Hick's Law says that the more choices a screen offers at once,
the longer a person takes to pick one, so a navigation menu with forty links is
measurably harder to use than one with seven. This tool cannot see a rendered page or
watch a real person use it; instead it reads the raw HTML text and flags the mistakes
that are decidable from that text alone, such as counting the links in a `<nav>`. That
trade keeps it fast and deterministic enough to run in a pre-commit hook or a CI step,
at the cost of catching only the fraction of each law's violations that a text scan can
see (the full, sourced definition of each law lives in
[`references/laws-of-ux.md`](https://github.com/warith-harchaoui/sprezzature-ux-laws/blob/main/references/laws-of-ux.md)).

## How it works

![Flow diagram. At the top, HTML source feeds two lanes. The left lane audits: it resolves what a single screen shows from the Tailwind display classes, reports the worse of the phone count and the desktop count, and decides eight named laws, returning findings that exit non-zero on an error. The right lane makes: it applies the four mechanical repairs. Both meet in one outcome, a screen whose measurable mistakes are gone.](https://raw.githubusercontent.com/warith-harchaoui/sprezzature-ux-laws/main/assets/how-it-works.svg)

## Laws covered

| Law | What it catches |
|---|---|
| **Hick's Law** | Too many choices presented at once (over-long menus / nav). |
| **Choice overload** | Long option lists with no grouping or default. |
| **Miller's Law** | Unchunked digit runs (phone numbers, codes) beyond ~7 items. |
| **Jakob's Law** | Non-conventional patterns where a familiar one is expected. |
| **Fitts's Law** | Interactive controls with no 44 px (`min-h-11`) hit area. |
| **Aesthetic-Usability** | Interactive elements missing a visible focus ring. |
| **Selective attention** | Elements styled like ads that carry real content. |
| **Tesler's Law** | Irreducible complexity pushed onto the user. |

## How it counts: choices, not elements

Hick's Law measures the choices a person faces **at one moment**, so counting
the links in a file gets it wrong twice.

**A responsive header holds two menus.** A row marked `hidden sm:inline` and a
hamburger marked `sm:hidden` never appear together: the phone reader sees one
set, the desktop reader sees the other. Adding them up charges the reader for
choices no screen ever shows. The auditor resolves each control's visibility
from its Tailwind display classes, walking ancestors (a container that hides
its subtree wins over a child that would show), and reports the worse of the
phone count and the desktop count, naming which one it is.

**A group is one choice.** A `<details>`, a `<menu>`, a `role="radiogroup"`
or a `role="tablist"` collapses several controls into a single decision. Each
one counts once, whatever it contains.

Where the two states are ambiguous the count goes up rather than down: a
control that appears at `md` and disappears again at `lg` is treated as
desktop-only. Over-reporting sends somebody to look; under-reporting ships.

---

## Install

```bash
pip install sprezzature-ux-laws               # the auditor: no dependencies
pip install "sprezzature-ux-laws[click]"      # + the click front door
pip install "sprezzature-ux-laws[api,mcp]"    # + the HTTP and agent surfaces
```

That the auditor has **no dependencies at all** is the point of it, and the
reason it is cheap enough to put in a pre-commit hook: standard library,
milliseconds, no browser. Everything heavier is an extra, named after what
needs it.

## Use

```bash
# Audit a file or a whole directory tree
sprezzature-ux-laws-audit public/index.html
sprezzature-ux-laws-audit site/ --json

# Restrict to specific laws, or auto-fix the mechanical ones
sprezzature-ux-laws-audit page.html --only fitts,jakob
sprezzature-ux-laws-audit page.html --fix
```

`sprezzature-ux-laws` is the same thing through click, with the same flags and
the same handler — use whichever matches the rest of your tooling. From a
clone, without installing, it reads `python scripts/audit_laws_of_ux.py
page.html`.

Findings are `error` or `warning`; the process exits non-zero when an error is present,
so it drops cleanly into CI.

## From Python

```python
from pathlib import Path

import sprezzature_ux_laws as ux

for finding in ux.audit_html("<nav>" + '<a href="/">x</a>' * 12 + "</nav>"):
    print(finding.law, finding.message)

ux.audit_file(Path("public/index.html"), laws={"fitts", "jakob"})
ux.fix_file(Path("page.html"), laws=set(ux.LAWS), dry_run=True)
```

`ux.LAWS` is the tuple of every law it knows, in the order the checks run —
the same list the command line validates `--only` against and the HTTP API
publishes, read from one place so the four surfaces cannot disagree.

## Honest scope

The auditor catches mechanical, source-decidable violations. It does not judge whether a
screen answers the right question or whether a flow makes sense. That stays a human call.
It is a fast gate, not a substitute for design review.

## License

BSD-3-Clause © Warith HARCHAOUI. Part of the [sprezzature](https://sprezzature.ai/) toolkit.
