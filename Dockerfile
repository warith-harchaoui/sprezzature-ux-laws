FROM python:3.11-slim

WORKDIR /app

COPY . .

# The API, and the MCP endpoint mounted beside it. A plain `pip install .`
# built an image that could not serve the thing its own CMD named: fastapi and
# uvicorn live behind the `api` extra precisely so that nobody installing the
# library pays for them, so an image that serves has to ask for it.
RUN pip install --no-cache-dir ".[api,mcp]"

EXPOSE 8000

# Serve what the image was built for. A CMD of `--help` is a container that
# starts, prints and exits — which looks like it works and does nothing.
# Override with the command line:
#
#   docker run --rm -v "$PWD:/work" IMAGE sprezzature-ux-laws-audit /work/index.html
CMD ["uvicorn", "sprezzature_ux_laws.api:app", "--host", "0.0.0.0", "--port", "8000"]
