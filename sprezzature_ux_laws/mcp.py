"""
sprezzature-ux-laws — Model Context Protocol (MCP) surface.

Adapter that republishes the FastAPI app in :mod:`sprezzature_ux_laws.api`
as MCP tools, so any MCP-aware host (an agent runtime, an IDE integration,
a custom shell) can call ``health``, ``list_laws`` and ``audit_interface``
as first-class tools instead of guessing at a shell command. Uses :mod:`fastapi_mcp` (https://github.com/tadata-org/fastapi_mcp):
one wrapper over the whole existing HTTP surface, so the routes serve both
plain HTTP callers and MCP hosts without being written twice.

Why a wrapper rather than a hand-written server
-----------------------------------------------
A hand-written MCP server would be a second description of the same
surface, free to drift from the routes it claims to mirror — a tool whose
argument names quietly disagree with the API is worse than no tool, because
the disagreement only shows up at call time. Deriving the tools from the
FastAPI signatures means the two cannot disagree: the ``operation_id`` on
each route *is* the tool name, and the Pydantic model *is* the schema.

Why these checks are worth giving an agent
-------------------------------------------
Each finding is a fact about the markup that the agent can point at: a
``<nav>`` with twelve choices, a ``<div>`` acting as a button, a time with
no timezone. An assistant asked "is this interface usable?" can answer with
located findings it computed instead of an impression it formed, and be
wrong in a way that is checkable.

``fastapi-mcp`` is a base dependency since 2026-11-01, so there is no
extra to ask for::

    pip install 'sprezzature-ux-laws'

Then run the MCP server::

    sprezzature-ux-laws-mcp          # entry point (see pyproject)
    # or, equivalently:
    python -m sprezzature_ux_laws.mcp

Usage Example
-------------
>>> # Register the MCP endpoint in your client. It publishes:
>>> #   health / list_laws / audit_interface
>>> # ...with the same argument names as the FastAPI routes.

Author
------
`Warith HARCHAOUI, Ph.D. <https://www.linkedin.com/in/warith-harchaoui/>`_
"""

from __future__ import annotations

import sys

try:
    from fastapi_mcp import FastApiMCP
except ImportError:  # pragma: no cover - dependency guard

    def main(argv: list[str] | None = None) -> None:
        """
        Entry point when fastapi-mcp cannot be imported (a broken install).

        Takes the same ``argv`` as the real entry point and ignores it:
        the two variants are reached through the same console script, so
        a caller that passes arguments must not get a ``TypeError`` from
        the branch that happens to be missing a dependency.

        Says which dependency is missing and stops. A broken install
        needs a one-line fix, not a stack trace.
        """
        print(
            "sprezzature-ux-laws MCP surface could not import fastapi-mcp, which is a "
            "base dependency since 2026-11-01 -- a broken install rather than "
            "a missing extra. Reinstall with: "
            "pip install 'sprezzature-ux-laws'",
            file=sys.stderr,
        )
        sys.exit(1)

else:
    # Reuse the exact same FastAPI app -- MCP is a thin wrapper on top.
    from sprezzature_ux_laws.api import app

    # FastApiMCP mounts an MCP endpoint on the existing FastAPI app; the wrapped
    # instance is kept at module scope so downstream code (tests, ASGI runners)
    # can reach both the FastAPI app and the MCP handler.
    mcp = FastApiMCP(
        app,
        name="sprezzature-ux-laws",
        description=(
            "Sprezzature UX Laws MCP tools: audit an interface against eight laws "
            "of UX — Hick, Miller, Fitts, Jakob, Tesler and friends."
        ),
        include_tags=["meta", "actions"],
    )
    # Newer fastapi-mcp releases split mount() into transport-specific
    # mount_http() (recommended) and mount_sse(); fall back to the legacy
    # mount() on older versions so a range of fastapi-mcp versions still work.
    if hasattr(mcp, "mount_http"):
        mcp.mount_http()
    else:  # pragma: no cover - legacy fastapi-mcp
        mcp.mount()

    def main(argv: list[str] | None = None) -> None:
        """
        Entry point for the ``sprezzature-ux-laws-mcp`` console script.

        Serves the FastAPI app — which carries both the HTTP routes and the
        MCP endpoint — with ``uvicorn``, in single-worker mode. Meant for
        local or container use; behind a real load balancer, run ``uvicorn``
        or ``gunicorn`` directly.

        Arguments are parsed before anything is bound, so ``--help`` answers
        instead of starting a server and hanging.

        Parameters
        ----------
        argv : list of str or None, optional
            Arguments to parse. ``None`` reads ``sys.argv``.
        """
        import os

        import click
        from sprezzature_ux_laws_scripts._click import run_command, sprezzature_command

        default_host = os.environ.get("SPREZZATURE_UX_LAWS_HOST", "127.0.0.1")
        default_port = int(os.environ.get("SPREZZATURE_UX_LAWS_PORT", "8000"))

        @sprezzature_command(
            "sprezzature-ux-laws-mcp",
            help=(
                "Serve the sprezzature-ux-laws MCP tools over HTTP. Every tool is a "
                "route on the same FastAPI app, with the MCP endpoint "
                "mounted beside them."
            ),
            epilog=(
                "Defaults come from SPREZZATURE_UX_LAWS_HOST and "
                "SPREZZATURE_UX_LAWS_PORT when those are set.\n\n"
                "The host defaults to 127.0.0.1: pass --host 0.0.0.0 to "
                "accept connections from outside this machine."
            ),
        )
        @click.option(
            "--host",
            default=default_host,
            help=f"Interface to bind (default: {default_host}).",
        )
        @click.option(
            "--port",
            type=int,
            default=default_port,
            help=f"Port to bind (default: {default_port}).",
        )
        def command(host: str, port: int) -> None:
            """Bind only once the flags have parsed, so --help never starts a server."""
            import uvicorn

            uvicorn.run(app, host=host, port=port, workers=1)

        run_command(command, argv)


if __name__ == "__main__":  # pragma: no cover
    main()
