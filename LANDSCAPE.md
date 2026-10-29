# Landscape

`sprezzature-ux-laws` is the user-experience (UX) audit brick of the
[sprezzature](https://sprezzature.ai/) suite, a set of Python packages for building
publication-quality web content. It never renders a page and never watches anyone use
one: it reads the raw HTML text and settles the fraction of eight named laws that a text
scan can honestly decide. That trade buys speed and determinism, at the cost of the
other twenty-two laws and of everything a law only reveals once a person is in front of
the screen.

## How it fits in the ecosystem

```
sprezzature suite
├── sprezzature-ux-laws       ← this package (8 of 30 laws, from the source alone)
├── sprezzature-ui            (writes the screen this one audits, and the design tokens)
├── sprezzature-accessibility (the neighbouring axis: 20 rules, same zero-browser trade)
├── sprezzature-colors        (contrast and colour-vision deficiency)
├── sprezzature-figures       (167 chart types, and the vision loop)
├── sprezzature-publish       (turns the audited pages into a site)
└── sprezzature-video         (checks what a film claims about all of the above)
```

**What comes before.** `sprezzature-ui` generates the markup: semantic HTML, Tailwind
utilities, the house focus token, the three-Roboto typography rule. Two of the eight
checks here read that stack's own scale (`min-h-11` for a 44-pixel hit area,
`focus-visible:ring-*` for the focus ring), which is why the auditor asks whether a
document uses Tailwind at all before it reports on either.

**What comes after.** `sprezzature-publish` turns a folder of Markdown into a site, and
the pages it emits are exactly what this auditor is pointed at in a pre-commit hook.

**The sibling doing the neighbouring job.** `sprezzature-accessibility` asks whether
every reader can operate the page, whatever their ability. This one asks whether the
page matches how attention, memory and motor control actually work. The two overlap on
exactly one point, colour used as the only status channel, and they flag it from
different angles.

## When to choose it

- **You want a pre-commit hook, not a report.** The median page of this suite's own
  site, about 20 kilobytes, audits in roughly five milliseconds, with no browser to
  start and nothing to install beyond Python and click. A gate that costs nothing runs
  every time; one that costs thirty seconds gets disabled.
- **You need the same verdict twice.** The checks are pure text analysis. No model, no
  network, no sampling. The build that failed yesterday fails today for the same reason,
  and a reviewer can reproduce it on a laptop with no account.
- **You are generating HTML with an agent and want a mechanical floor.** An agent that
  writes a clickable `<div>` will write it again. `--fix` repairs four of the eight laws
  in place, loops until it reaches a fixed point, and applies zero edits on a second
  pass over a repaired file.
- **You want the rule and its paper in the same repository.**
  `references/laws-of-ux.md` restates the canonical set with its origin named for each
  entry: HICK 1952 and HYMAN 1953, MILLER 1956, DOHERTY and THADANI 1982, KUROSU and
  KASHIMURA 1995. A finding points at a law, and the law points at a publication.

## When to pick something else

- **Baymard UX-Ray** wins on coverage and on evidence. It scans 209 UX parameters
  against a library of more than 700 published guidelines, and Baymard reports a 95 %
  agreement with how its own human auditors rated the same sites. Nothing here is
  measured against human judgement at all. If the question is "is this checkout any
  good", that is the tool, and it costs money.
- **Maze, Lyssna, UXtweak and UserTesting** win the moment the question is whether
  anyone understands the screen. A static scan cannot discover that a label is
  ambiguous, that a flow asks for a number the user does not have, or that the button
  everyone needs is the one nobody finds. Five to eight real participants will. Nothing
  in this document replaces that session; this tool exists so the mechanical faults
  never reach it.
- **axe-core and Pa11y** win on accessibility, which is the neighbouring axis and a far
  more mature one. They run against a real document object model (DOM), they map each
  rule to a Web Content Accessibility Guidelines (WCAG) success criterion, and Deque
  reports that a continuous-integration (CI) gate built on them catches roughly 57 % of
  accessibility defects. This package checks none of that and should not be asked to.
- **Lighthouse plus field data** wins on the Doherty Threshold, which is the law this
  package explicitly cannot check: response time is not a fact about source.
  `references/laws-of-ux.md` says so and names Lighthouse as the answer. Even Lighthouse
  only half-wins, since Interaction to Next Paint (INP) needs real interactions and lab
  tooling reports Total Blocking Time as a proxy; the Chrome User Experience Report
  (CrUX) carries the real number.
- **ux-skill** wins on rule count inside the same niche, with 152 deterministic offline
  rules across nine categories, a Model Context Protocol (MCP) server, installers for
  seventeen editors, and a run under 200 milliseconds. It is the nearest frontal
  competitor this search turned up. It is also younger, and far less cited per rule,
  which is the trade in the other direction.
- **Microsoft Clarity** wins on price for the thing this tool structurally cannot see.
  It is free with no session cap, and rage clicks and dead clicks are evidence about
  real people that no scan of the markup produces.

## Ideas worth stealing

Ordered best return first. Two of the six are refusals, with the reason, which is the
point of looking.

**1. SARIF output, from the whole static-analysis ecosystem.** The Static Analysis
Results Interchange Format
([SARIF 2.1.0](https://docs.github.com/en/code-security/code-scanning/integrating-with-code-scanning/sarif-support-for-code-scanning))
is the OASIS JSON schema GitHub code scanning ingests, and ruff, clippy, detekt and
golangci-lint all emit it. A tool declares its rules once, then each result points back
at a rule id and a physical location. Here it is a `--sarif` flag beside `--json` in
`scripts/audit_laws_of_ux.py`, with `LAW_REGISTRY` becoming the `rules` array and each
`Finding` becoming a `result` carrying `path` and `line`. The payoff is that a Hick
finding lands as an annotation on the pull-request diff, beside the `<nav>` that caused
it, read by nobody and seen by everybody. The cost is an afternoon and no new
dependency, since the output is `json.dumps` of a different shape.

**2. A per-finding suppression comment, from ESLint and from axe-core's
`hideElements`.** Both let you silence one occurrence in one place, in the file, where
the reason can sit next to it. This package has only `--ignore tesler`, which drops the
law on every page, including the clock times it exists for. The repository already knows
this: the docstring above `RE_DURATION_CONTEXT` says the only remedy on offer "silences
the law everywhere, including on the clock times it is for". The fix is an HTML comment
read by `Walker`, `<!-- ux-laws-disable-next-line tesler: this is a playback position
-->`, with the text after the colon required rather than optional. Half a day, and it
would have spared the hand-written duration heuristic that sits in the file today.

**3. Pa11y's `threshold`, and its per-URL configuration.**
[Pa11y](https://github.com/pa11y/pa11y) accepts a number of findings to permit before
the run fails, which is what lets a team point it at a legacy tree, pin the count where
it stands, and ratchet it down. Here it is `--max-warnings N` on both front doors, plus
a `.ux-laws.toml` holding one budget per path glob. Today the choice is binary: errors
fail, warnings never do, and `--strict` fails on everything. An afternoon for the flag,
a day for the file, and the file is the part worth hesitating over, because a
configuration format is a thing you then owe people forever.

**4. axe-core's four result buckets.** axe returns `violations`, `passes`, `incomplete`
and `inapplicable`, so silence is never ambiguous: you can tell a rule that found
nothing from a rule that had nothing to look at. This package already has the idea at
half strength, in `_not_a_tailwind_page`, which says once per document that a scale
check could not read a Tailwind class list. Generalising it means `--json` carrying a
per-law status block beside the findings, so a clean report also says which of the eight
actually ran. Half a day, and most of the thinking is done.

**5. Baymard's published agreement rate, refused for now.** Baymard states a
[95 % agreement](https://baymard.com/blog/ai-heuristic-evaluations) between UX-Ray and
its own human auditors on the same sites. That is a better claim than any rule count,
and it is the single most credible thing a competitor in this field does. Reproducing it
here means a corpus of hand-labelled pages, two labellers to measure against each other,
and a precision and recall figure per law. That is a week of work before a line of code,
and the corpus has to be maintained as the rules move. Worth doing the day the rule set
stops changing; not before, because a measured number on a moving rule set is a number
about last month.

**6. A vision model reading the rendered page, refused with a caveat.**
[uxlint](https://github.com/GyeongHoKim/uxlint) drives Playwright, screenshots the page,
and asks a multimodal model to judge usability from a declared persona. It gets what no
text scan can: crowding, visual hierarchy, whether the primary action looks primary. It
also costs a Chrome install, a model, and determinism, which are the three things this
package is built out of refusing. The caveat is that the suite already owns the
mechanism, in `sprezzature-figures`'s Ralph Eyeball Loop, which runs a local model
offline. So the honest statement is not "we cannot" but "not in the brick whose whole
selling point is that a pre-commit hook can afford it".

## How the field divides

**By what the tool is allowed to look at.** A *source reader* parses the markup a
developer just wrote: this package, ux-skill, Banno's ux-lint, `@lapidist/design-lint`.
A *runtime checker* needs the page to exist and render, which is where axe-core, Pa11y
and Lighthouse live, and it is a real jump in cost, because a browser has to start. A
*behaviour recorder* needs people on the live site, which is Hotjar, Microsoft Clarity
and LogRocket. A *study* needs recruited participants, which is Maze, Lyssna, UXtweak,
UserTesting and Optimal Workshop. The further down that list you go, the more a tool
knows and the later it can tell you.

**By whether a model is in the loop.** The 2025 and 2026 entrants almost all put one
there. Baymard UX-Ray went from 39 parameters in October 2025 to 209 a year later, UX
Pilot reviews a design file inside the design tool, uxlint drives a browser and a
multimodal model, and Attention Insight and Neurons Predict guess where the eye will
land from models trained on recorded eye-tracking fixations. These see things a parser
cannot. They also return a different answer on a different day, which is tolerable in a
design review and not in a gate.

**By whether it gates or reports.** A gate runs before the change lands, exits non-zero,
and blocks. A report runs after, and tells you what already happened. Session replay and
CrUX are reports by construction, because they need traffic that only exists once the
page is live. Usability studies sit in between: they run before launch, but not before
every commit. This package is a gate and nothing else, and most of what it cannot do
follows from that one choice.

## How it compares

Every tool rated 1 to 5 on each criterion, higher is better, from ⭐ weak to ⭐⭐⭐⭐⭐
strongest. The scores are an argued judgement, not a benchmark, and each axis is
oriented so more stars mean stronger on that trait: for cost, more stars mean cheaper or
more open. A single ⭐ means the tool does not do that thing at all, which on a
capability scale is a one. The machine-readable source is
[`assets/landscape.csv`](assets/landscape.csv): 25 tools across 13 criteria.

| UX quality tool | Free or open source | Speed in continuous integration | Deterministic and reproducible | Laws of UX covered | Catches comprehension and journey problems | Automatic repair | No browser required | Runs entirely on your machine | No human reviewer needed | No real traffic needed | Published source per rule | Maturity and ecosystem | Machine-readable output |
| --- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| sprezzature-ux-laws | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐ | ⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐ | ⭐⭐⭐⭐ |
| ux-skill | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐ | ⭐⭐ | ⭐⭐⭐⭐ |
| uxlint | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐ | ⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐ | ⭐ | ⭐⭐⭐⭐ |
| Banno ux-lint | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐ | ⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐ | ⭐ | ⭐⭐⭐ |
| sprezzature-accessibility | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐ | ⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐ | ⭐⭐⭐⭐ |
| axe-core | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐ | ⭐ | ⭐ | ⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| Pa11y | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐ | ⭐ | ⭐ | ⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| Lighthouse | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐ | ⭐ | ⭐ | ⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| @lapidist/design-lint | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐ | ⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐ | ⭐⭐ | ⭐⭐⭐⭐ |
| Figma Design Lint | ⭐⭐⭐⭐⭐ | ⭐ | ⭐⭐⭐⭐ | ⭐ | ⭐ | ⭐⭐ | ⭐⭐ | ⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐ | ⭐⭐⭐ | ⭐ |
| Baymard UX-Ray | ⭐ | ⭐ | ⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐ | ⭐⭐ | ⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐ |
| UX Pilot | ⭐⭐ | ⭐ | ⭐⭐ | ⭐⭐ | ⭐⭐⭐ | ⭐⭐ | ⭐⭐ | ⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐ | ⭐ |
| Heurio | ⭐⭐⭐ | ⭐ | ⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐ | ⭐ | ⭐ | ⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐ | ⭐⭐ |
| Manual heuristic review (NIELSEN) | ⭐⭐⭐⭐ | ⭐ | ⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐ |
| Maze | ⭐⭐ | ⭐ | ⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐ | ⭐ | ⭐ | ⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ |
| Lyssna | ⭐⭐ | ⭐ | ⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐ | ⭐ | ⭐ | ⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ |
| UXtweak | ⭐⭐⭐ | ⭐ | ⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐ | ⭐ | ⭐ | ⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ |
| UserTesting | ⭐ | ⭐ | ⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐ | ⭐ | ⭐ | ⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐ |
| Optimal Workshop | ⭐⭐ | ⭐ | ⭐⭐ | ⭐⭐ | ⭐⭐⭐⭐ | ⭐ | ⭐⭐ | ⭐ | ⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ |
| Hotjar | ⭐⭐⭐ | ⭐ | ⭐⭐ | ⭐⭐ | ⭐⭐⭐⭐ | ⭐ | ⭐ | ⭐ | ⭐⭐ | ⭐ | ⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ |
| Microsoft Clarity | ⭐⭐⭐⭐ | ⭐ | ⭐⭐ | ⭐⭐ | ⭐⭐⭐⭐ | ⭐ | ⭐ | ⭐ | ⭐⭐ | ⭐ | ⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ |
| LogRocket | ⭐⭐ | ⭐⭐ | ⭐⭐ | ⭐⭐ | ⭐⭐⭐⭐ | ⭐ | ⭐ | ⭐ | ⭐⭐ | ⭐ | ⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| Attention Insight | ⭐⭐ | ⭐ | ⭐⭐⭐ | ⭐⭐ | ⭐⭐ | ⭐ | ⭐⭐ | ⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐ |
| Neurons Predict | ⭐ | ⭐ | ⭐⭐⭐ | ⭐⭐ | ⭐⭐ | ⭐ | ⭐⭐ | ⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐ |
| CrUX + web-vitals | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ | ⭐ | ⭐⭐ | ⭐ | ⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |

![Positioning map of 25 UX quality tools on two axes derived from a principal component analysis. Top right, alone in its corner, sits sprezzature-ux-laws, with Banno ux-lint, @lapidist/design-lint, sprezzature-accessibility and ux-skill just beside it: the tools that read source, need nothing, and run for free. The opposite corner, bottom left, holds UserTesting, Maze, Hotjar, Microsoft Clarity and LogRocket, the ones that need recruited participants or live traffic. Top left holds axe-core, Pa11y, Lighthouse and CrUX, mature and pipeline-ready. Bottom right holds the manual heuristic review and Heurio, which need no infrastructure and a person. The horizontal axis opposes needing nothing to being established; the vertical opposes what a machine does cheaply to what only a person finds.](assets/landscape.svg)

The source is [`assets/landscape.csv`](assets/landscape.csv), the star table above and
nothing added, and the map is regenerated with:

```sh
python ~/sprezzature/scripts/landscape_to_csv.py LANDSCAPE.md
standpoint assets/landscape.csv --outdir assets --stem landscape --check
```

The geometry is ordinary correlation principal component analysis (PCA) and it is
**deterministic**: the same table gives the same map every run. The four words at the
edges come from a local model, and they are vaguer than the loadings behind them, so the
loadings are the control. Here is what the two axes are actually made of.

**Horizontal, `Robustness ↔ Autonomy`, 50.6 % of the variance.** No real traffic needed
(+0.50), no browser required (+0.40) and automatic repair (+0.37) pull right; maturity
and ecosystem (−0.43) and machine-readable output (−0.32) pull left. The axis opposes
*needing nothing* to *being established*. `sprezzature-ux-laws` sits at the far right by
construction: it is the reference row, and `standpoint` anchors the reference top right.
That is a convention of the drawing, not a claim about quality, and the honest reading
of the left end is that axe-core, Pa11y, Lighthouse and the Chrome User Experience
Report have an ecosystem this package does not.

**Vertical, `Usability ↔ Efficiency`, 14.4 % of the variance.** Machine-readable output
(+0.43), speed in continuous integration (+0.38), free or open source (+0.35) and no
human reviewer needed (+0.32) load at the top; laws of UX covered (−0.35) and catches
comprehension and journey problems (−0.33) load at the bottom. That is the whole
argument of this document in one axis: the things a machine does cheaply sit opposite
the things only a person finds. UserTesting is the lowest point on the map, and it is
the tool that would tell you the most.

**Two axes carry 65.0 % of the table.** A third of what those 13 criteria say is not on
this page. The map is a first orientation; the table is the evidence. `standpoint --check`
also reports `readable: False` for this figure, because at 25 points five pairs of
labels risk overlapping (`sprezzature-ux-laws` with `Banno ux-lint`, `ux-skill` with
`sprezzature-accessibility`, `Lyssna` with `UXtweak`, `Hotjar` with `Microsoft Clarity`
and with `LogRocket`). Those pairs overlap because they genuinely rate almost the same,
which is information, but the label crowding is a real defect of the picture and the
coordinates in [`assets/landscape.yaml`](assets/landscape.yaml) are where to read it
exactly. `standpoint` writes a prose interpretation beside the figure as well; it is not
reproduced here, because a model reading back ratings somebody else wrote is not a
finding.

## Sources

- Jon YABLONSKI, [lawsofux.com](https://lawsofux.com/), the curated set of 30 laws, and
  *Laws of UX*, O'Reilly, 2nd ed. 2024.
- Baymard Institute, [AI heuristic UX evaluations with a 95 % accuracy
  rate](https://baymard.com/blog/ai-heuristic-evaluations) and [UX-Ray
  2.0](https://baymard.com/research-articles/ux-ray-2-point-0-launch).
- [Pa11y](https://github.com/pa11y/pa11y), its `threshold`, `ignore` and `hideElements`
  options, and its five reporters.
- [SARIF support for code
  scanning](https://docs.github.com/en/code-security/code-scanning/integrating-with-code-scanning/sarif-support-for-code-scanning),
  GitHub documentation.
- [ux-skill](https://github.com/Laith0003/ux-skill), 152 deterministic offline rules,
  and [uxlint](https://github.com/GyeongHoKim/uxlint), the browser-and-model approach.
- [Heurio](https://www.heurio.co/guidelines), the guideline library: NIELSEN's ten
  heuristics, SHNEIDERMAN's eight golden rules, RAMS's ten principles, ISO 9241-110,
  WCAG 2.2.
- [Attention Insight](https://attentioninsight.com/) and
  [Neurons Predict](https://www.neuronsinc.com/), the second of which absorbed
  VisualEyes and Loceye; both trained on recorded eye-tracking fixations.
- Nielsen Norman Group, [The Aesthetic-Usability
  Effect](https://www.nngroup.com/articles/aesthetic-usability-effect/), Kate MORAN and
  Kathryn WHITENTON, February 2024.
