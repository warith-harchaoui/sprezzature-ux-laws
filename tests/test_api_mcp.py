"""
Tests for the HTTP and MCP surfaces.

The law checks themselves are covered by ``test_ux_laws.py``; what these
guard is the wiring — a route that stops matching its model, an
``operation_id`` renamed so an agent's tool vanishes, or a fastapi-mcp
upgrade that moves ``mount()``. All three fail quietly rather than loudly.

Author
------
`Warith HARCHAOUI, Ph.D. <https://www.linkedin.com/in/warith-harchaoui/>`_
"""

from __future__ import annotations

import pytest

pytest.importorskip("fastapi")
from fastapi.testclient import TestClient  # noqa: E402

from sprezzature_ux_laws.api import app  # noqa: E402

client = TestClient(app)


def test_health() -> None:
    """The liveness probe answers."""
    assert client.get("/health").json() == {"status": "ok"}


def test_all_eight_laws_are_advertised() -> None:
    """Each law is listed with a note on what it checks."""
    laws = client.get("/v1/laws").json()["laws"]
    assert len(laws) == 8
    assert {"hick", "fitts", "miller", "tesler"} <= {law["id"] for law in laws}
    assert all(law["checks"] for law in laws), "a law with no note is a law nobody can act on"


def test_small_button_trips_fitts() -> None:
    """A target below the 44 px minimum is the canonical Fitts violation."""
    result = client.post(
        "/v1/audit", json={"html": '<button class="p-1">Go</button>'}
    ).json()
    assert any(f["law"] == "fitts" for f in result["findings"])


def test_tidy_markup_reports_nothing() -> None:
    """A checker that only ever finds faults proves nothing."""
    html = '<button class="min-h-11 focus-visible:ring-2">Go</button>'
    result = client.post("/v1/audit", json={"html": html}).json()
    assert result["findings"] == [], result["findings"]


def test_law_subset_is_honoured() -> None:
    """Asking for one law runs that law and no other."""
    html = '<button class="p-1">Go</button>'
    only_fitts = client.post(
        "/v1/audit", json={"html": html, "laws": ["fitts"]}
    ).json()
    assert {f["law"] for f in only_fitts["findings"]} <= {"fitts"}


def test_unknown_law_is_rejected_not_ignored() -> None:
    """
    Silently dropping an unknown slug would return a clean report for
    checks that never ran — the worst possible answer.
    """
    response = client.post(
        "/v1/audit", json={"html": "<p>x</p>", "laws": ["gravity"]}
    )
    assert response.status_code == 400
    assert "gravity" in response.json()["detail"]


def test_openapi_names_every_tool() -> None:
    """Each route carries an operation_id: that *is* the MCP tool name."""
    paths = client.get("/openapi.json").json()["paths"]
    for path, methods in paths.items():
        for verb, spec in methods.items():
            assert "operationId" in spec, f"{verb.upper()} {path} has no operation_id"


def test_mcp_mounts_and_publishes_the_tools() -> None:
    """The MCP endpoint exists and carries the expected tool names."""
    pytest.importorskip("fastapi_mcp")
    from sprezzature_ux_laws.mcp import mcp

    assert mcp is not None
    mounted = {getattr(r, "path", "") for r in app.routes}
    assert any(p.startswith("/mcp") for p in mounted), sorted(mounted)
    assert "audit_interface" in {t.name for t in mcp.tools}


def _documented_routes(app):
    """This package's own tools -- fastapi-mcp mounts its transport route on
    the same app, and that one is not ours to document."""
    return [
        route
        for route in app.routes
        if getattr(route, "operation_id", None)
        and not getattr(route, "path", "").startswith("/mcp")
    ]


def test_every_tool_has_a_written_summary() -> None:
    """The first line an MCP host shows is FastAPI's `summary`, and its
    default is the function name title-cased: `cvd` became "Cvd", `wer`
    became "Wer". An agent choosing between tools from several servers reads
    those headlines and little else, so each has to be a written phrase
    saying what the tool does -- not a restatement of the Python identifier.
    """
    from sprezzature_ux_laws.api import app

    for route in _documented_routes(app):
        summary = (getattr(route, "summary", "") or "").strip()
        assert summary, f"{route.operation_id}: no summary, so the headline is a function name"
        derived = getattr(route, "name", "").replace("_", " ").title()
        assert summary != derived, (
            f"{route.operation_id}: summary {summary!r} is FastAPI's default (the "
            f"function name title-cased). Write one that says what the tool does."
        )
        assert " " in summary and len(summary) > 15, (
            f"{route.operation_id}: summary {summary!r} is too terse to route on."
        )


def test_every_tool_says_when_to_call_it() -> None:
    """A description that only restates the summary does not help an agent
    choose. Each route's docstring carries the deciding context: when to
    reach for it, what it needs first, or what it must not be used for.
    """
    from sprezzature_ux_laws.api import app

    for route in _documented_routes(app):
        description = (getattr(route, "description", "") or "").strip()
        assert len(description) > 120, (
            f"{route.operation_id}: description is {len(description)} chars. Say when "
            f"to call it, not just what it is."
        )
