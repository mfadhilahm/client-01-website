"""Session 4 Automated Product Check Suite for Nordwerk Industrie-Service (B6).

Implements three distinct automated check families against the Release Candidate (AC-01..AC-08)
without requiring the Software Factory process, LLM provider, or database:
1. Check Family 1 (Content): AC-01, AC-02 (all 3 services N-03..N-05), AC-03 (target groups N-06,
   working approach N-07, no <form> or forbidden invented claims), and N-09 course notice.
2. Check Family 2 (Contact & Navigation): AC-04 ('Anfrage stellen' -> mailto:kontakt@nordwerk.example)
   and AC-05 (<nav> links to #leistungen and #kontakt; all internal #anchor links resolve to existing IDs).
3. Check Family 3 (Local References, Assets & A11y/Responsive): AC-05, AC-06, AC-07 (local asset files exist,
   no external font/tracking URLs, lang="de", <title>, viewport meta, heading hierarchy h1/h2/h3,
   image alt attributes, and :focus/:focus-visible + @media rules in styles.css).
"""
from __future__ import annotations

import unittest
from html.parser import HTMLParser
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
SITE_DIR = REPO_ROOT / "site"
INDEX_HTML = SITE_DIR / "index.html"
STYLES_CSS = SITE_DIR / "styles.css"


class _ReleaseCandidateHTMLInspector(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.html_lang: str | None = None
        self.has_viewport_meta: bool = False
        self.in_title: bool = False
        self.title_chunks: list[str] = []
        self.in_nav: bool = False
        self.nav_links: list[tuple[str, str]] = []
        self.links: list[tuple[str, str]] = []
        self._current_href: str | None = None
        self._current_link_text: list[str] = []
        self._current_link_in_nav: bool = False
        self.element_ids: set[str] = set()
        self.headings: list[tuple[str, str]] = []
        self._current_heading_tag: str | None = None
        self._current_heading_text: list[str] = []
        self.local_asset_refs: list[str] = []
        self.external_asset_refs: list[str] = []
        self.images: list[tuple[str, str | None]] = []
        self.forms_count: int = 0
        self.text_chunks: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attr_map = dict(attrs)
        elem_id = attr_map.get("id")
        if elem_id and elem_id.strip():
            self.element_ids.add(elem_id.strip())

        if tag == "html" and self.html_lang is None:
            self.html_lang = attr_map.get("lang")
        elif tag == "meta":
            if (attr_map.get("name") or "").lower() == "viewport":
                content = attr_map.get("content") or ""
                if "width=device-width" in content:
                    self.has_viewport_meta = True
        elif tag == "title":
            self.in_title = True
        elif tag == "nav":
            self.in_nav = True
        elif tag == "form":
            self.forms_count += 1
        elif tag in ("h1", "h2", "h3"):
            self._current_heading_tag = tag
            self._current_heading_text = []
        elif tag == "a":
            self._current_href = attr_map.get("href") or ""
            self._current_link_text = []
            self._current_link_in_nav = self.in_nav
        elif tag == "link":
            href = (attr_map.get("href") or "").strip()
            if href:
                self._record_asset_ref(href)
        elif tag == "script":
            src = (attr_map.get("src") or "").strip()
            if src:
                self._record_asset_ref(src)
        elif tag == "img":
            src = (attr_map.get("src") or "").strip()
            alt = attr_map.get("alt")
            self.images.append((src, alt))
            if src:
                self._record_asset_ref(src)

    def _record_asset_ref(self, ref: str) -> None:
        if ref.startswith(("http://", "https://", "//")):
            self.external_asset_refs.append(ref)
        elif not ref.startswith(("mailto:", "tel:", "#", "data:")):
            clean_ref = ref.split("?", 1)[0].split("#", 1)[0]
            if clean_ref:
                self.local_asset_refs.append(clean_ref)

    def handle_endtag(self, tag: str) -> None:
        if tag == "title":
            self.in_title = False
        elif tag == "nav":
            self.in_nav = False
        elif tag in ("h1", "h2", "h3") and self._current_heading_tag == tag:
            heading_text = " ".join("".join(self._current_heading_text).split())
            self.headings.append((tag, heading_text))
            self._current_heading_tag = None
            self._current_heading_text = []
        elif tag == "a" and self._current_href is not None:
            label = " ".join("".join(self._current_link_text).split())
            pair = (self._current_href, label)
            self.links.append(pair)
            if self._current_link_in_nav:
                self.nav_links.append(pair)
            self._current_href = None
            self._current_link_text = []
            self._current_link_in_nav = False

    def handle_data(self, data: str) -> None:
        if self.in_title:
            self.title_chunks.append(data)
        if self._current_heading_tag is not None:
            self._current_heading_text.append(data)
        if self._current_href is not None:
            self._current_link_text.append(data)
        cleaned = " ".join(data.split())
        if cleaned:
            self.text_chunks.append(cleaned)


class TestNordwerkSession04ReleaseCandidate(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        if not INDEX_HTML.is_file():
            raise AssertionError(f"Missing product HTML file: {INDEX_HTML}")
        cls.raw_html = INDEX_HTML.read_text(encoding="utf-8")
        cls.inspector = _ReleaseCandidateHTMLInspector()
        cls.inspector.feed(cls.raw_html)
        cls.visible_text = " ".join(cls.inspector.text_chunks)

    def test_family1_required_content_ac01_ac02_ac03(self) -> None:
        """Check Family 1 (Content): AC-01, AC-02 (all 3 services), AC-03 (target groups, approach, guardrails)."""
        self.assertNotIn("TODO_FACTORY_GENERATION", self.raw_html)

        # AC-01: N-01 Company name & N-02 Main statement
        self.assertIn("Nordwerk Industrie-Service", self.visible_text)
        self.assertIn(
            "Praktische Unterstützung für Ihren technischen Betrieb.",
            self.visible_text,
        )

        # AC-02: All three required services (N-03, N-04, N-05)
        required_services = {
            "Wartungsplanung": (
                "Wir strukturieren Wartungsaufgaben und dokumentieren "
                "Zuständigkeiten für kleine technische Betriebe."
            ),
            "Ersatzteilkoordination": (
                "Wir unterstützen bei der Abstimmung von Ersatzteilbedarfen "
                "und Lieferterminen."
            ),
            "Betriebsdokumentation": (
                "Wir bringen technische Unterlagen in eine nachvollziehbare "
                "und nutzbare Struktur."
            ),
        }
        for title, description in required_services.items():
            self.assertIn(
                title,
                self.visible_text,
                f"Missing required AC-02 service title: {title}",
            )
            self.assertIn(
                description,
                self.visible_text,
                f"Missing required AC-02 service description for {title}",
            )

        # AC-03: Both target groups (N-06) and working approach (N-07)
        self.assertIn("Kleine Produktionsbetriebe", self.visible_text)
        self.assertIn("Technische Serviceunternehmen", self.visible_text)
        self.assertIn(
            "Ein fester Ansprechpartner, ein gemeinsam vereinbarter Leistungsumfang "
            "und nachvollziehbare Ergebnisse.",
            self.visible_text,
        )

        # N-09: Course notice
        self.assertIn(
            "Fiktives Unternehmen – Lehrprojekt der HAW Hamburg. "
            "Keine realen Angebote oder Kontaktaufnahme.",
            self.visible_text,
        )

        # Scope guardrails: no <form> and no invented claims (ISO/TÜV, 24/7 SLA, fake references)
        self.assertEqual(
            self.inspector.forms_count,
            0,
            "Contact form (<form>) is out of scope per customer brief.",
        )
        forbidden_claims = ("ISO 9001", "TÜV", "24/7", "Reaktionszeit", "Kundenstimmen")
        for claim in forbidden_claims:
            self.assertNotIn(
                claim.lower(),
                self.visible_text.lower(),
                f"Forbidden unrequested claim detected: {claim}",
            )

    def test_family2_contact_and_navigation_targets_ac04_ac05(self) -> None:
        """Check Family 2 (Contact & Navigation): AC-04 mailto target and AC-05 internal anchor navigation."""
        # AC-04: N-08 mailto link
        self.assertIn(
            ("mailto:kontakt@nordwerk.example", "Anfrage stellen"),
            self.inspector.links,
            f"Expected ('mailto:kontakt@nordwerk.example', 'Anfrage stellen') in {self.inspector.links}",
        )

        # AC-05: Navigation links to services (#leistungen) and contact (#kontakt)
        nav_hrefs = [href for href, _ in self.inspector.nav_links]
        self.assertIn(
            "#leistungen",
            nav_hrefs,
            f"Navigation (<nav>) must link to #leistungen; found {self.inspector.nav_links}",
        )
        self.assertIn(
            "#kontakt",
            nav_hrefs,
            f"Navigation (<nav>) must link to #kontakt; found {self.inspector.nav_links}",
        )

        # Verify every internal anchor href="#..." resolves to an existing element id="..."
        internal_anchors = [
            href for href, _ in self.inspector.links if href.startswith("#")
        ]
        self.assertGreaterEqual(
            len(internal_anchors),
            2,
            "Expected at least two internal anchor links (#leistungen, #kontakt).",
        )
        for anchor in internal_anchors:
            target_id = anchor[1:]
            self.assertTrue(
                target_id and target_id in self.inspector.element_ids,
                f"Broken internal anchor link '{anchor}': no element with id='{target_id}' in index.html",
            )

    def test_family3_local_assets_and_usability_ac05_ac06_ac07(self) -> None:
        """Check Family 3 (Local Assets & A11y/Responsive): AC-05 local files, AC-06 responsive CSS, AC-07 a11y."""
        # AC-07: German language tag, non-empty document title, viewport meta, semantic headings
        self.assertEqual(self.inspector.html_lang, "de")
        doc_title = " ".join("".join(self.inspector.title_chunks).split())
        self.assertTrue(
            len(doc_title) > 0 and "Nordwerk Industrie-Service" in doc_title,
            f"Expected non-empty <title> containing company name, got: {doc_title!r}",
        )
        self.assertTrue(
            self.inspector.has_viewport_meta,
            "Missing <meta name='viewport' content='width=device-width, initial-scale=1.0'> for AC-06.",
        )

        heading_tags = [tag for tag, _ in self.inspector.headings]
        self.assertIn("h1", heading_tags, "Document must contain an <h1> heading.")
        self.assertIn("h2", heading_tags, "Document must contain <h2> section headings.")
        self.assertIn("h3", heading_tags, "Document must contain <h3> service headings.")

        # AC-07: Any <img> element must have a non-empty alt attribute
        for src, alt in self.inspector.images:
            self.assertTrue(
                alt is not None and len(alt.strip()) > 0,
                f"Image '{src}' is missing a non-empty alt attribute (AC-07).",
            )

        # AC-05: No external font/tracking URLs; all local asset references exist in site/
        self.assertEqual(
            self.inspector.external_asset_refs,
            [],
            f"External asset/tracking URLs are not allowed: {self.inspector.external_asset_refs}",
        )
        self.assertIn(
            "styles.css",
            self.inspector.local_asset_refs,
            "site/index.html must reference local stylesheet 'styles.css'.",
        )
        for rel_asset in self.inspector.local_asset_refs:
            asset_path = (SITE_DIR / rel_asset).resolve()
            self.assertTrue(
                asset_path.is_file(),
                f"Referenced local asset does not exist in site/: {rel_asset}",
            )

        # AC-06 & AC-07: Verify styles.css defines visible keyboard focus and responsive @media rules
        self.assertTrue(STYLES_CSS.is_file(), f"Missing stylesheet: {STYLES_CSS}")
        css_text = STYLES_CSS.read_text(encoding="utf-8")
        self.assertTrue(
            ":focus" in css_text and "outline" in css_text,
            "styles.css must define visible keyboard :focus/:focus-visible outline styles (AC-07).",
        )
        self.assertIn(
            "@media",
            css_text,
            "styles.css must include @media responsive layout rules for 375px/1280px viewports (AC-06).",
        )


if __name__ == "__main__":
    unittest.main()
