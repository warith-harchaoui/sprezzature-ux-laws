"""
sprezzature-ux-laws: the FastAPI HTTP surface.

Module summary
--------------
Exposes the laws-of-UX auditor over HTTP, so a design review, a CI job, or
an editor plugin in any language can check an interface against the eight
laws without shelling out to Python. ``POST /v1/audit`` calls
:func:`sprezzature_ux_laws.audit_html`, the function the command line
reaches too, so the HTTP answer and the terminal answer cannot disagree.

What ships here
---------------
- ``GET  /health``: a liveness probe.
- ``GET  /v1/laws``: the eight laws, each with what it checks.
- ``POST /v1/audit``: audit a string of HTML and return the findings.

What this can and cannot tell you
----------------------------------
These checks read *structure*, not experience. "Nine links in a nav" is a
fact about the markup, and Hick's law says more choices cost decision time;
whether nine is too many for *this* audience, doing *this* task, is a
judgement no linter holds. The findings are prompts for a designer, not
verdicts: only two laws report errors (``hick`` above seven choices and
``jakob`` for a ``<div>`` or ``<span>`` acting as a button); the other six
report warnings, and ``fitts`` and ``aesthetic-usability`` report a single
``info`` on a page that does not use Tailwind.

FastAPI and uvicorn are base dependencies since 2026-11-01, so there
is no extra to ask for::

    pip install 'sprezzature-ux-laws'

Then run the app with any ASGI server::

    uvicorn sprezzature_ux_laws.api:app --host 0.0.0.0 --port 8000

Usage example
-------------
>>> # curl -X POST localhost:8000/v1/audit \\
>>> #      -H 'content-type: application/json' \\
>>> #      -d '{"html": "<button class=\\"p-1\\">Go</button>"}'
>>> # Full OpenAPI docs at http://localhost:8000/docs

Author
------
`Warith HARCHAOUI, Ph.D. <https://www.linkedin.com/in/warith-harchaoui/>`_
"""

from __future__ import annotations

try:
    from fastapi import FastAPI, HTTPException
    from fastapi.responses import RedirectResponse
except ImportError as exc:  # pragma: no cover - dependency guard
    raise ImportError(
        "The FastAPI HTTP surface could not import fastapi, which is a base "
        "dependency since 2026-11-01 -- so this is a broken install rather "
        "than a missing extra. Reinstall with: "
        "pip install 'sprezzature-ux-laws'"
    ) from exc

from pydantic import BaseModel, Field

# The checks come from this package's own library surface, which exists for
# exactly this: one set of names that the command line, this API, the MCP
# tools and somebody else's build step all read.
#
# Until 1.2.0 these two lines were a sys.path insert and a bare-name import
# of `audit_laws_of_ux`, chosen because the modules sit in scripts/ in a
# checkout and ship as a package in a wheel. It worked, and it made an HTTP
# surface depend on a directory layout. A package import holds under both.
from . import LAW_REGISTRY, audit_html  # noqa: E402
from . import __version__ as _VERSION  # noqa: E402

#: One line per law, so a caller (or an agent) knows what it is being told.
#: Kept here rather than in the auditor because it is presentation: the
#: checks themselves need no prose to run.
_LAW_NOTES: dict[str, str] = {
    "hick": "Decision time grows with the number of choices. Flags a <nav> showing more than seven top-level choices on one screen.",
    "choice-overload": "Too many comparable options stall a choice entirely. Flags a pricing or plans grid with more than four columns.",
    "miller": "Working memory holds about seven items. Flags visible runs of eight or more letters and digits that contain a digit.",
    "jakob": "People expect your site to work like the others they know. Flags a <div> or <span> acting as a button instead of a native control.",
    "fitts": "Time to hit a target falls with its size. Flags interactive elements without a 44 px height class (Tailwind pages).",
    "aesthetic-usability": "A tidy interface is perceived as more usable. Flags interactive elements without a focus-visible ring class (Tailwind pages).",
    "selective-attention": "People miss what they are not looking for. Flags a status shown by colour alone, with no word or icon.",
    "tesler": "Complexity is conserved: what the interface drops, the user carries. Flags clock times shown without a timezone.",
}

app = FastAPI(
    title="Sprezzature UX Laws API",
    description=(
        "HTTP surface for sprezzature-ux-laws: audit an interface against "
        "eight laws of UX — Hick, Miller, Fitts, Jakob, Tesler and friends."
    ),
    version=_VERSION,
    docs_url="/docs",
    redoc_url="/redoc",
)


class AuditRequest(BaseModel):
    """Body for ``POST /v1/audit``."""

    html: str = Field(description="HTML source. A fragment is fine; no document wrapper required.")
    laws: list[str] = Field(
        default_factory=list,
        description="Laws to run, by slug. Empty runs all eight.",
    )


@app.get(
    "/health",
    tags=["meta"],
    operation_id="health",
    summary="Check that this UX-audit server is up",
)
def health() -> dict:
    """
    Liveness probe — no dependency check, just proves the app is up.

    Call this only to diagnose a connection problem.

    Returns
    -------
    dict
        ``{"status": "ok"}``.
    """
    return {"status": "ok"}


@app.get(
    "/v1/laws",
    tags=["meta"],
    operation_id="list_laws",
    summary="List the UX laws this auditor can check",
)
def laws() -> dict:
    """
    The eight laws, each with a one-line note on what it checks.

    Call this to answer "which laws do you know", and before narrowing
    `audit_interface` to a subset -- a law id that does not exist is refused
    with HTTP 400, so take the ids from here rather than guessing. It also draws the
    boundary: eight laws, mechanically checkable, out of a field that is much
    larger and mostly judgement.

    Returns
    -------
    dict
        ``{"laws": [{"id": ..., "checks": ...}, ...]}``.
    """
    return {
        "laws": [
            {"id": slug, "checks": _LAW_NOTES.get(slug, "")}
            for slug in LAW_REGISTRY
        ]
    }


@app.post(
    "/v1/audit",
    tags=["actions"],
    operation_id="audit_interface",
    summary="Audit an interface against the Laws of UX",
)
def audit(request: AuditRequest) -> dict:
    """
    Audit a string of HTML against the requested laws.

    This is the tool for "is this interface any good", "too many options",
    "why does this feel slow", "review my UI", « est-ce que cette interface
    est utilisable » -- the usability question, as distinct from the
    accessibility one (sprezzature-accessibility) and the contrast one
    (sprezzature-colors).

    It reads the markup: it counts choices, reads the classes that size a
    target or draw a focus ring, matches codes and clock times in the text.
    It does not measure response time. It cannot watch anybody use the page,
    so it finds the mechanical mistakes and says nothing about whether the
    design is right. Report it as evidence, never as a verdict.

    Parameters
    ----------
    request : AuditRequest
        The markup and which laws to run.

    Returns
    -------
    dict
        ``findings`` (law, severity, line, message), plus ``errors`` and
        ``warnings`` counts (``info`` findings are listed but not counted).

    Raises
    ------
    fastapi.HTTPException
        400 when an unknown law slug is requested — silently ignoring it
        would return a clean report for checks that never ran.
    """
    requested = set(request.laws) if request.laws else set(LAW_REGISTRY)
    unknown = sorted(requested - set(LAW_REGISTRY))
    if unknown:
        raise HTTPException(
            status_code=400,
            detail=f"unknown law(s): {unknown}. Known: {sorted(LAW_REGISTRY)}",
        )

    findings = audit_html(request.html, requested)
    rows = [
        {"law": f.law, "severity": f.severity, "line": f.line, "message": f.message}
        for f in findings
    ]
    return {
        "findings": rows,
        "errors": sum(1 for r in rows if r["severity"] == "error"),
        "warnings": sum(1 for r in rows if r["severity"] == "warning"),
    }


@app.get("/docs-redirect", include_in_schema=False)
def docs_redirect() -> RedirectResponse:
    """Convenience redirect to the interactive API docs."""
    return RedirectResponse(url="/docs")
