"""Automated product checks for Nordwerk Industrie-Service (Session 3 slice).

Verifies AC-01, AC-02 (first service N-03), AC-04, and B6 scope guardrails
without requiring the Software Factory process, LLM, or database.
"""
from __future__ import annotations

import unittest
from html.parser import HTMLParser
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
INDEX_HTML = REPO_ROOT / "site" / "index.html"


class _HTMLInspector(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.html_lang: str | None = None
        self.links: list[tuple[str, str]] = []
        self._current_href: str | None = None
        self._current_link_text: list[str] = []
        self.text_chunks: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attr_map = dict(attrs)
        if tag == "html" and self.html_lang is None:
            self.html_lang = attr_map.get("lang")
        if tag == "a":
            self._current_href = attr_map.get("href") or ""
            self._current_link_text = []

    def handle_endtag(self, tag: str) -> None:
        if tag == "a" and self._current_href is not None:
            label = " ".join("".join(self._current_link_text).split())
            self.links.append((self._current_href, label))
            self._current_href = None
            self._current_link_text = []

    def handle_data(self, data: str) -> None:
        cleaned = " ".join(data.split())
        if cleaned:
            self.text_chunks.append(cleaned)
        if self._current_href is not None:
            self._current_link_text.append(data)


class TestNordwerkSession03Slice(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        if not INDEX_HTML.is_file():
            raise AssertionError(f"Missing product file: {INDEX_HTML}")
        cls.raw_html = INDEX_HTML.read_text(encoding="utf-8")
        cls.inspector = _HTMLInspector()
        cls.inspector.feed(cls.raw_html)
        cls.visible_text = " ".join(cls.inspector.text_chunks)

    def test_placeholder_replaced_by_factory(self) -> None:
        """Ensure the initial scaffold placeholder has been replaced."""
        self.assertNotIn("TODO_FACTORY_GENERATION", self.raw_html)

    def test_ac01_identity_and_main_statement(self) -> None:
        """AC-01: N-01 company name and N-02 main statement are visible."""
        self.assertEqual(self.inspector.html_lang, "de")
        self.assertIn("Nordwerk Industrie-Service", self.visible_text)
        self.assertIn(
            "Praktische Unterstützung für Ihren technischen Betrieb.",
            self.visible_text,
        )

    def test_ac02_first_service_present(self) -> None:
        """B2 / AC-02 slice: At least one required service (N-03, N-04, or N-05) with verbatim text."""
        services = {
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
        matched = [
            title
            for title, description in services.items()
            if title in self.visible_text and description in self.visible_text
        ]
        self.assertGreaterEqual(
            len(matched),
            1,
            "At least one AC-02 service with its exact required description must be present.",
        )

    def test_ac04_contact_mailto_and_course_notice(self) -> None:
        """AC-04: N-08 mailto link ('Anfrage stellen' -> mailto:kontakt@nordwerk.example) and N-09 notice."""
        self.assertIn(
            ("mailto:kontakt@nordwerk.example", "Anfrage stellen"),
            self.inspector.links,
            f"Expected ('mailto:kontakt@nordwerk.example', 'Anfrage stellen') in {self.inspector.links}",
        )
        self.assertIn(
            "Fiktives Unternehmen – Lehrprojekt der HAW Hamburg. "
            "Keine realen Angebote oder Kontaktaufnahme.",
            self.visible_text,
        )


if __name__ == "__main__":
    unittest.main()
