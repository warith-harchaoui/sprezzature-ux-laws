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


# ── Hick's Law ──────────────────────────────────────────────────────────────


def test_hick_flags_overcrowded_nav(tmp_path: Path) -> None:
    """A <nav> with 8 top-level links raises a Hick finding (> 7 threshold)."""
    from audit_laws_of_ux import audit_file

    links = "".join(f'<a href="/p{i}">Item {i}</a>' for i in range(8))
    page = tmp_path / "nav.html"
    page.write_text(
        f"<!DOCTYPE html><html><body><nav>{links}</nav></body></html>",
        encoding="utf-8",
    )
    findings = audit_file(page, {"hick"})
    hick = [f for f in findings if f.law == "hick"]
    assert len(hick) == 1
    assert hick[0].severity == "error"


def test_hick_allows_seven_item_nav(tmp_path: Path) -> None:
    """A <nav> with exactly 7 top-level links stays under the threshold."""
    from audit_laws_of_ux import audit_file

    links = "".join(f'<a href="/p{i}">Item {i}</a>' for i in range(7))
    page = tmp_path / "nav_ok.html"
    page.write_text(
        f"<!DOCTYPE html><html><body><nav>{links}</nav></body></html>",
        encoding="utf-8",
    )
    findings = audit_file(page, {"hick"})
    assert not [f for f in findings if f.law == "hick"]


# ── Miller's Law ────────────────────────────────────────────────────────────


def test_miller_flags_long_digit_bearing_run(tmp_path: Path) -> None:
    """An unbroken run of >= 8 alphanumerics with a digit raises a Miller finding."""
    from audit_laws_of_ux import audit_file

    page = tmp_path / "miller.html"
    page.write_text(
        "<!DOCTYPE html><html><body>"
        "<p>Your order reference is AB1234567X, keep it safe.</p>"
        "</body></html>",
        encoding="utf-8",
    )
    findings = audit_file(page, {"miller"})
    miller = [f for f in findings if f.law == "miller"]
    assert len(miller) == 1
    assert "AB1234567X" in miller[0].message


def test_miller_ignores_pure_alphabetic_word(tmp_path: Path) -> None:
    """A long pure-alphabetic word (ordinary English) is not flagged."""
    from audit_laws_of_ux import audit_file

    page = tmp_path / "miller_ok.html"
    page.write_text(
        "<!DOCTYPE html><html><body>"
        "<p>Our collaborators appreciate the implementation.</p>"
        "</body></html>",
        encoding="utf-8",
    )
    findings = audit_file(page, {"miller"})
    assert not [f for f in findings if f.law == "miller"]


# ── Choice Overload ─────────────────────────────────────────────────────────


def test_choice_overload_flags_wide_pricing_grid(tmp_path: Path) -> None:
    """A pricing grid with 5 column children raises a Choice-Overload finding."""
    from audit_laws_of_ux import audit_file

    cols = "".join(f'<article>Plan {i}</article>' for i in range(5))
    page = tmp_path / "pricing.html"
    page.write_text(
        f'<!DOCTYPE html><html><body>'
        f'<section class="pricing grid grid-cols-5">{cols}</section>'
        f"</body></html>",
        encoding="utf-8",
    )
    findings = audit_file(page, {"choice-overload"})
    co = [f for f in findings if f.law == "choice-overload"]
    assert len(co) == 1
    assert co[0].severity == "warning"


def test_choice_overload_allows_four_column_grid(tmp_path: Path) -> None:
    """A pricing grid with exactly 4 columns stays under the threshold."""
    from audit_laws_of_ux import audit_file

    cols = "".join(f'<article>Plan {i}</article>' for i in range(4))
    page = tmp_path / "pricing_ok.html"
    page.write_text(
        f'<!DOCTYPE html><html><body>'
        f'<section class="pricing grid grid-cols-4">{cols}</section>'
        f"</body></html>",
        encoding="utf-8",
    )
    findings = audit_file(page, {"choice-overload"})
    assert not [f for f in findings if f.law == "choice-overload"]


# ── Selective Attention ─────────────────────────────────────────────────────


def test_selective_attention_flags_colour_only_status(tmp_path: Path) -> None:
    """A status <span> using colour alone (no word, no icon) raises a finding."""
    from audit_laws_of_ux import audit_file

    page = tmp_path / "status.html"
    page.write_text(
        '<!DOCTYPE html><html><body>'
        '<span class="text-red-700">3.2</span>'
        "</body></html>",
        encoding="utf-8",
    )
    findings = audit_file(page, {"selective-attention"})
    sel = [f for f in findings if f.law == "selective-attention"]
    assert len(sel) == 1
    assert sel[0].severity == "warning"


def test_selective_attention_allows_status_word(tmp_path: Path) -> None:
    """A status <span> whose text names the status is not flagged."""
    from audit_laws_of_ux import audit_file

    page = tmp_path / "status_ok.html"
    page.write_text(
        '<!DOCTYPE html><html><body>'
        '<span class="text-red-700">Error</span>'
        "</body></html>",
        encoding="utf-8",
    )
    findings = audit_file(page, {"selective-attention"})
    assert not [f for f in findings if f.law == "selective-attention"]


def test_selective_attention_allows_icon_child(tmp_path: Path) -> None:
    """A status <span> that wraps an <svg> icon has a second channel."""
    from audit_laws_of_ux import audit_file

    page = tmp_path / "status_icon.html"
    page.write_text(
        '<!DOCTYPE html><html><body>'
        '<span class="text-red-700"><svg></svg>3.2</span>'
        "</body></html>",
        encoding="utf-8",
    )
    findings = audit_file(page, {"selective-attention"})
    assert not [f for f in findings if f.law == "selective-attention"]


# ── Tesler's Law ─────────────────────────────────────────────────────────────


def test_tesler_flags_bare_time(tmp_path: Path) -> None:
    """A plain HH:MM with no timezone token nearby raises a Tesler finding."""
    from audit_laws_of_ux import audit_file

    page = tmp_path / "time.html"
    page.write_text(
        "<!DOCTYPE html><html><body>"
        "<p>The meeting starts at 14:30 sharp.</p>"
        "</body></html>",
        encoding="utf-8",
    )
    findings = audit_file(page, {"tesler"})
    tesler = [f for f in findings if f.law == "tesler"]
    assert len(tesler) == 1


def test_tesler_allows_time_with_named_zone(tmp_path: Path) -> None:
    """A HH:MM with a UTC token nearby is not flagged."""
    from audit_laws_of_ux import audit_file

    page = tmp_path / "time_ok.html"
    page.write_text(
        "<!DOCTYPE html><html><body>"
        "<p>The meeting starts at 14:30 UTC sharp.</p>"
        "</body></html>",
        encoding="utf-8",
    )
    findings = audit_file(page, {"tesler"})
    assert not [f for f in findings if f.law == "tesler"]


def test_tesler_allows_compact_zulu_suffix(tmp_path: Path) -> None:
    """Regression: 12:34Z (Zulu glued to the timestamp) must not be flagged.

    RE_TZ_TOKEN's ``\\bZ\\b`` alternative never matches here because ``4``
    and ``Z`` are both word characters, so no ``\\b`` boundary exists
    between them; the ``(?<=\\d)Z\\b`` alternative added alongside it
    covers exactly this compact ISO-8601 form.
    """
    from audit_laws_of_ux import audit_file

    page = tmp_path / "time_zulu.html"
    page.write_text(
        "<!DOCTYPE html><html><body>"
        "<p>Deploy window opens at 12:34Z sharp.</p>"
        "</body></html>",
        encoding="utf-8",
    )
    findings = audit_file(page, {"tesler"})
    assert not [f for f in findings if f.law == "tesler"]


# ── --fix mode ────────────────────────────────────────────────────────────


def test_fix_mode_applies_fitts_and_au_and_is_sane(tmp_path: Path) -> None:
    """--fix (via fix_file) repairs Fitts + Aesthetic-Usability findings.

    Builds a button with neither a 44px hit-area class nor a focus ring,
    runs the live fixer, and asserts: (1) at least one edit was applied,
    (2) re-auditing the fixed file shows no more Fitts/AU findings, and
    (3) the output HTML is still well-formed enough to keep the button
    text intact (a sanity check that the fixer didn't mangle the markup).
    """
    from audit_laws_of_ux import audit_file, fix_file

    page = tmp_path / "fixme.html"
    page.write_text(
        '<!DOCTYPE html><html><body>'
        '<button class="px-4">Go</button>'
        "</body></html>",
        encoding="utf-8",
    )
    applied, skipped, remaining = fix_file(
        page, {"fitts", "aesthetic-usability"}
    )
    assert applied >= 2  # min-h-11 + the three focus-ring tokens
    assert skipped == 0
    assert not remaining

    fixed_text = page.read_text(encoding="utf-8")
    assert "Go</button>" in fixed_text
    assert "min-h-11" in fixed_text
    assert "focus-visible:ring-2" in fixed_text

    # Re-auditing directly (not just trusting fix_file's own return value)
    # confirms the write actually landed on disk.
    post_findings = audit_file(page, {"fitts", "aesthetic-usability"})
    assert not post_findings


def test_fix_mode_is_idempotent(tmp_path: Path) -> None:
    """A second --fix pass on an already-fixed file applies zero edits."""
    from audit_laws_of_ux import fix_file

    page = tmp_path / "fixme_twice.html"
    page.write_text(
        '<!DOCTYPE html><html><body>'
        '<button class="px-4">Go</button>'
        "</body></html>",
        encoding="utf-8",
    )
    fix_file(page, {"fitts", "aesthetic-usability"})
    applied_again, _, remaining_again = fix_file(
        page, {"fitts", "aesthetic-usability"}
    )
    assert applied_again == 0
    assert not remaining_again


def test_fix_mode_dry_run_does_not_write(tmp_path: Path) -> None:
    """--fix --dry-run reports what would change without touching disk."""
    from audit_laws_of_ux import fix_file

    page = tmp_path / "dry.html"
    original = '<!DOCTYPE html><html><body><button class="px-4">Go</button></body></html>'
    page.write_text(original, encoding="utf-8")
    applied, skipped, remaining = fix_file(
        page, {"fitts", "aesthetic-usability"}, dry_run=True
    )
    assert applied >= 2
    assert remaining  # dry-run reports the pre-fix findings, unresolved
    assert page.read_text(encoding="utf-8") == original


def test_fix_mode_reports_unfixable_findings_as_skipped(tmp_path: Path) -> None:
    """Hick has no fixer: --fix leaves it in place and counts it as skipped."""
    from audit_laws_of_ux import fix_file

    links = "".join(f'<a href="/p{i}">Item {i}</a>' for i in range(8))
    page = tmp_path / "unfixable.html"
    page.write_text(
        f"<!DOCTYPE html><html><body><nav>{links}</nav></body></html>",
        encoding="utf-8",
    )
    applied, skipped, remaining = fix_file(page, {"hick"})
    assert applied == 0
    assert skipped == 1
    assert any(f.law == "hick" for f in remaining)
