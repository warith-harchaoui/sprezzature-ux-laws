# sprezzature-ux-laws

[![License](https://img.shields.io/badge/license-BSD--3--Clause-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/)

[![logo](assets/logo.png)](https://harchaoui.org/warith/sprezzature/)

A static **Laws-of-UX** auditor for HTML. It flags the user-experience mistakes that are
decidable straight from source — no browser, no runtime DOM, no network — so you can run
it in a pre-commit hook or a CI step and get a fast, deterministic gate.

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
python scripts/audit_laws_of_ux.py site/ --format json

# Restrict to specific laws, or auto-fix the mechanical ones
python scripts/audit_laws_of_ux.py page.html --laws fitts,jakob
python scripts/audit_laws_of_ux.py page.html --fix
```

Findings are `error` or `warning`; the process exits non-zero when an error is present,
so it drops cleanly into CI.

## Honest scope

The auditor catches mechanical, source-decidable violations. It does not judge whether a
screen answers the right question or whether a flow makes sense — that stays a human call.
It is a fast gate, not a substitute for design review.

## License

BSD-3-Clause © Warith Harchaoui. Part of the [sprezzature](https://harchaoui.org/warith/sprezzature/) toolkit.
