"""
sprezzature_ux_laws -- a static Laws-of-UX auditor for HTML.

The "Laws of UX" are named heuristics from psychology and human-computer
interaction research (Hick's Law, Miller's Law, Fitts's Law, Jakob's Law,
Tesler's Law, and more; curated by Jon YABLONSKI at lawsofux.com and
restated with sources in ``references/laws-of-ux.md``). Most tools check
them by rendering a page in a real browser and measuring it; this one
instead reads the raw HTML text and flags only what is decidable from
that text alone, for example a ``<nav>`` with more menu items than
Hick's Law says a user can scan at a glance. That trade keeps the check
fast enough for a pre-commit hook or a CI gate, at the cost of missing
anything that only shows up once the page actually renders (real layout
sizes, real response time, focus behaviour under a mouse).

Author
------
Warith HARCHAOUI <warithmetics@deraison.ai>
"""
from __future__ import annotations

__version__ = "1.2.0"
__author__ = "Warith HARCHAOUI"
__email__ = "warithmetics@deraison.ai"
__license__ = "BSD-3-Clause"

# The library surface. Until this existed, `import sprezzature_ux_laws` gave
# you a version string and nothing else: the auditor was reachable from a
# command line, from HTTP and from an agent, and not from Python — which is
# the one place a static HTML check is most obviously useful, inside somebody
# else's build step.
#
# `api.py` reached it by inserting `scripts/` on sys.path and importing
# `audit_laws_of_ux` by bare name. That works, and it is also how a surface
# ends up depending on a layout rather than on a package. These names are the
# contract now, and every surface reads them from here.
from sprezzature_ux_laws_scripts.audit_laws_of_ux import (  # noqa: E402
    FITTS_FIX_TOKEN,
    LAW_REGISTRY,
    Element,
    Finding,
    Walker,
    audit_file,
    audit_html,
    fix_file,
)

#: Every law this package knows how to check, in the order the registry runs
#: them. Exported because all four surfaces need the same list: the command
#: line validates `--laws` against it, the HTTP API publishes it, and the MCP
#: tool schema is derived from the API.
LAWS: tuple[str, ...] = tuple(LAW_REGISTRY)

__all__ = [
    "FITTS_FIX_TOKEN",
    "LAWS",
    "LAW_REGISTRY",
    "Element",
    "Finding",
    "Walker",
    "audit_file",
    "audit_html",
    "fix_file",
]
