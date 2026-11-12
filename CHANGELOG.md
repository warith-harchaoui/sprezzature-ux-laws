# Changelog

All notable changes to sprezzature-ux-laws are documented here.

## [Unreleased]

## [1.5.0] — 2026-11-12

### Added

- **The skill ships inside the package.** `sprezzature_ux_laws/skill/` holds the
  `SKILL.md` an agent reads and its `references/` (the thirty laws, the trigger
  catalogue), so one `pip install` carries all five surfaces: library, command line,
  HTTP (HyperText Transfer Protocol, the protocol a browser uses to ask a server for a
  page) API (application programming interface, addresses another program calls to use
  this tool), MCP (Model Context Protocol, the protocol
  through which AI agents call tools in English) server, and skill. Until now it
  lived only in the sprezzature hub.
- **`sprezzature-ux-laws-skill`**, a fourth command: it reports whether the copy under
  `~/.claude/skills` is in step with the installed package, `--install` copies the
  shipped one there (moving an older copy to `skills-superseded/`), `--agent opencode`
  targets `~/.opencode/skills`, and `--path` prints where pip put it.
- **`sprezzature_ux_laws.skill_path()`** returns that folder.

### Docs

- README and LISEZMOI: the five surfaces and the four installed commands are listed;
  the "Agent skill" section said the skill shipped from the hub, and now documents
  `sprezzature-ux-laws-skill`; `skill_path` is among the exports; `-V` and the exit `2`
  on a non-numeric port of `sprezzature-ux-laws-mcp` are stated.
- SKILL.md: the banner and the surfaces table still said the skill lived in a monorepo
  and the tools had moved out; they now say it ships in the package, and how to install it.
- TRIGGERS.md: `sprezzature-ux-laws-skill` and `skill_path` added to the tool tables;
  acronyms defined at first use.
- CODING.md said `import sprezzature_ux_laws` never needs click; since `_skill.py`
  it does, and says so. CONTRIBUTING.md: the CI (continuous integration, the automatic checks
  GitHub runs on every push) runs ruff and pytest but
  not mypy, which the pre-push hook runs; an editable install must be redone to pick up
  a new command; a new law also goes in the skill's own reference and table.

## [1.4.3] — 2026-11-08

### Fixed

- **The MCP server announces its version as a version.** fastapi-mcp 0.4 passes
  the description into `Server`'s version slot, so `serverInfo.version` was a
  sentence. It is the package version now, and the description is `instructions`.
- **`--fix` writes no Tailwind class on a page without Tailwind.** The single
  `info` such a page gets went to the fixer, which added the classes on line 1;
  the re-audit then read the page as a Tailwind page, and the next pass wrote
  them on every control. The README had always said it did not.
- **The Fitts and Aesthetic-Usability fixers write on the element the finding
  is about.** They extended the first `class` on the line: a card around a
  button got the hit-area class and the focus ring, the button stayed reported,
  the second control of a line was counted unfixable, and an element without a
  `class` handed its tokens to its neighbour. A finding now records the column
  of its tag.
- **Tesler no longer takes `px-4` for a timezone.** Any sign followed by a digit
  counted as an offset within the 40-character window, so a class name, a date
  or a phone number silenced the check on most Tailwind pages. An offset now
  has to be glued to the minutes or stand alone, and be at most 14 hours.
- **Selective attention reads whole words.** The `ok` of `Look` passed for a
  status word. `warnings`, `successful` and `failing` were added to the list.
- **Miller skips an HTML comment over several lines**, which is not visible text.
- **`<wbr>` and the other void elements not yet listed** (`base`, `col`, `embed`,
  `param`, `track`) no longer adopt the siblings after them, which hid a real
  link from the Jakob check.
- **`--fix` keeps a form feed or a U+2028.** Lines were cut with `splitlines`
  and joined with `\n`, which replaced those characters with a line break, and
  the numbering disagreed with the HTML parser's.
- **A non-numeric `SPREZZATURE_UX_LAWS_PORT`** is a usage error (exit `2`) on
  `sprezzature-ux-laws-mcp`, not a traceback, even on `--help`.

Eighteen regression cases in `tests/test_ux_laws.py` and `tests/test_api_mcp.py`,
each failing without its fix. Three `--fix` tests used a page with a single
kind of Tailwind utility and passed thanks to the first defect above: their
fixture now has two kinds.

### Docs

- README, LISEZMOI, EXAMPLES.md: the Tailwind detection counts kinds of
  utility, not utilities (`px-4` and `py-2` are one kind); a fixer also leaves
  an element whose `class` is not on the line its tag opens; running the script
  from a clone needs click.
- LANDSCAPE.md and PAYSAGE.md: 168 chart types.

## [1.4.2] — 2026-11-05

### Fixed

- **The Miller fixer chunks the run the reader sees, never the markup.**
  The check strips tags and attribute values before it looks, but the fixer
  replaced the first occurrence of the run on the raw line, which is often
  an `href` or a `data-` value standing before the text:
  `<a href="/orders/AB12CD34EF">` came back with non-breaking spaces inside
  its URL, a second pass then chunked the text too, and the run reported
  nothing left. It now rewrites a whole run outside every tag and quoted
  attribute value, or nothing.
- **The Jakob fixer rewrites the clickable element, not the first `<div>` or
  `<span>` on the line.** On `<div class="card"><span onclick="go()">` it
  made the card a button, then the span a second button inside it, and
  reported zero findings on invalid HTML; it also renamed the first closing
  tag of that name rather than the element's own. It now picks the element
  that is clickable the way the check means it, holds no real control and
  closes on the same line, finds its own closing tag by nesting, and leaves
  anything else reported as unfixable.

### Docs

- README, LISEZMOI, EXAMPLES.md and the skill say what Miller skips as it
  is: every tag and its attributes on the line, not only `class`, `id`,
  `href` and `src` (those four are what it strips on a tag split across
  lines), and that `--fix` leaves the same run inside a tag alone. The Jakob
  row says which element is rewritten and when it is left.
- `sprezzature-ux-laws --help` says `--dry-run` implies `--fix`, as it
  already did and as the per-tool script's help said.

Three regression tests in `tests/test_ux_laws.py`, each failing on the old
fixers.

## [1.4.1] — 2026-11-05

### Fixed

- **`--fix` writes a file only when a fixer changed something.** The loop
  wrote the page before every audit pass, so a run with zero edits still
  rewrote it.
- **`--fix` keeps the line endings.** The file was read with universal
  newlines and written back with `\n`, so every CRLF page came back LF. It
  is now read as bytes and written back in its own endings.
- **A directory target picks up `.htm` files**, as a file target already
  did. It searched for `*.html` only.

### Changed

- **`sprezzature-ux-laws -V`** prints the version, like the other two
  commands; only `--version` worked on the click command.

Five regression tests in `tests/test_ux_laws.py`.

### Docs

- README.md and LISEZMOI.md: the `[dev]` extra lists httpx2 too, and running
  `uvicorn sprezzature_ux_laws.api:app` is said to serve the routes only, with
  `/mcp` mounted by `sprezzature-ux-laws-mcp`.
- EXAMPLES.md: the JSON example piped into `jq 'length'` and showed the array;
  it now shows the array and says the pipe prints `3`.
- CODING.md and the auditor's docstrings: the checks are stdlib only, the
  command line parses with click; the Jakob check names every control child
  it accepts and the label exemption; `Finding.severity` includes `info`.
- README.md, LISEZMOI.md and TRIGGERS.md: `-V` on every command, `.htm` in
  directory targets, and `--fix` writing only on a change, in the file's own
  line endings.
- `assets/how-it-works.yaml`: the footer said "No dependencies at all"; the
  checks use the standard library only, the package has base dependencies.
  The figure is redrawn from the hub.

## [1.4.0] — 2026-11-04: click everywhere, and two refusals

### Changed

- **Click is the only parser, for every command.** `sprezzature-ux-laws-audit`
  and `sprezzature-ux-laws-mcp` parsed with argparse; both are click now,
  through `scripts/_click.py`, with the same flags, defaults, help texts and
  exit codes (a usage error still exits 2). The usage line now reads
  `Usage:`. `scripts/_argparse.py` is deleted, since nothing imports it. The
  click command is built inside `main()`, so `import sprezzature_ux_laws`
  still works on a machine without click.
- **`-V` prints the package version.** `sprezzature-ux-laws-audit -V` printed
  `1.0.0`, a stale helper constant, while the package is at 1.3.0.
  `sprezzature-ux-laws-mcp`
  gains `-V` too.
- **The Docker image serves `/mcp` as well.** Its CMD ran
  `uvicorn sprezzature_ux_laws.api:app`, which never imports `mcp.py`, so the
  container answered the HTTP routes and not the MCP endpoint. It now runs
  `sprezzature-ux-laws-mcp --host 0.0.0.0 --port 8000`, and
  `docker-compose.yml` states the same command: one process, one port, both
  `/v1/...` and `/mcp`.
- **A guard test**, `tests/test_click_only.py`: every console script answers
  `--help` with exit 0 and a click usage line, and no module of the package
  imports argparse.

### Fixed

- **`--ignore` with an unknown slug is refused**, with exit code 2 and the
  same `unknown law(s)` message as `--only`. It used to be accepted and skip
  nothing, so the law it meant to silence still ran. Both commands share the
  handler, so both now refuse it.
- **`sprezzature-ux-laws-audit` refuses a path that does not exist** (exit 2),
  as the click command already did. It skipped the target with a warning and
  exited 0, so a typo in a CI target turned the gate green.
- **The `[dev]` extra matches `requirements-dev.txt`**: mypy bounded to
  `>=1.11,<3`, and httpx2 added for starlette's TestClient. Both were in the
  file the CI installs and missing from the extra.

Three regression tests in `tests/test_ux_laws.py`.

### Docs

The documentation now says what the code does, checked against the code and
by running every command it shows.

- **README.md and LISEZMOI.md.** The laws table described checks that do not
  exist: Jakob flagged "non-conventional patterns" (it flags a `<div>` or
  `<span>` acting as a button), Selective attention "elements styled like ads"
  (a status shown by colour alone), Tesler "irreducible complexity" (a clock
  time with no timezone), Choice overload "long option lists" (a pricing or
  plans grid with more than four columns). The table now gives each slug, its
  severity, its exact trigger and whether it has a fixer. The install section
  showed the same `pip install` twice and still said "everything heavier is an
  extra"; there is one install and `[dev]` is the only extra. Added what was
  missing: the `info` severity and the Tailwind precondition of Fitts and
  aesthetic-usability, the exemptions of each check (including the acronym
  guard that keeps `GMTED2010` whole), the full list of Hick grouping
  containers, every flag, the exit codes 0, 1 and 2, what `--fix` writes, the
  HTTP routes with their `operation_id`, Docker and compose, the MCP server
  and its options, and where the skill ships from.
- **TRIGGERS.md.** Routing now rests on the closed vocabulary of the eight
  laws rather than on sample phrasings. It claimed that an unknown law id
  "silently runs no check"; the API answers 400 and the command line exits 2.
  It listed one command for two and left out `sprezzature-ux-laws-audit`,
  `sprezzature-ux-laws-mcp` and the `health` tool, and it said the auditor
  "looks for the feedback a slow action should give", which no check does.
- **EXAMPLES.md.** The fixture had a single Tailwind utility, so the Fitts and
  aesthetic-usability findings shown never appeared: the auditor reports one
  `info` per check instead. The fixture now carries two, and every output
  shown was rerun. The `--fix` output was labelled stderr though half of it is
  stdout.
- **references/laws-of-ux.md.** Said it restated each of the 30 laws and held
  29: Fitts's Law, one of the eight the auditor checks, was missing. Pointed at
  `ux-psychology.md` and `anti-patterns.md` as if they were here; they belong
  to `sprezzature-ui`. Surnames are now in capitals.
- **CONTRIBUTING.md.** The setup line installed the test tools and not the
  package. It now matches the CI, and the steps for a new law name every place
  that has to learn it.
- **LANDSCAPE.md and PAYSAGE.md.** "Nothing to install beyond Python and
  click" predates the single install.
- **Comments.** `requirements.txt` said "No runtime dependencies"; the
  `[project.scripts]` comment in `pyproject.toml` presented argparse as the
  click command's twin by choice.
- **Docstrings and comments.** `mcp.py` named three tools from
  `sprezzature-colors` (`check_contrast`, `simulate_color_blindness`,
  `get_palette`) and argued for colour checks. `api.py` said every finding is
  a warning unless a hit area is too small (Fitts is a warning; Hick and Jakob
  are the errors), and its per-law notes served by `list_laws` described
  checks that do not exist. The auditor's docstring named two severities out
  of three and a `references/checklist.md` that is not in this repository. The
  `Dockerfile` comment still spoke of an `api` extra.

## [1.3.0] — 2026-11-01: one `pip install`

### Changed — one `pip install`

**Everything this package does now installs with it.** 3 extras became
**one**, and it is not a feature: `[dev]` is the test toolchain.

  Both surfaces. The base was **one** dependency — click — so `pip install
  sprezzature-ux-laws` gave an audit command and no way to call it over HTTP.

Measured across the suite before touching anything: **59 extras over eleven
repositories**, and **six bricks whose base was a single dependency** — so
`pip install <brick>` installed almost nothing and did almost nothing, and
choosing the right extra was a thing a reader had to know *before* the package
could do its job. Here the base goes from **1** to **5**
dependencies.

All eleven unions were dry-run resolved in a clean venv before any manifest was
edited, so this is a measured feasibility and not an optimistic one.

### Fixed — the places that encoded the extras

Install lines, error messages, docstrings, the `Dockerfile`, the CI workflow and
the README/LISEZMOI install sections all named extras that no longer exist. pip
treats an unknown extra as a **warning and exits 0**, so none of these would
have failed loudly: they would have quietly installed nothing.

The hub's `test_no_document_promises_an_extra_that_does_not_exist` found the
cross-repository ones — a document in one brick naming another brick's extra —
which no per-repository pass would have caught.

## [1.2.0] - 2026-10-19: the two surfaces this package did not have

Five surfaces is the contract across this suite — library, command line, HTTP
API, MCP, skill — and this package had three. The gaps were the two most
basic ones.

### Added

- **A library surface.** `import sprezzature_ux_laws` gave you a version
  string and nothing else. The auditor was reachable from a command line,
  from HTTP and from an agent, and not from Python — which is the one place a
  static HTML check is most obviously useful, inside somebody else's build
  step. `audit_html`, `audit_file`, `fix_file`, `Finding`, `Walker`,
  `Element`, `LAW_REGISTRY`, `LAWS` and `FITTS_FIX_TOKEN` are the contract
  now, and every surface reads them from there.

- **`sprezzature-ux-laws`, the click twin**, over the same flags and the same
  handler as `sprezzature-ux-laws-audit`. Both build the same argument vector
  and hand it to the same `main`, so a flag cannot exist on one front door and
  be missing from the other — a test derives the argparse flags from the
  source and checks the twin against them.

  Click is an **extra**, and the import is guarded. The auditor declares no
  dependencies at all, which is what makes it cheap enough for a pre-commit
  hook; a twin importing click at module load would end that silently,
  because the failure arrives at the console script rather than at the
  install. The guard is checked by actually hiding click from a subprocess.

### Changed

- **`api.py` imports the package, not a directory.** It reached the checks by
  inserting `scripts/` on `sys.path` and importing `audit_laws_of_ux` by bare
  name. That worked, and it made an HTTP surface depend on a layout: the
  module imported correctly from a checkout and from a wheel for two
  different reasons, and only one of them was a package.

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
