# Changelog

All notable changes to sprezzature-ux-laws are documented here.

## [1.1.0] - 2026-10-02: the auditor is installable, which is the whole package

Two changelog sections sat under "Unreleased" since August and September. They
ship here, together with the release that makes the auditor reachable at all.

### Added

- **`sprezzature-ux-laws-audit`, a console script.** The auditor is this
  package's reason to exist and nothing installed it. The README told readers
  to run `python scripts/audit_laws_of_ux.py`, a path that exists in a clone
  and not in a wheel, and the parser's own `--help` advertised
  `sprezzature-ux-laws-audit`, which nothing registered. Someone who ran `pip
  install sprezzature-ux-laws` could reach the MCP server and nothing else.
- **A type gate**, `mypy.ini` plus one CI step. The monorepo carried one while
  the skills lived there; at the split ruff came with the package and mypy did
  not, so no standalone package checked its own annotations. Run by hand, it
  found the `main` defect below in six packages at once. The step runs once, on
  3.12: this is a gate, not a test matrix.
- **`test_mcp_fallback_signature.py`**, which reads the source as a syntax tree
  and so needs neither mypy nor an install, and a case in
  `test_console_scripts_exist.py` ruling out the state where its scan finds no
  candidates and the file reports green while testing nothing.
- **A versioned `.githooks/pre-push`** running the same lint, type and test
  steps as the workflow, in the same order, so a red state cannot reach the
  remote.

### Fixed

- **`mcp.py` defined `main` twice, and the two took different arguments.** One
  definition sits in the `except ImportError` branch reached when the `[mcp]`
  extra is absent, the other in the `else` branch that serves the real
  endpoint. A single console script reaches both, so to a caller they are one
  function. They were not: the fallback took nothing while the real one took
  `argv`, so `main(["--host", "127.0.0.1"])` answered on a machine with the
  extra and raised `TypeError` on a machine without it. The broken half is the
  one a reader who skipped the extra meets first.
- **Hick counted two breakpoints as one, and Miller broke acronyms apart.**
  Two counting defects in the audit itself.
- **The declared homepage named a host that no longer answers.**
  `project.urls` pointed at `harchaoui.org`, now returning 503, and PyPI prints
  that link on the package page. It points at `sprezzature.ai`.

- `fix_file`: the live `--fix` and `--dry-run` summary line ("N unfixable
  finding(s)") only counted findings whose law has no fixer registered
  at all (Hick, Choice overload, Tesler). A finding whose law *does*
  have a fixer, but whose specific instance the fixer declines to touch
  (Fitts/Aesthetic-Usability on an element with no `class="..."`
  attribute for `_insert_class_tokens` to extend), was counted as
  neither applied nor skipped: the printed "unfixable" count silently
  undercounted what still needed a human, even though the honest
  `remaining` count right after it was always correct. Both `fix_file`
  code paths now count a declining fixer call as skipped too, matching
  `_insert_class_tokens`'s own documented contract. New regression test:
  `test_fix_mode_counts_declined_fixer_as_skipped`.

### Added (retroactive changelog entry for prior, already-committed work)

- `RE_TZ_TOKEN` missed compact ISO-8601 timestamps like `12:34Z` (no
  word boundary exists between a digit and a letter, so `\bZ\b` never
  matched); added `(?<=\d)Z\b` as an extra alternative. Added tests for
  the 5 laws that previously had zero test coverage (Hick, Miller,
  Choice overload, Selective attention, Tesler) and for `--fix` mode.
  Committed as `5805266` on 2026-09-02; this entry was missing from the
  changelog until now.

### Also shipping here, held since 2026-08-20

### Fixed

- `scripts/audit_laws_of_ux.py`: `Walker.handle_endtag` unwound the
  entire open-element stack on a stray closing tag with no matching
  opener (a common artifact in hand-written or templated HTML), instead
  of ignoring it. That silently corrupted every later ancestor-based
  check (Hick's `<nav>` counting, the Jakob label-wrapped-control
  exemption) for the rest of the file. Now searches for a match before
  mutating the stack, and ignores a stray tag when none exists.
- `check_aesthetic_usability`: a comment claimed `<input type="submit">`
  was exempt from the focus-ring check, but the only `continue` in that
  branch fired for `type="hidden"`; a submit button still fell through
  to the normal check. Removed the dead branch: only `type="hidden"`,
  which is genuinely non-interactive, is exempt.
- `_fix_jakob`: tried both the `div` and `span` rewrite patterns against
  the same line unconditionally, risking a rewrite of an unrelated
  element sharing the line with the one actually flagged. Now stops
  once one tag type has produced a fix.
- README.md: the "Use" section documented `--format json` and
  `--laws fitts,jakob`, neither of which exists in the CLI (the real
  flags are `--json` and `--only`). Corrected.

### Added

- `LISEZMOI.md`, `CODING.md`, `CONTRIBUTING.md`, `Dockerfile`,
  `EXAMPLES.md`, `LANDSCAPE.md`, `PAYSAGE.md`, `TRIGGERS.md`: repo
  structure brought in line with sibling `sprezzature-*` packages.

## [1.0.0] - 2026-07-30

### Added

- `scripts/audit_laws_of_ux.py`: static Laws-of-UX auditor for HTML.
  Stdlib only, no browser. Eight checks: Hick, Choice Overload, Miller,
  Jakob, Fitts, Aesthetic-Usability, Selective Attention, Tesler.
  Text and JSON output, `--only`, `--ignore`, `--strict`, `--fix`, and
  `--dry-run` modes. Auto-fixers for Fitts, Aesthetic-Usability, Miller,
  and Jakob; idempotent by design.
- `scripts/_argparse.py`: shared argparse parser factory.
- `references/laws-of-ux.md`: sourced restatement of Jon YABLONSKI's
  canonical Laws of UX set, in the skill's trigger, action, and
  Tailwind/HTML hook format.
- `sprezzature_ux_laws/__init__.py`: package metadata.
- 6 tests in `tests/`, all passing. ruff clean.
