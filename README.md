# sprezzature-ux-laws

[![License](https://img.shields.io/badge/license-BSD--3--Clause-blue.svg)](https://github.com/warith-harchaoui/sprezzature-ux-laws/blob/main/LICENSE)
[![Python](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/)

[🇫🇷 LISEZMOI.md](https://github.com/warith-harchaoui/sprezzature-ux-laws/blob/main/LISEZMOI.md) · 🇬🇧 README.md

[![logo](https://raw.githubusercontent.com/warith-harchaoui/sprezzature-ux-laws/main/assets/logo.png)](https://sprezzature.ai/)

A static **Laws-of-UX** auditor for HTML.

The "Laws of UX" are named heuristics from psychology and human-computer-interaction
research, curated by Jon YABLONSKI at [lawsofux.com](https://lawsofux.com/). Hick's Law,
for instance, says that the more choices a screen offers at once, the longer a person
takes to pick one, so a navigation menu with forty links is measurably harder to use
than one with seven. This tool cannot see a rendered page or watch a real person use it.
It reads the raw HTML text and flags the mistakes that are decidable from that text
alone, such as counting the links in a `<nav>`. That trade keeps it fast and
deterministic enough to run in a pre-commit hook or a continuous integration (CI) step,
at the cost of catching only the fraction of each law's violations that a text scan can
see. The full, sourced definition of each law lives in
[`references/laws-of-ux.md`](https://github.com/warith-harchaoui/sprezzature-ux-laws/blob/main/references/laws-of-ux.md).

## How it works

![Flow diagram. At the top, HTML source feeds two lanes. The left lane audits: it resolves what a single screen shows from the Tailwind display classes, reports the worse of the phone count and the desktop count, and decides eight named laws, returning findings that exit non-zero on an error. The right lane makes: it applies the four mechanical repairs. Both meet in one outcome, a screen whose measurable mistakes are gone.](https://raw.githubusercontent.com/warith-harchaoui/sprezzature-ux-laws/main/assets/how-it-works.svg)

## Laws covered

Eight laws, in the order the checks run. The slug is the name every surface uses.

| Slug | Law | Severity | What fires it | Fixer |
|---|---|---|---|---|
| `hick` | Hick's Law | error | A `<nav>` showing more than 7 top-level `<a>` or `<button>` choices on one screen (see below) | no |
| `choice-overload` | Choice overload | warning | A `<section>` or `<div>` whose classes contain `pricing` or `plans` and `grid` or `flex`, with more than 4 direct `<article>` or `<div>` columns | no |
| `miller` | Miller's Law | warning | A visible run of 8 or more letters and digits, with at least one digit (codes, IDs, card numbers) | yes |
| `jakob` | Jakob's Law | error | A `<div>` or `<span>` with `onclick`, `role="button"` or `cursor-pointer`, and no real `<button>`, `<a>`, `<input>`, `<select>` or `<summary>` child | yes |
| `fitts` | Fitts's Law | warning | An interactive element with no `h-`, `min-h-` or `size-` class of at least `11` (44 px), or `full`, `screen`, `auto` | yes |
| `aesthetic-usability` | Aesthetic-usability effect | warning | An interactive element with no `focus-visible:ring-*` or `focus:ring-*` class | yes |
| `selective-attention` | Selective attention | warning | A `<span>` coloured `text-red-*`, `text-green-*`, `text-amber-*`, `text-yellow-*` or `text-orange-*`, with no status word ("error", "ok", "pending"…) and no `<svg>` or `<img>` child | no |
| `tesler` | Tesler's Law | warning | An `HH:MM` time with no timezone token (`UTC`, `GMT`, `Z`, `+02:00`, `Europe/Paris`…) within 40 characters | no |

Interactive elements are `<button>`, `<a>`, `<input>`, `<select>`, `<textarea>` and
`<summary>`. What each check leaves alone:

- **Miller** skips text inside `<script>` and `<style>`, the values of `class`, `id`,
  `href` and `src`, purely alphabetic words, and names shaped as three or more letters
  followed by digits only (`GMTED2010`, `LANDSAT8`, `ISO14001`): those are names of
  standards or datasets, and the fixer would otherwise split them with non-breaking
  spaces.
- **Jakob** also leaves a styled `<span>` or `<div>` inside a `<label>` that holds an
  `<input>`, `<select>` or `<textarea>`: the form control carries the semantics.
- **Fitts** skips `<input type="hidden">`, and treats an `<a>` as a text link rather
  than a button unless it carries `inline-flex`, `flex`, `block`, `btn`, `button`, or a
  `bg-` or `border-` class.
- **Tesler** skips a time that sits in a duration context: the words `duration`,
  `elapsed`, `remaining`, `currentTime`, `runtime`, `length`, a `data-ra-` attribute, an
  `ra-time` class, a range input, `<progress>`, `<audio>` or `<video>`. A playback
  position has no timezone.

**Fitts and aesthetic-usability read Tailwind's scale**, so they first ask whether the
document uses Tailwind CSS at all: at least two distinct Tailwind-only utilities, such
as `px-4` and `bg-blue-600`. When it does not, each of the two checks returns one
`info` finding for the whole document instead of one warning per element, and `--fix`
writes no Tailwind classes into it.

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

**A group is one choice.** A `<details>`, a `<dialog>`, a `<menu>`, or an element
whose `role` is `radiogroup`, `tablist`, `menubar`, `listbox` or `combobox`
collapses several controls into a single decision. Each one counts once, whatever
it contains. Two `<nav>` elements on one page are counted apart.

Where the two states are ambiguous the count goes up rather than down: a
control that appears at `md` and disappears again at `lg` is treated as
desktop-only. Over-reporting sends somebody to look; under-reporting ships.

---

## Install

```bash
pip install sprezzature-ux-laws
```

One install gives every surface: the library, both commands, the HTTP API and the MCP
server. The base dependencies are click (the command line), FastAPI, uvicorn,
fastapi-mcp and mcp. There are no feature extras. The only extra, `[dev]`, is the test
toolchain (pytest, ruff, mypy, httpx2).

The auditor itself uses the Python standard library only (`html.parser`), with no
browser and no network, which keeps it cheap enough for a pre-commit hook.

## Command line

```bash
# Audit a file or a whole directory tree
sprezzature-ux-laws public/index.html
sprezzature-ux-laws site/ --json

# Restrict to some laws, or skip some
sprezzature-ux-laws page.html --only fitts,jakob
sprezzature-ux-laws page.html --ignore tesler

# Repair the mechanical ones in place, or preview the repair
sprezzature-ux-laws page.html --fix
sprezzature-ux-laws page.html --fix --dry-run
```

Two installed commands take the same targets and flags and call the same handler:
`sprezzature-ux-laws` (click) and `sprezzature-ux-laws-audit` (the per-tool script).
From a clone, without installing, `python scripts/audit_laws_of_ux.py page.html` runs
that handler too.

| Flag | Effect |
|---|---|
| `--json` | Print a JSON array, one object per finding (`law`, `severity`, `path`, `line`, `message`, `snippet`), instead of the text report. |
| `--strict` | Any finding fails the run, whatever its severity. |
| `--only LAWS` | Comma-separated slugs to run. Default: all eight. |
| `--ignore LAWS` | Comma-separated slugs to skip. |
| `--fix` | Apply the mechanical fixes in place. |
| `--dry-run` | Report what `--fix` would apply, without writing. Implies `--fix`. |
| `--version` | Print the version (`-V` also works on `sprezzature-ux-laws-audit`). |

A target is an `.html` or `.htm` file, or a directory searched recursively for
`*.html`. Any other existing file is skipped with a warning. A path that does not
exist is refused by both commands (exit `2`).

Exit codes:

- `0`: no `error` finding (with `--strict`, no finding at all), or no HTML file found.
  A `--dry-run` always exits `0`.
- `1`: at least one `error` finding (with `--strict`, at least one finding).
- `2`: an unknown slug in `--only` or `--ignore`, a path that does not exist, or
  another usage error.

Findings are printed in the order the checks run, not in line order.

### What `--fix` changes

Four laws have a fixer. The other four (`hick`, `choice-overload`,
`selective-attention`, `tesler`) need a design decision, not a text edit.

| Law | Edit |
|---|---|
| `fitts` | Adds `min-h-11` to the element's `class` attribute. |
| `aesthetic-usability` | Adds `focus:outline-none focus-visible:ring-2 focus-visible:ring-brand-blue`. |
| `miller` | Splits the run into groups of four from the right, joined by non-breaking spaces. |
| `jakob` | Rewrites a single-line `<div>` or `<span>` to `<button>`, and removes `role="button"`. |

The fixer re-audits and repeats, up to five passes, because rewriting a `<div>` into a
`<button>` creates new Fitts and focus-ring findings. A second run on a repaired file
applies zero edits. A fixer only extends a `class` attribute that already exists: an
element without one is counted as unfixable and stays among the remaining findings.
`--fix` rewrites the page, so diff the result before committing it.

## From Python

```python
from pathlib import Path

import sprezzature_ux_laws as ux

for finding in ux.audit_html("<nav>" + '<a href="/">x</a>' * 12 + "</nav>"):
    print(finding.law, finding.severity, finding.message)

ux.audit_file(Path("public/index.html"), laws={"fitts", "jakob"})
applied, unfixable, remaining = ux.fix_file(Path("page.html"), laws=set(ux.LAWS), dry_run=True)
```

The package exports `audit_html`, `audit_file`, `fix_file`, `Finding`, `Walker`,
`Element`, `LAW_REGISTRY`, `LAWS` and `FITTS_FIX_TOKEN`. `ux.LAWS` is the tuple of the
eight slugs, in the order the checks run: the command line validates `--only` against
the same registry, and the HTTP API publishes it.

## HTTP API

```bash
uvicorn sprezzature_ux_laws.api:app --host 127.0.0.1 --port 8000
```

| Method and path | `operation_id` | Answer |
|---|---|---|
| `GET /health` | `health` | `{"status": "ok"}` |
| `GET /v1/laws` | `list_laws` | The eight slugs, each with a one-line note on what it checks. |
| `POST /v1/audit` | `audit_interface` | Body `{"html": "...", "laws": [...]}`; an empty `laws` runs all eight. Returns `findings` (`law`, `severity`, `line`, `message`) and the `errors` and `warnings` counts. |

An unknown slug in `laws` returns HTTP 400, rather than a clean report for checks that
never ran. Interactive documentation is served at `/docs` and `/redoc`. Run this way,
uvicorn serves the routes only: the MCP endpoint is mounted by `sprezzature-ux-laws-mcp`
(below), which serves the same routes and `/mcp` together.

### Docker

```bash
docker compose up -d
curl -s localhost:8000/health
docker compose run --rm api sprezzature-ux-laws-audit --json /work/index.html
```

The image runs `sprezzature-ux-laws-mcp`, so one process on port 8000 serves both the
HTTP routes (`/health`, `/v1/...`) and the MCP endpoint at `/mcp`. Compose mounts
`./work` at `/work` for the pages to audit.

## MCP server

The Model Context Protocol (MCP) lets an agent host call tools directly. The server
wraps the same FastAPI app with fastapi-mcp, so each route's `operation_id` is the tool
name: `health`, `list_laws`, `audit_interface`.

```bash
sprezzature-ux-laws-mcp                      # 127.0.0.1:8000, MCP endpoint at /mcp
sprezzature-ux-laws-mcp --host 0.0.0.0 --port 9000
```

`--host` and `--port` default to `SPREZZATURE_UX_LAWS_HOST` and
`SPREZZATURE_UX_LAWS_PORT` when those are set. `python -m sprezzature_ux_laws.mcp` is
equivalent.

## Agent skill

The skill that tells an agent when to apply these laws, `sprezzature-ux-laws`, ships
from the [sprezzature](https://github.com/warith-harchaoui/sprezzature) hub. The routing
rules and the tool table for agents are in
[`TRIGGERS.md`](https://github.com/warith-harchaoui/sprezzature-ux-laws/blob/main/TRIGGERS.md).

## Honest scope

The auditor catches mechanical, source-decidable violations of eight laws out of the
thirty on lawsofux.com. It does not judge whether a screen answers the right question
or whether a flow makes sense: that stays a human call. Response time (the Doherty
threshold) is not a fact about source, and is not checked. It is a fast gate, not a
substitute for design review.

## License

BSD-3-Clause © Warith HARCHAOUI. Part of the [sprezzature](https://sprezzature.ai/) toolkit.
