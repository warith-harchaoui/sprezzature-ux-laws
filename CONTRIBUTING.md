# Contributing

## Setup

```bash
git clone https://github.com/warith-harchaoui/sprezzature-ux-laws
cd sprezzature-ux-laws
pip install -r requirements-dev.txt
```

## Tests

```bash
pytest
```

## Lint

`ruff` is the Python linter and formatter this project uses: it reads
the source without running it and flags style issues (unused imports,
wrong quote style, and the like) in one fast pass.

```bash
ruff check .
```

## Adding a law check

1. Add a `check_<law_name>(walker, path)` (or `check_<law_name>(path,
   lines)` for a text-only check) function in `scripts/audit_laws_of_ux.py`.
2. Register it in `LAW_REGISTRY`, as `(walker_fn, None)` or
   `(None, text_fn)` depending on which input shape it needs.
3. If a mechanical fix exists, add a `_fix_<law_name>` function and
   register it in `LAW_FIXERS`.
4. Add a test in `tests/test_ux_laws.py`: at least one file that should
   trigger the finding, one that should not.
5. Document the law in the table in `README.md` / `LISEZMOI.md`, and add
   a sourced entry to `references/laws-of-ux.md` if the law is not
   already covered there.

## Code standards

See `CODING.md`. NumPy docstrings, full typing, ~25-30% comment
density, stdlib only.

## Prose standards

English prose (README, docstrings, comments) follows WRITING.md:
https://gist.github.com/warith-harchaoui/f45304d066abc81dd7d4f059a1f4e45f

French prose (LISEZMOI) follows ECRITURE.md:
https://gist.github.com/warith-harchaoui/7cc42b038e86c5195ec09f0531111ba4

No punctuation dashes, no machine tells ("Moreover", "In conclusion",
reflexive "not only X but also Y"). Acronyms glossed on first use.

## Releases

Releases live in `CHANGELOG.md`, tagged `vX.Y.Z` in git, and published
as GitHub releases.

## Authorship

Sole author: [Warith HARCHAOUI](https://www.linkedin.com/in/warith-harchaoui/).
External contributions are welcome. Open an issue or pull request on GitHub.

## License

[BSD-3-Clause](LICENSE).
