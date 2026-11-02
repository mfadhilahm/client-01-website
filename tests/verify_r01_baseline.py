"""Isolated verification check for the Session 4 / Session 5 reference experiment task R-01.

Verifies that all Session 4 Release Candidate criteria (AC-01..AC-08) continue to pass
without regressions AND that the 4th service card ('Projektkoordination') is present.
Named 'verify_r01_baseline.py' so default 'test_*.py' discovery on the customer Release
Candidate (R-BASE) only checks the customer Release Candidate scope.
"""
from __future__ import annotations

import unittest

from tests.test_website_s4 import TestNordwerkSession04ReleaseCandidate


class TestNordwerkR01ReferenceTask(TestNordwerkSession04ReleaseCandidate):
    def test_r01_project_coordination_card_added_without_regression(self) -> None:
        """R-01: 'Projektkoordination' card is present alongside all 3 existing services."""
        self.assertIn("Projektkoordination", self.visible_text)
        self.assertIn(
            "Wir koordinieren klar abgegrenzte technische Vorhaben mit Ihrem Team.",
            self.visible_text,
        )


if __name__ == "__main__":
    unittest.main()
