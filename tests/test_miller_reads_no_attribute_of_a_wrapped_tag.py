"""
Miller's rule reads the text a reader sees, not the attributes of a wrapped tag.

The rule worked line by line: it blanked four attributes (``class``, ``id``,
``href``, ``src``) and then removed each ``<…>`` that opened and closed on the
same line. A tag written over several lines escaped the second step, and every
other attribute on its continuation lines was read as visible text. The French
figure gallery of sprezzature.ai was flagged for ``surface3d``, a file name
inside ``data-src-academic``, on 2026-11-16, while the English page with the
same names passed because its tags sit on one line each.
"""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def _engine():
    spec = importlib.util.spec_from_file_location("_ux_wrap", ROOT / "scripts" / "audit_laws_of_ux.py")
    mod = importlib.util.module_from_spec(spec)
    sys.modules["_ux_wrap"] = mod
    spec.loader.exec_module(mod)
    return mod


PAGE = """<!doctype html><html lang="fr"><body><main>
<button type="button"
  class="zoom"
  aria-label="Agrandir : Surface 3D" data-src="fr/surface3d.svg" data-src-academic="fr/academic/surface3d.svg"
  data-alt="Surface 3D">
  <img src="fr/surface3d.png" data-src-academic="fr/academic/surface3d.png" width="900"
    alt="Surface 3D" loading="lazy">
</button>
<p>Commande AB12CD34EF56 à rappeler.</p>
</main></body></html>
"""


def test_a_wrapped_tag_hides_its_attributes(tmp_path: Path) -> None:
    page = tmp_path / "page.html"
    page.write_text(PAGE, encoding="utf-8")
    runs = [f.message for f in _engine().audit_file(page) if f.law == "miller"]
    assert not any("surface3d" in r for r in runs), runs


def test_a_real_code_in_the_text_is_still_found(tmp_path: Path) -> None:
    """The fix must not blind the rule: the order number in the paragraph is visible."""
    page = tmp_path / "page.html"
    page.write_text(PAGE, encoding="utf-8")
    runs = [f.message for f in _engine().audit_file(page) if f.law == "miller"]
    assert any("AB12CD34EF56" in r for r in runs), runs
