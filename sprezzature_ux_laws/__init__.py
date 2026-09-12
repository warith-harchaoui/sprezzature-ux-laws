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
Warith HARCHAOUI <warith.harchaoui@gmail.com>
"""
from __future__ import annotations

__version__ = "1.0.0"
__author__ = "Warith HARCHAOUI"
__email__ = "warith.harchaoui@gmail.com"
