# Examples

The examples below all run against the same tiny fixture:

```html
<!-- public/index.html -->
<!DOCTYPE html><html><body>
<button class="px-4">Go</button>
<div class="cursor-pointer">Menu</div>
</body></html>
```

Line 2 is a `<button>` with no hit-area class (Fitts) and no focus
ring (Aesthetic-Usability). Line 3 is a clickable `<div>` standing in
for a real `<button>` (Jakob).

## Audit a single file

```bash
python scripts/audit_laws_of_ux.py public/index.html
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
python scripts/audit_laws_of_ux.py public/
```

## JSON output for machine consumption

```bash
python scripts/audit_laws_of_ux.py --json public/index.html | jq 'length'
```

Output:

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
python scripts/audit_laws_of_ux.py --only fitts,jakob public/index.html
```

Drops the aesthetic-usability finding, keeps the other two.

## Skip specific laws

```bash
python scripts/audit_laws_of_ux.py --ignore jakob,aesthetic-usability public/index.html
```

Leaves only the Fitts finding.

## Strict mode: promote every warning to an error

```bash
python scripts/audit_laws_of_ux.py --strict --only fitts public/index.html
```

A `fitts` finding is a `warning` by default and would not fail the
run alone; `--strict` makes it exit `1` anyway.

## Auto-fix in place

```bash
python scripts/audit_laws_of_ux.py --fix public/index.html
```

stderr output:

```
public/index.html: applied 5 fix(es); 0 unfixable finding(s); 0 remaining.
audit_laws_of_ux: 0 findings.
```

All three findings had a fixer, and Jakob's `<div>` to `<button>`
rewrite introduces new Fitts and Aesthetic-Usability findings on the
freshly minted `<button>`, which the loop then fixes in a later pass;
5 total edits across every pass, for 3 original findings.

Laws with a fixer: `fitts` (adds `min-h-11`), `aesthetic-usability`
(adds `focus-visible:ring-2 …`), `miller` (chunks long digit runs with
non-breaking spaces), `jakob` (rewrites a single-line `<div
role="button">` / `<span>` to a real `<button>`). A fixer can only add
tokens to a `class="…"` attribute that already exists on the element;
an element with no `class` attribute at all is reported but left
untouched, and shows up again as `remaining` after the fix pass.

Laws without a fixer (they need a design decision, not a text edit):
`hick`, `choice-overload`, `tesler`, `selective-attention`.

## Preview a fix without writing

```bash
python scripts/audit_laws_of_ux.py --fix --dry-run public/index.html
```

Exits `0` always: a preview, not a verdict.

## Pre-commit hook

```yaml
# .pre-commit-config.yaml
repos:
  - repo: local
    hooks:
      - id: ux-laws-audit
        name: Laws-of-UX audit
        entry: python scripts/audit_laws_of_ux.py
        language: python
        files: \.html$
        args: ["public/"]
```
