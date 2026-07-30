"""Tests for sprezzature_ux_laws and its core auditor script."""
from __future__ import annotations

import json
import sys
from pathlib import Path

# The script uses sys.path insertion at import time; mirror that for tests.
SCRIPTS = Path(__file__).resolve().parent.parent / "scripts"
sys.path.insert(0, str(SCRIPTS))


def test_package_imports() -> None:
    """sprezzature_ux_laws is importable with correct metadata."""
    import sprezzature_ux_laws

    assert sprezzature_ux_laws.__version__ == "1.0.0"
    assert sprezzature_ux_laws.__author__ == "Warith Harchaoui"


def test_law_registry_keys() -> None:
    """The registry exposes the expected law slugs."""
    from audit_laws_of_ux import LAW_REGISTRY

    assert "fitts" in LAW_REGISTRY
    assert "hick" in LAW_REGISTRY
    assert len(LAW_REGISTRY) >= 8


def test_fitts_flags_small_button(tmp_path: Path) -> None:
    """A button with no 44 px hit-area class raises a Fitts finding."""
    from audit_laws_of_ux import audit_file

    page = tmp_path / "page.html"
    page.write_text(
        '<!DOCTYPE html><html><body>'
        '<button class="px-4">Go</button>'
        '</body></html>',
        encoding="utf-8",
    )
    findings = audit_file(page, {"fitts"})
    assert any(f.law == "fitts" for f in findings)


def test_clean_button_passes_fitts(tmp_path: Path) -> None:
    """A button with min-h-11 (44 px) produces no Fitts finding."""
    from audit_laws_of_ux import audit_file

    page = tmp_path / "ok.html"
    page.write_text(
        '<!DOCTYPE html><html><body>'
        '<button class="min-h-11 px-4">Go</button>'
        '</body></html>',
        encoding="utf-8",
    )
    findings = audit_file(page, {"fitts"})
    assert not [f for f in findings if f.law == "fitts"]


def test_format_json_is_valid_json() -> None:
    """format_json emits parseable JSON for an empty finding list."""
    from audit_laws_of_ux import format_json

    assert json.loads(format_json([])) == []


def test_discover_finds_html(tmp_path: Path) -> None:
    """discover() collects .html files under a directory target."""
    from audit_laws_of_ux import discover

    (tmp_path / "a.html").write_text("<html></html>", encoding="utf-8")
    (tmp_path / "b.txt").write_text("nope", encoding="utf-8")
    found = discover([tmp_path])
    names = {p.name for p in found}
    assert "a.html" in names
    assert "b.txt" not in names
