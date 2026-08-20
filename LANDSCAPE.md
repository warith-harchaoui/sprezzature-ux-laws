# Landscape

Design-quality tools split into two families by how they reach a
verdict. A **heuristic** tool checks a page against named principles
from psychology and human-computer-interaction research (Hick's Law,
Fitts's Law, and the like): it flags a *pattern*, not a rendering bug.
A **runtime usability** tool watches a real person, or a simulated one,
use the page, and reports what actually went wrong for them. This
compares `sprezzature-ux-laws`, a static heuristic tool, to the other
ways a team checks whether an interface follows sound UX principles.

## Tool comparison

| Tool | Type | Browser needed | Fixable | CI-friendly | Python |
|---|---|---|---|---|---|
| **sprezzature-ux-laws** | Static heuristic linter | No | Yes (4 laws) | Yes | Yes |
| Manual heuristic review (Nielsen's 10) | Human expert review | No | No | No | N/A |
| Usability testing | Real users, moderated or not | Yes | No | No | N/A |
| axe-core / Pa11y | Runtime DOM, accessibility-focused | Yes | No | Yes (via CLI) | No |
| Hotjar / FullStory (session replay) | Runtime, real-user telemetry | Yes | No | No | No |

### Ratings

| Dimension | sprezzature-ux-laws | Manual heuristic review | Usability testing |
|---|---|---|---|
| Speed (CI) | ⭐⭐⭐⭐⭐ | ⭐ | N/A |
| Catches flow/comprehension issues | ⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| Zero-dep install | ⭐⭐⭐⭐⭐ | N/A | N/A |
| Auto-fix | ⭐⭐⭐ | ⭐ | N/A |
| Repeatable, deterministic | ⭐⭐⭐⭐⭐ | ⭐⭐ | ⭐⭐ |

## When to use what

Use `sprezzature-ux-laws` as a **mechanical pre-commit gate**: it
catches the fraction of each law's violations that are decidable from
the raw HTML text alone (a `<nav>` with too many links, a clickable
`<div>` standing in for a `<button>`), in milliseconds, with no browser
and no human reviewer needed. It cannot tell whether a screen answers
the right question, whether a flow makes sense end to end, or whether
users actually understand what a button does; those need a human.

A manual heuristic review (someone walking the product against Jakob
Nielsen's ten usability heuristics, or the fuller Laws-of-UX set in
`references/laws-of-ux.md`) catches judgment calls this tool cannot
make: is this the right law to apply here, does the grouping actually
make sense to a first-time user. Run it before a release, not on every
commit.

Usability testing (watching five to eight real people attempt real
tasks) is the only method that reveals comprehension failures no
heuristic predicts. Nothing here replaces it; this tool exists so that
the mechanical, source-decidable violations never reach that expensive
session in the first place.

axe-core and Pa11y check accessibility, a related but distinct axis
(can every user operate the page, regardless of ability) from the
Laws-of-UX axis this tool checks (does the page's design match how
human cognition and perception actually work). `sprezzature-accessibility`,
a companion static tool in this same suite, covers the accessibility
axis with the same zero-browser trade-off.

Session-replay tools (Hotjar, FullStory) show what real users did
after shipping. They are a feedback loop, not a gate: useful for
finding what this tool and a heuristic review both missed, too slow
and too late to replace either.
