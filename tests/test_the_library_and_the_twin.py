"""
The two surfaces this package did not have: a library and a click twin.

Until 1.2.0, `import sprezzature_ux_laws` gave you a version string. The
auditor was reachable from a command line, from HTTP and from an agent, and
not from Python — which is the one place a static HTML check is most obviously
useful, inside somebody else's build step. Worse, the package's own HTTP
surface reached the checks by inserting `scripts/` on `sys.path` and importing
`audit_laws_of_ux` by bare name: it worked, and it made an HTTP surface depend
on a directory layout.

These tests hold the shape of the fix rather than the behaviour of the
auditor, which `test_audit_laws_of_ux.py` already covers:

- the library exports the names every other surface reads, and they work;
- the click twin offers exactly the flags the argparse one does;
- the twin refuses politely when click is not installed, checked by actually
  hiding click rather than by reading the source.

That last one has teeth. The auditor declares **no** dependencies, which is
what makes it cheap enough for a pre-commit hook. A twin importing click at
module load would end that silently — the failure arrives at the console
script, not at the install.

Author
------
Warith HARCHAOUI <warithmetics@deraison.ai>
"""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

import sprezzature_ux_laws as ux

REPO_ROOT = Path(__file__).resolve().parent.parent

# Blocking an import from a subprocess needs `find_spec`, not `find_module`:
# the legacy finder API was removed in Python 3.12, so a blocker written that
# way is simply never consulted — the module imports normally and the test
# passes by not testing anything. The colours package had exactly that bug in
# the first version of this check.
_HIDE_CLICK = (
    "import sys\n"
    "class Blocked:\n"
    "    def find_spec(self, name, path=None, target=None):\n"
    "        if name == 'click':\n"
    "            raise ImportError('click is not installed')\n"
    "        return None\n"
    "sys.meta_path.insert(0, Blocked())\n"
)


def _without_click(program: str) -> subprocess.CompletedProcess[str]:
    """Run a snippet in a subprocess where importing click fails."""
    return subprocess.run(
        [sys.executable, "-c", _HIDE_CLICK + program],
        capture_output=True,
        text=True,
        cwd=REPO_ROOT,
    )


# ── The library ────────────────────────────────────────────────────────────


def test_the_library_exports_what_the_other_surfaces_use() -> None:
    """These names are the contract; every surface reads them from here."""
    for name in (
        "audit_html",
        "audit_file",
        "fix_file",
        "Finding",
        "Walker",
        "Element",
        "LAW_REGISTRY",
        "LAWS",
        "FITTS_FIX_TOKEN",
    ):
        assert hasattr(ux, name), f"{name} is not on the library surface"
        assert name in ux.__all__, f"{name} works but is not in __all__"


def test_laws_is_the_registry_in_registry_order() -> None:
    """A second list of law names would be free to drift from the first."""
    assert ux.LAWS == tuple(ux.LAW_REGISTRY)
    assert "hick" in ux.LAWS


def test_auditing_a_string_works_from_the_library_alone() -> None:
    """The point of the surface: no file, no server, no command line."""
    crowded = "<nav>" + '<a href="/">x</a>' * 12 + "</nav>"
    findings = ux.audit_html(crowded)
    assert any(f.law == "hick" for f in findings), (
        "twelve links in a nav is the textbook Hick's Law finding"
    )
    for finding in findings:
        assert finding.law in ux.LAW_REGISTRY


def test_a_subset_of_laws_is_honoured() -> None:
    """`laws=` has to actually narrow, or the HTTP surface's filter is a lie."""
    crowded = "<nav>" + '<a href="/">x</a>' * 12 + "</nav>"
    only_jakob = ux.audit_html(crowded, laws={"jakob"})
    assert all(f.law == "jakob" for f in only_jakob)


def test_auditing_a_file_needs_nothing_but_the_file() -> None:
    """`audit_file(path)` runs every law, like the command line with no --only.

    It had no default while `audit_html`, the function it wraps, did. So the
    file entry point -- the one a caller reaches for first, and the one the
    sibling repository's site guard tried to call -- was strictly harder to
    call than the string entry point behind it, and demanded a subset of laws
    from a caller who wants all of them.
    """
    import tempfile

    crowded = "<nav>" + '<a href="/">x</a>' * 12 + "</nav>"
    with tempfile.TemporaryDirectory() as tmp:
        page = Path(tmp) / "crowded.html"
        page.write_text(crowded, encoding="utf-8")
        findings = ux.audit_file(page)
        narrowed = ux.audit_file(page, {"jakob"})
    assert any(f.law == "hick" for f in findings), (
        "audit_file with no laws= ran a narrower set than every law"
    )
    assert all(f.law == "jakob" for f in narrowed), (
        "passing laws= to audit_file no longer narrows"
    )


def test_the_http_surface_reads_the_library_not_a_directory() -> None:
    """The sys.path insert is gone, and must not come back.

    It is not a style point: with it, `sprezzature_ux_laws.api` imports
    correctly from a checkout and from a wheel for two different reasons, and
    only one of them is a package.
    """
    source = (REPO_ROOT / "sprezzature_ux_laws" / "api.py").read_text(
        encoding="utf-8"
    )
    assert "sys.path.insert" not in source
    assert "from audit_laws_of_ux import" not in source


# ── The click twin ─────────────────────────────────────────────────────────


def test_the_twin_offers_every_flag_the_argparse_front_door_does() -> None:
    """A flag on one front door and not the other is the failure to prevent."""
    from sprezzature_ux_laws.cli_click import main as click_main

    click_flags = {
        opt.lstrip("-").replace("-", "_")
        for param in click_main.params
        for opt in getattr(param, "opts", [])
        if opt.startswith("--")
    }
    source = (
        REPO_ROOT / "scripts" / "audit_laws_of_ux.py"
    ).read_text(encoding="utf-8")
    argparse_flags = {
        flag.lstrip("-").replace("-", "_")
        for flag in re.findall(r'add_argument\(\s*"(--[a-z-]+)"', source)
    }
    missing = argparse_flags - click_flags
    assert not missing, f"the click twin is missing {sorted(missing)}"


def test_both_front_doors_are_declared_as_console_scripts() -> None:
    """A front door nobody can type is not a front door."""
    pyproject = (REPO_ROOT / "pyproject.toml").read_text(encoding="utf-8")
    section = re.search(
        r"^\[project\.scripts\]\s*$(.*?)(?=^\[|\Z)", pyproject, re.M | re.S
    )
    assert section
    for name in ("sprezzature-ux-laws-audit", "sprezzature-ux-laws"):
        assert re.search(rf"^{re.escape(name)}\s*=", section.group(1), re.M), name


def test_click_is_an_extra_and_not_a_dependency() -> None:
    """The auditor's zero dependencies are the reason it is worth reaching for."""
    pyproject = (REPO_ROOT / "pyproject.toml").read_text(encoding="utf-8")
    base = re.search(r"^dependencies\s*=\s*\[(.*?)\]", pyproject, re.M | re.S)
    assert base and "click" not in base.group(1)
    assert re.search(r"^click\s*=\s*\[", pyproject, re.M), (
        "the twin's help tells the reader to install [click]"
    )


def test_the_twin_refuses_politely_when_click_is_missing() -> None:
    """A bare install must get a sentence, not a traceback."""
    done = _without_click(
        "from sprezzature_ux_laws.cli_click import main\nsys.exit(main())\n"
    )
    assert done.returncode == 1, done.stderr
    assert "sprezzature-ux-laws[click]" in done.stderr
    assert "sprezzature-ux-laws-audit" in done.stderr, (
        "the refusal has to point at the front door that needs nothing"
    )
    assert "Traceback" not in done.stderr


def test_the_refusal_and_the_real_command_agree_on_their_signature() -> None:
    """Two conditional definitions that disagree are a trap.

    A caller who imports ``main`` and passes an argv gets a TypeError on the
    machine where click is missing and nowhere else — the hardest kind of bug
    to be told about, because the person who hits it has the broken install
    and you have the working one.
    """
    done = _without_click(
        "import inspect\n"
        "from sprezzature_ux_laws.cli_click import main\n"
        "print(list(inspect.signature(main).parameters))\n"
    )
    assert done.returncode == 0, done.stderr
    assert done.stdout.strip() == "['argv']"


def test_the_library_imports_with_no_click_anywhere() -> None:
    """`import sprezzature_ux_laws` must not need the twin's extra.

    In a subprocess, because by the time the suite is running click is
    importable and this is a question about a machine where it is not.
    """
    done = _without_click(
        "import sprezzature_ux_laws as ux\n"
        "print(len(ux.audit_html('<button>Go</button>')) >= 0)\n"
    )
    assert done.returncode == 0, done.stderr
    assert done.stdout.strip() == "True"
