# Triggers

Natural-language phrases that invoke the sprezzature-ux-laws skill.

## Direct invocations

- "Audit this page against the Laws of UX"
- "Check this HTML for Hick's Law violations"
- "Run the UX laws auditor"
- "Is this nav menu too big?"
- "Check for clickable divs that should be buttons"
- "Does this button have a big enough hit area?"
- "Check the focus rings on this page"
- "Chunk this long phone number / code / ID"
- "Fix the UX law violations in this file"
- "Run audit_laws_of_ux.py"

## Intent-based phrases

- "Does this screen offer too many choices?"
- "Is this pricing table overwhelming?"
- "Are these time stamps missing a timezone?"
- "Is this status shown with color alone?"
- "Apply Hick / Fitts / Miller / Jakob / Tesler to this page"
- "Why does this menu feel overwhelming?"
- "Check this against lawsofux.com"

## File patterns

Files matching `*.html` routed to this skill when a Laws-of-UX
concern is expressed.

## Related scripts

- `scripts/audit_laws_of_ux.py`: main auditor
- `scripts/_argparse.py`: shared parser factory

## Related reference

- `references/laws-of-ux.md`: the sourced Laws-of-UX set this auditor
  checks against, with the fuller trigger, action, and Tailwind/HTML
  hook table for the laws that need a design decision instead of a
  mechanical fix.
