# Examples

The examples below all run against the same tiny fixture:

```html
<!-- public/index.html -->
<!DOCTYPE html><html><body>
<button class="px-4 bg-blue-600">Go</button>
<div class="cursor-pointer">Menu</div>
</body></html>
```

Line 2 is a `<button>` with no hit-area class (Fitts) and no focus
ring (Aesthetic-Usability). Line 3 is a clickable `<div>` standing in
for a real `<button>` (Jakob).

`px-4` and `bg-blue-600` are two distinct Tailwind utilities, which is
what makes the Fitts and Aesthetic-Usability checks read the page. With
fewer than two, each of those checks reports a single `info` finding on
line 1 ("no Tailwind utilities in this document…") instead.

## Audit a single file

```bash
sprezzature-ux-laws-audit public/index.html
```

Output (text):

```
public/index.html:3: [error] jakob: <div> acts as a button. Use a real <button> or <a href>: native focus, Enter/Space, screen-reader role.
public/index.html:2: [warning] fitts: <button> has no min-h-11 / h-11 (44 px). Confirm the hit area is at least 44×44.
public/index.html:2: [warning] aesthetic-usability: <button> has no focus-visible:ring-* class. Add the house focus token.

audit_laws_of_ux: 3 finding(s).
```

Exit code: `1` (an `error`-severity finding is present). Findings print
in `LAW_REGISTRY` order, not line order.

## Audit a directory recursively

```bash
sprezzature-ux-laws-audit public/
```

## JSON output for machine consumption

```bash
sprezzature-ux-laws-audit --json public/index.html
```

Output (piped through `jq 'length'`, the same run prints `3`):

```json
[
  {
    "law": "jakob",
    "severity": "error",
    "path": "public/index.html",
    "line": 3,
    "message": "<div> acts as a button. Use a real <button> or <a href>: native focus, Enter/Space, screen-reader role.",
    "snippet": ""
  },
  {
    "law": "fitts",
    "severity": "warning",
    "path": "public/index.html",
    "line": 2,
    "message": "<button> has no min-h-11 / h-11 (44 px). Confirm the hit area is at least 44×44.",
    "snippet": ""
  },
  {
    "law": "aesthetic-usability",
    "severity": "warning",
    "path": "public/index.html",
    "line": 2,
    "message": "<button> has no focus-visible:ring-* class. Add the house focus token.",
    "snippet": ""
  }
]
```

## Restrict to specific laws

```bash
sprezzature-ux-laws-audit --only fitts,jakob public/index.html
```

Drops the aesthetic-usability finding, keeps the other two.

## Skip specific laws

```bash
sprezzature-ux-laws-audit --ignore jakob,aesthetic-usability public/index.html
```

Leaves only the Fitts finding.

## Strict mode: promote every warning to an error

```bash
sprezzature-ux-laws-audit --strict --only fitts public/index.html
```

A `fitts` finding is a `warning` by default and would not fail the
run alone; `--strict` makes it exit `1` anyway.

## Auto-fix in place

```bash
sprezzature-ux-laws-audit --fix public/index.html
```

Output (the first line on stderr, the second on stdout):

```
public/index.html: applied 5 fix(es); 0 unfixable finding(s); 0 remaining.
audit_laws_of_ux: 0 findings.
```

The repaired file:

```html
<!DOCTYPE html><html><body>
<button class="px-4 bg-blue-600 min-h-11 focus:outline-none focus-visible:ring-2 focus-visible:ring-brand-blue">Go</button>
<button class="cursor-pointer min-h-11 focus:outline-none focus-visible:ring-2 focus-visible:ring-brand-blue">Menu</button>
</body></html>
```

All three findings had a fixer, and Jakob's `<div>` to `<button>`
rewrite introduces new Fitts and Aesthetic-Usability findings on the
freshly minted `<button>`, which the loop then fixes in a later pass;
5 total edits across every pass, for 3 original findings.

Laws with a fixer: `fitts` (adds `min-h-11`), `aesthetic-usability`
(adds `focus:outline-none focus-visible:ring-2 focus-visible:ring-brand-blue`),
`miller` (splits a long digit-bearing run into groups of four with
non-breaking spaces; names such as `GMTED2010` are never flagged, so never
split), `jakob` (rewrites a clickable `<div>` or
`<span>` that fits on one line to a real `<button>`, removing
`role="button"`). A fixer can only add
tokens to a `class="…"` attribute that already exists on the element;
an element with no `class` attribute at all is reported but left
untouched, and shows up again as `remaining` after the fix pass.

Laws without a fixer (they need a design decision, not a text edit):
`hick`, `choice-overload`, `tesler`, `selective-attention`.

## Preview a fix without writing

```bash
sprezzature-ux-laws-audit --fix --dry-run public/index.html
```

stderr reads `public/index.html: would apply 3 fix(es); 0 unfixable
finding(s); 3 remaining.`, and stdout lists the three original findings.
The count is one pass only, so it does not include the findings a Jakob
rewrite would create. `--dry-run` alone implies `--fix`. Exits `0` always:
a preview, not a verdict.

## Unknown law

```bash
sprezzature-ux-laws-audit --only bogus public/index.html
```

Prints `audit_laws_of_ux: unknown law(s): bogus` on stderr and exits `2`.

## Pre-commit hook

```yaml
# .pre-commit-config.yaml
repos:
  - repo: local
    hooks:
      - id: ux-laws-audit
        name: Laws-of-UX audit
        entry: sprezzature-ux-laws-audit
        language: python
        # Without this, pre-commit builds an empty environment and the entry
        # is not on its PATH. `python scripts/...` does not work either: that
        # path belongs to this repository, not to the one being audited.
        additional_dependencies: ["sprezzature-ux-laws"]
        files: \.html$
        args: ["public/"]
```
