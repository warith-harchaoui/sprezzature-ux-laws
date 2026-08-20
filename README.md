# sprezzature-ux-laws

[![License](https://img.shields.io/badge/license-BSD--3--Clause-blue.svg)](https://github.com/warith-harchaoui/sprezzature-ux-laws/blob/main/LICENSE)
[![Python](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/)

[🇫🇷 LISEZMOI.md](https://github.com/warith-harchaoui/sprezzature-ux-laws/blob/main/LISEZMOI.md) · 🇬🇧 README.md

[![logo](https://raw.githubusercontent.com/warith-harchaoui/sprezzature-ux-laws/main/assets/logo.png)](https://harchaoui.org/warith/sprezzature/)

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
[`references/laws-of-ux.md`](references/laws-of-ux.md)).

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

## Use

```bash
# Audit a file or a whole directory tree
python scripts/audit_laws_of_ux.py public/index.html
python scripts/audit_laws_of_ux.py site/ --json

# Restrict to specific laws, or auto-fix the mechanical ones
python scripts/audit_laws_of_ux.py page.html --only fitts,jakob
python scripts/audit_laws_of_ux.py page.html --fix
```

Findings are `error` or `warning`; the process exits non-zero when an error is present,
so it drops cleanly into CI.

## Honest scope

The auditor catches mechanical, source-decidable violations. It does not judge whether a
screen answers the right question or whether a flow makes sense. That stays a human call.
It is a fast gate, not a substitute for design review.

## License

BSD-3-Clause © Warith Harchaoui. Part of the [sprezzature](https://harchaoui.org/warith/sprezzature/) toolkit.
