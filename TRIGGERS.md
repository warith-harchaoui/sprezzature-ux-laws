# Triggers

When to audit an interface against the Laws of UX (user experience: how an interface
feels to use, such as how long it takes to find the right button), and what to call.

This file is written for an agent: a Claude Code or OpenCode skill, an MCP (Model Context
Protocol, the protocol through which AI agents call tools in English) host, anything
choosing a tool on someone's behalf. Humans are welcome,
but the routing rules below are the point.

---

## The generalisation, stated once

> **Route on the domain's closed vocabulary, not on phrasings.** This package decides
> eight named laws from HTML source. A request belongs here when it names, or when its
> answer depends on, one of the objects those eight laws are about: the number of
> **choices** in a `<nav>` or menu, the **columns** of a pricing or plans grid, an
> unchunked **run of digits** (code, ID, card or phone number), a **clickable `<div>` or
> `<span>`** standing in for a native control, the **hit area** of a target (44 px,
> `min-h-11`), the **focus ring** (`focus-visible:ring-*`), a **status shown by colour
> alone**, a **clock time without a timezone**. The words "Laws of UX", "usability
> heuristic", or a law's own name (Hick, choice overload, Miller, Jakob, Fitts,
> aesthetic-usability, selective attention, Tesler) route here too.

A complaint about how an interface feels ("too many options", "I keep missing the
button") is the same request in plain clothes: map it to one of those objects, then
route. If it maps to none of them, this tool has nothing to say about it.

The second trigger is silent: **you just wrote HTML for an interface.** A nav, a pricing
table, a settings page, a form. Audit it before handing it over, the same way you would
lint the markup.

### The vocabulary that routes elsewhere

| The request is about | Package | Tool |
|---|---|---|
| choices, columns, digit runs, clickable divs, hit area, focus ring, colour-only status, timezone | sprezzature-ux-laws | `audit_interface` |
| alt text, labels, heading order, ARIA (Accessible Rich Internet Applications, the HTML attributes that tell a screen reader what an element is), language attribute, WCAG (Web Content Accessibility Guidelines, the international rules a web page must follow to be usable by people with disabilities) rules | sprezzature-accessibility | `lint_html` |
| contrast ratio, colour-vision deficiency, palette | sprezzature-colors | `check_contrast`, `simulate_color_blindness` |
| response time, the Doherty threshold, real layout or real focus behaviour | none here | a browser tool such as Lighthouse |
| the other 22 laws of lawsofux.com (Peak-End, Von Restorff, Goal-Gradient, Postel…) | none: vocabulary only | read `references/laws-of-ux.md` |

A page can pass one and fail the others. When someone asks for a broad review of the UI (user
interface, the screens, buttons and forms a person uses), run
the first three and say which found what.

---

## Every tool, and the request it answers

| Tool | Request it answers |
|---|---|
| `audit_interface` (`POST /v1/audit`, a route of the HTTP (HyperText Transfer Protocol, the protocol a browser uses to ask a server for a page) API (application programming interface, addresses another program calls to use this tool)) | "Audit this HTML against the Laws of UX", for all eight laws or a named subset. Returns findings with law, severity, line and message, and the error and warning counts. |
| `list_laws` (`GET /v1/laws`) | "Which laws can you check?", and the exact slugs to pass before narrowing an audit. |
| `health` (`GET /health`) | "Is the server up?" Only for diagnosing a connection. |
| `sprezzature-ux-laws`, `sprezzature-ux-laws-audit` | Audit files or directories on disk, with `--json`, `--strict`, `--only`, `--ignore`; repair four laws with `--fix`, preview with `--fix --dry-run`. |
| `sprezzature-ux-laws-mcp` | Start the HTTP app with the MCP endpoint at `/mcp`, so a host can call the three tools above. |
| `sprezzature-ux-laws-skill` | "Is the skill I read up to date?" Reports whether the copy under `~/.claude/skills` matches the installed package; `--install` copies the shipped one there (`--agent opencode` for `~/.opencode/skills`). |
| `audit_html`, `audit_file`, `fix_file` (Python) | The same audit and repair from inside a build step. |
| `skill_path()` (Python) | Where the package keeps its skill, `sprezzature_ux_laws/skill/`. |

---

## The eight laws, and the object each one inspects

You do not need to name a law to route: `audit_interface` runs all eight by default.
This table is for reading the findings back to a user in their own terms.

| Slug | Object inspected | Severity | The complaint it explains |
|---|---|---|---|
| `hick` | top-level choices in one `<nav>`, per screen | error | "there are too many options", "this menu is enormous" |
| `choice-overload` | columns of a pricing or plans grid | warning | "I can't decide", "this pricing table is overwhelming" |
| `miller` | visible runs of 8 or more letters and digits | warning | "I can't hold this in my head" |
| `jakob` | a `<div>` or `<span>` acting as a button | error | "this doesn't work like everything else does" |
| `fitts` | hit area of interactive elements (Tailwind pages) | warning | "the button is tiny", "I keep missing it" |
| `aesthetic-usability` | focus ring on interactive elements (Tailwind pages) | warning | "it looks unfinished", "I can't see where I am with the keyboard" |
| `selective-attention` | a status `<span>` signalled by colour only | warning | "I never saw that", "the warning is invisible" |
| `tesler` | `HH:MM` times without a timezone | warning | "what time is that, mine or theirs?" |

On a page that does not use Tailwind CSS (Cascading Style Sheets, the rules that give a
web page its colours, fonts and layout), `fitts` and `aesthetic-usability` each return
one `info` finding for the document instead of per-element warnings.

---

## What to call, on every surface

The five surfaces are the library (Python), the CLI (command-line interface, a program
you run by typing a command in a terminal), the HTTP API, MCP, and the skill.

| Job | CLI | MCP tool (= `operation_id`) | HTTP route | Python |
|---|---|---|---|---|
| Audit markup | `sprezzature-ux-laws PATH…` or `sprezzature-ux-laws-audit PATH…` | `audit_interface` | `POST /v1/audit` | `audit_html`, `audit_file` |
| Repair the mechanical laws | `sprezzature-ux-laws PATH --fix` (`--dry-run` to preview) | none | none | `fix_file` |
| Which laws exist | `sprezzature-ux-laws --help` (lists the slugs) | `list_laws` | `GET /v1/laws` | `LAWS`, `LAW_REGISTRY` |
| Is the server up | none | `health` | `GET /health` | none |
| Serve the tools | `sprezzature-ux-laws-mcp` | none | none | none |
| Install or refresh the skill | `sprezzature-ux-laws-skill --install` | none | none | `skill_path` |

Repair is a command-line and Python job only: no route or MCP tool writes files.

Narrowing to a subset is possible but rarely useful. If you do it, take the slugs from
`list_laws`: an unknown slug is refused (HTTP 400 on the API, exit code 2 for `--only` or
`--ignore` on the command line), so a guessed name fails loudly rather than running
nothing.

---

## What this cannot see: say so when you report

The auditor reads markup. It counts choices, reads class names, matches text patterns.
It cannot watch anybody use the page and it does not measure response time, so it finds
mechanical mistakes and says nothing about whether the design is right. Eight laws are
checkable this way out of the thirty on lawsofux.com.

Report findings as evidence, never as a verdict. "Nothing fired" means exactly that,
not "this interface is good".

---

## File patterns

`*.html` and `*.htm` route here when one of the objects above is in question, and, per
the generalisation, when such a file was just written. A directory target is searched
for both.
