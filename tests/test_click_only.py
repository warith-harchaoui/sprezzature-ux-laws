"""
Click is the only command-line parser of this package.

The suite settled on click on 2026-10-25 and the front door followed, but
two console scripts kept argparse: ``sprezzature-ux-laws-audit`` (through the
``scripts/_argparse.py`` helper) and ``sprezzature-ux-laws-mcp``. Nothing
failed, so nothing said so. Two checks hold the line now:

* every console script in ``[project.scripts]`` answers ``--help`` with exit 0
  and a click usage line (``Usage:``, capitalised; argparse writes ``usage:``);
* no module of the package, library or scripts, imports argparse.

The second reads the source with :mod:`ast` rather than grepping, so a comment
or a docstring that mentions argparse is not mistaken for an import.

Author
------
Warith HARCHAOUI <warithmetics@deraison.ai>
"""

from __future__ import annotations

import ast
import re
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent

#: ``[project.scripts]`` read with a regex: ``tomllib`` is 3.11+ and the
#: package supports 3.10, where the import would fail collection.
_SECTION = re.compile(r"^\[project\.scripts\]\s*$(.*?)(?=^\[|\Z)", re.M | re.S)
_ENTRY = re.compile(r'^([\w.-]+)\s*=\s*"([\w.]+):(\w+)"', re.M)


def _console_scripts() -> list[tuple[str, str, str]]:
    """Every (command, module, function) the manifest declares."""
    text = (REPO_ROOT / "pyproject.toml").read_text(encoding="utf-8")
    section = _SECTION.search(text)
    return _ENTRY.findall(section.group(1)) if section else []


def test_the_manifest_declares_console_scripts() -> None:
    """The parametrised case below means nothing over an empty list."""
    assert len(_console_scripts()) >= 3


@pytest.mark.parametrize(
    ("command", "module", "function"),
    _console_scripts(),
    ids=[c for c, _, _ in _console_scripts()],
)
def test_every_console_script_answers_help_with_click(
    command: str, module: str, function: str
) -> None:
    """``--help`` exits 0 and prints a click usage line naming the command."""
    found = shutil.which(command)
    if found is not None:
        done = subprocess.run([found, "--help"], capture_output=True, text=True)
    else:
        code = (
            "import sys\n"
            f"sys.argv = [{command!r}, '--help']\n"
            f"from {module} import {function}\n"
            f"raise SystemExit({function}())\n"
        )
        done = subprocess.run(
            [sys.executable, "-c", code], capture_output=True, text=True, cwd=REPO_ROOT
        )
    assert done.returncode == 0, done.stderr
    assert done.stdout.startswith(f"Usage: {command} "), (
        f"{command} --help does not print a click usage line:\n{done.stdout[:200]}"
    )


def _imports_argparse(path: Path) -> bool:
    """Whether ``path`` imports argparse anywhere, at any depth."""
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    for node in ast.walk(tree):
        if isinstance(node, ast.Import) and any(
            alias.name.split(".")[0] == "argparse" for alias in node.names
        ):
            return True
        if isinstance(node, ast.ImportFrom) and (node.module or "").split(".")[0] == "argparse":
            return True
    return False


def test_no_module_of_the_package_imports_argparse() -> None:
    """The library and the scripts shipped in the wheel parse with click only."""
    sources = sorted((REPO_ROOT / "sprezzature_ux_laws").rglob("*.py")) + sorted(
        (REPO_ROOT / "scripts").rglob("*.py")
    )
    assert sources
    offenders = [str(p.relative_to(REPO_ROOT)) for p in sources if _imports_argparse(p)]
    assert not offenders, f"argparse is imported by {offenders}"
