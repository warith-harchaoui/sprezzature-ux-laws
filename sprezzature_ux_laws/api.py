"""
sprezzature-ux-laws: the FastAPI HTTP surface.

Module summary
--------------
Exposes the laws-of-UX auditor over HTTP, so a design review, a CI job, or
an editor plugin in any language can check an interface against the eight
laws without shelling out to Python. Every route calls
:func:`audit_laws_of_ux.audit_html` — the same function the command line
calls — so the HTTP answer and the terminal answer cannot disagree.

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
verdicts — which is why every one of them is a warning rather than an error
unless it breaks something measurable, like a hit area below 44 px.

Install the extra to get the runtime dependencies::

    pip install 'sprezzature-ux-laws[api]'

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
`Warith Harchaoui, Ph.D. <https://www.linkedin.com/in/warith-harchaoui/>`_
"""

from __future__ import annotations

import sys
from pathlib import Path

try:
    from fastapi import FastAPI, HTTPException
    from fastapi.responses import RedirectResponse
except ImportError as exc:  # pragma: no cover - dependency guard
    raise ImportError(
        "The FastAPI HTTP surface requires the [api] extra. "
        "Install with: pip install 'sprezzature-ux-laws[api]'"
    ) from exc

from pydantic import BaseModel, Field

# The checks live in the scripts package, which is where the command line
# reaches them too; importing rather than re-implementing is the point.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
from audit_laws_of_ux import LAW_REGISTRY, audit_html  # noqa: E402

from . import __version__ as _VERSION  # noqa: E402

#: One line per law, so a caller (or an agent) knows what it is being told.
#: Kept here rather than in the auditor because it is presentation: the
#: checks themselves need no prose to run.
_LAW_NOTES: dict[str, str] = {
    "hick": "Decision time grows with the number of choices. Flags long menus and option lists.",
    "choice-overload": "Too many comparable options stall a choice entirely. Flags oversized grids of cards.",
    "miller": "Working memory holds about seven items. Flags unbroken runs of digits or long unchunked strings.",
    "jakob": "People expect your site to work like the others they know. Flags unconventional control naming.",
    "fitts": "Time to hit a target falls with its size. Flags interactive elements below the 44 px minimum.",
    "aesthetic-usability": "A tidy interface is perceived as more usable. Flags crowding and inconsistent spacing.",
    "selective-attention": "People miss what looks like an advert. Flags status conveyed by colour alone.",
    "tesler": "Complexity is conserved: what the interface drops, the user carries. Flags raw timestamps and unlocalised values.",
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


@app.get("/health", tags=["meta"], operation_id="health")
def health() -> dict:
    """
    Liveness probe — no dependency check, just proves the app is up.

    Returns
    -------
    dict
        ``{"status": "ok"}``.
    """
    return {"status": "ok"}


@app.get("/v1/laws", tags=["meta"], operation_id="list_laws")
def laws() -> dict:
    """
    The eight laws, each with a one-line note on what it checks.

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


@app.post("/v1/audit", tags=["actions"], operation_id="audit_interface")
def audit(request: AuditRequest) -> dict:
    """
    Audit a string of HTML against the requested laws.

    Parameters
    ----------
    request : AuditRequest
        The markup and which laws to run.

    Returns
    -------
    dict
        ``findings`` (law, severity, line, message) and counts by severity.

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
