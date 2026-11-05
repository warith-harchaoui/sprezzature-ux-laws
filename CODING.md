# CODING.md

Coding standards for sprezzature-ux-laws.

Key rules: NumPy-style docstrings on every function, full typing
(`from __future__ import annotations` at the top of every file),
roughly 25-30% comment density explaining *why* a non-obvious line
does what it does, ruff-clean (`ruff check .`), no bare `except
Exception` without a comment explaining why the broad catch is
intentional.

Stdlib only in the checks of `scripts/audit_laws_of_ux.py`: no
`beautifulsoup`, no `lxml`. The auditor parses HTML with
`html.parser.HTMLParser` on purpose, to stay dependency-free and fast
enough for a pre-commit hook. Its command line parses with click, the
one parser of the suite, imported inside `main()` so that
`import sprezzature_ux_laws` never needs it.
