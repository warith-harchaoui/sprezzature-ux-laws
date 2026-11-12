# Contributing

## Setup

```bash
git clone https://github.com/warith-harchaoui/sprezzature-ux-laws
cd sprezzature-ux-laws
pip install -e . -r requirements-dev.txt
```

This is the install the CI (continuous integration, the automatic checks GitHub runs on
every push) runs: the package itself in editable mode, plus
the test toolchain listed in `requirements-dev.txt` (pytest, ruff, mypy,
httpx2). `pip install -e ".[dev]"` installs the same toolchain. Re-run it after a
pull that adds a command: an editable install only learns the console scripts
(`sprezzature-ux-laws`, `-audit`, `-mcp`, `-skill`) that existed when it was made.

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

## Types

The CI runs ruff and pytest, not mypy. The pre-push hook (`.githooks/pre-push`,
enabled with `git config core.hooksPath .githooks`) runs ruff, then mypy, then
pytest; mypy runs in two invocations because `scripts/` imports its siblings by
bare name:

```bash
mypy sprezzature_ux_laws
mypy scripts
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
5. Add a one-line note for it in `_LAW_NOTES` in
   `sprezzature_ux_laws/api.py`, which `GET /v1/laws` and the `list_laws`
   MCP (Model Context Protocol, the protocol through which AI agents call
   tools in English) tool serve.
6. Document the law in the tables of `README.md`, `LISEZMOI.md` and
   `TRIGGERS.md`, add its name to the "mechanically-detectable violations"
   list in `references/laws-of-ux.md` (a test compares that list with
   `LAW_REGISTRY`), and add a sourced entry there if the law is not already
   covered. The skill carries its own copy of that reference, in
   `sprezzature_ux_laws/skill/references/laws-of-ux.md`, and its own table of
   checks in `sprezzature_ux_laws/skill/SKILL.md`: update both.

## Code standards

See `CODING.md`. NumPy docstrings, full typing, ~25-30% comment
density, standard library only in the auditor.

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

The [BSD (Berkeley Software Distribution) 3-Clause licence](LICENSE), a permissive open-source licence.
