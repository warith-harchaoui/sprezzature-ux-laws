FROM python:3.11-slim

WORKDIR /app

COPY . .

# The API, and the MCP endpoint mounted beside it. fastapi, uvicorn and
# fastapi-mcp are base dependencies since 2026-11-01, so a plain install
# serves what the CMD below names; there is no extra to ask for.
RUN pip install --no-cache-dir "."

EXPOSE 8000

# Serve what the image was built for. A CMD of `--help` is a container that
# starts, prints and exits — which looks like it works and does nothing.
#
# The MCP server, not bare uvicorn on api:app: mcp.py mounts /mcp on the same
# FastAPI app as the HTTP routes, so this one process on one port answers
# both /v1/... and /mcp. `uvicorn sprezzature_ux_laws.api:app` served the
# routes only, because nothing imported mcp.py to mount the endpoint.
# Override with the command line:
#
#   docker run --rm -v "$PWD:/work" IMAGE sprezzature-ux-laws-audit /work/index.html
CMD ["sprezzature-ux-laws-mcp", "--host", "0.0.0.0", "--port", "8000"]
