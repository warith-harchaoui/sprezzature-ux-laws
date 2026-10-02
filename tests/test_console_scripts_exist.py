"""
Every command the help text names has to be a command you can run.

``audit_laws_of_ux.py`` built its parser with ``prog="sprezzature-ux-laws-audit"``
and ``pyproject.toml`` installed exactly one console script,
``sprezzature-ux-laws-mcp``. So the auditor, which is the reason this package
exists, printed a usage line naming a command that did not exist, and the
README told readers to run ``python scripts/audit_laws_of_ux.py``, a path that
is there in a clone and gone in a wheel. Someone who ran
``pip install sprezzature-ux-laws`` could start the MCP server and reach the
auditor no other way.

The same shape of mistake has now been found three times across the suite
(``caption_diarize.py`` in sprezzature-audio named itself after a console
script that did not exist; its two installers still do). Nothing crashes, so
no test caught it: the program runs fine, it just tells you to type something
that is not there.

This check derives both sides from the files rather than from a list kept by
hand, so a script added later is covered without anyone remembering to add it.

Author
------
Warith HARCHAOUI <warith.harchaoui@gmail.com>
"""

from __future__ import annotations

import re
from pathlib import Path

import pytest
import tomllib

REPO_ROOT = Path(__file__).resolve().parent.parent
SCRIPTS_DIR = REPO_ROOT / "scripts"

#: A ``prog=`` or Click ``name=`` argument spelling a suite command name.
_PROG_RE = re.compile(r'(?:prog|name)\s*=\s*["\'](sprezzature[a-z0-9-]*)["\']')


def _declared_console_scripts() -> set[str]:
    """The names ``pip install`` actually puts on a user's PATH."""
    with (REPO_ROOT / "pyproject.toml").open("rb") as handle:
        return set(tomllib.load(handle)["project"].get("scripts", {}))


def _advertised_names() -> list[tuple[str, str]]:
    """``(script file name, command it tells the reader to type)`` pairs."""
    out: list[tuple[str, str]] = []
    for path in sorted(SCRIPTS_DIR.glob("*.py")):
        text = path.read_text(encoding="utf-8", errors="replace")
        for match in _PROG_RE.finditer(text):
            out.append((path.name, match.group(1)))
    return out


@pytest.mark.parametrize(
    "script_name,advertised",
    _advertised_names(),
    ids=lambda value: value,
)
def test_the_command_the_help_names_is_a_command_that_exists(
    script_name: str, advertised: str
) -> None:
    """A ``prog=`` must match a console script pyproject.toml installs."""
    declared = _declared_console_scripts()
    assert advertised in declared, (
        f"{script_name} tells the reader to run {advertised!r}, which "
        f"[project.scripts] does not install. Installed: {sorted(declared)}. "
        f"Either declare it, or name the script after something that exists."
    )


def test_every_console_script_points_at_something_importable() -> None:
    """The other direction: no entry point naming a module that is not there.

    Skipped on a checkout that was never installed. The mapped script package
    (``..._scripts``) only exists once pip has read ``[tool.setuptools]
    package-dir``, so on a bare clone this would fail for the environment
    rather than for the code. CI installs the package first, which is where
    the check is meant to bite.
    """
    import importlib
    import importlib.util

    with (REPO_ROOT / "pyproject.toml").open("rb") as handle:
        scripts = tomllib.load(handle)["project"].get("scripts", {})

    for name, target in sorted(scripts.items()):
        module_name, _, attribute = target.partition(":")
        if importlib.util.find_spec(module_name.split(".")[0]) is None:
            pytest.skip(
                f"{module_name.split('.')[0]} is not importable here: this "
                f"checkout is not installed (pip install -e .)."
            )
        module = importlib.import_module(module_name)
        assert hasattr(module, attribute), (
            f"console script {name} points at {target}, but {module_name} has "
            f"no attribute {attribute!r}."
        )
