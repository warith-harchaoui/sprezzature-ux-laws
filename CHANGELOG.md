# Changelog

All notable changes to sprezzature-ux-laws are documented here.

## [Unreleased] - 2026-08-20

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
- `references/laws-of-ux.md`: sourced restatement of Jon Yablonski's
  canonical Laws of UX set, in the skill's trigger, action, and
  Tailwind/HTML hook format.
- `sprezzature_ux_laws/__init__.py`: package metadata.
- 6 tests in `tests/`, all passing. ruff clean.
