# Triggers

When to audit an interface against the Laws of UX, and what to call.

This file is written for an agent — a Claude Code / OpenCode skill, an MCP
host, anything choosing a tool on someone's behalf. Humans are welcome, but
the routing rules below are the point.

---

## The generalisation, stated once

> **A complaint about how an interface *feels* is the trigger.** Nobody
> names a law. They say "this page is overwhelming", "why does this feel
> slow", "there's too much going on", "I can never find the button", « c'est
> confus », « il y a trop de choix ». Those sentences are usability
> findings in plain clothes, and this is the tool that turns them into
> located, named, fixable ones.

The second trigger is silent, and is the one to remember: **you just wrote an
interface.** A nav, a pricing table, a settings page, a form. Audit it before
handing it over, the same way you would lint the markup.

---

## Which tool, and which neighbour

Three different questions get asked about the same page. Send each to the
right place — they do not substitute for one another:

| The question | Package | Tool |
|---|---|---|
| **Is it usable?** too many choices, targets too small, no feedback | sprezzature-ux-laws | `audit_interface` |
| **Is it accessible?** missing alt, unlabelled inputs, heading order | sprezzature-accessibility | `lint_html` |
| **Is it legible?** contrast, colour-blind safety | sprezzature-colors | `check_contrast`, `simulate_color_blindness` |

A page can pass any one and fail the others. When someone asks a broad
"review my UI", run all three and say which found what.

---

## The eight laws, and the plain-language complaint each answers

You do not need to name a law to route: `audit_interface` runs all eight by
default. This table is for reading the *findings* back to a user in their own
terms.

| Law | The complaint it explains |
|---|---|
| `hick` | "there are too many options", "this menu is enormous" |
| `choice-overload` | "I can't decide", "this pricing table is overwhelming" |
| `miller` | "I can't hold this in my head" — long unchunked numbers, codes, IDs |
| `jakob` | "this doesn't work like everything else does" |
| `fitts` | "the button is tiny", "I keep missing it", "it's too far away" |
| `aesthetic-usability` | "it looks unfinished, so I don't trust it" |
| `selective-attention` | "I never saw that", "the warning is invisible" |
| `tesler` | "this is simple for me and horrible for support" — complexity moved, not removed |

---

## What to call, on every surface

| Job | CLI | MCP tool |
|---|---|---|
| Audit markup | `sprezzature-ux-laws` (the auditor script) | `audit_interface` |
| Which laws exist | — | `list_laws` |

Narrowing to a subset is possible but rarely wise — and if you do it, take
the ids from `list_laws`: a law id that does not exist selects nothing, so a
guessed name silently runs no check.

---

## What this cannot see — say so when you report

The auditor reads markup. It counts choices, measures targets, looks for the
feedback a slow action should give. It cannot watch anybody use the page, so
it finds mechanical mistakes and says nothing about whether the design is
right. Eight laws are checkable this way out of a field that is much larger
and mostly judgement.

Report findings as evidence, never as a verdict. "Nothing fired" means
exactly that — not "this interface is good".

---

## File patterns

`*.html` routes here when a usability concern is expressed — and, per the
generalisation above, when such a file was just written.
