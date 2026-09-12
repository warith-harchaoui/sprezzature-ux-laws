"""
Tests for the HTTP and MCP surfaces.

The law checks themselves are covered by ``test_ux_laws.py``; what these
guard is the wiring — a route that stops matching its model, an
``operation_id`` renamed so an agent's tool vanishes, or a fastapi-mcp
upgrade that moves ``mount()``. All three fail quietly rather than loudly.

Author
------
`Warith Harchaoui, Ph.D. <https://www.linkedin.com/in/warith-harchaoui/>`_
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
    assert {"hick", "fitts", "miller", "tesler"} <= {l["id"] for l in laws}
    assert all(l["checks"] for l in laws), "a law with no note is a law nobody can act on"


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
