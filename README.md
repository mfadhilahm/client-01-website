# Nordwerk Industrie-Service – Website (`client-01-website`)

> **Course Notice / Übungshinweis (N-09):**  
> Fiktives Unternehmen – Lehrprojekt der HAW Hamburg. Keine realen Angebote oder Kontaktaufnahme.

Customer product repository for **Customer Project 01 (Nordwerk Industrie-Service)**, produced and verified through the separate Software Factory repository (`agentic_ai_haw_2627`).

---

## 1. Independent Startup from a Fresh Checkout (`AC-08`, `B5`)

This static website has **no runtime dependency** on the Software Factory, any LLM provider, or the PostgreSQL database.

### Clone & Start via Local HTTP Server (Recommended)
Run from a fresh checkout of `client-01-website`:

```powershell
git clone https://github.com/mfadhilahm/client-01-website.git
cd client-01-website
git checkout R-BASE
python -m http.server 8080 --directory site
```

Then open <http://localhost:8080> in your browser.

### Direct File Open
Alternatively, open `site/index.html` directly in any web browser.

---

## 2. Separate Automated Product Checks (`AC-08`, `B6`)

The automated product test suites verify both the Session 3 slice ([`tests/test_website_s3.py`](tests/test_website_s3.py)) and the full Session 4 Release Candidate across **three distinct check families** ([`tests/test_website_s4.py`](tests/test_website_s4.py)):
1. **Family 1 – Required Content (`AC-01`, `AC-02`, `AC-03`):** Verbatim identity (`N-01`, `N-02`), all three services (`N-03`, `N-04`, `N-05`), both target groups (`N-06`), working approach (`N-07`), course notice (`N-09`), and absence of `<form>` or forbidden claims.
2. **Family 2 – Contact & Navigation Targets (`AC-04`, `AC-05`):** `Anfrage stellen` link targeting `mailto:kontakt@nordwerk.example` (`N-08`), `<nav>` links to `#leistungen` and `#kontakt`, and target resolution for all internal `#anchor` links.
3. **Family 3 – Local Assets, Responsive & Accessibility (`AC-05`, `AC-06`, `AC-07`):** Local asset existence (`styles.css`), zero external font/tracking URLs, `<html lang="de">`, `<title>`, viewport meta, heading hierarchy (`h1`–`h3`), and `:focus-visible` + `@media` rules.

Run all product checks using the Python standard library (`unittest`, zero third-party packages required):

```powershell
python -m unittest discover -s tests -p "test_*.py" -v
```

Or run specifically with `pytest`:

```powershell
python -m pytest tests/test_website_s4.py -q
```

For the isolated Session 4/5 reference experiment task **`R-01`** (on the separate `R-01` branch/worktree only):

```powershell
python -m pytest tests/verify_r01_baseline.py -q
```

---

## 3. Release Candidate Scope & Documentation (`AC-01`–`AC-08`)

- **Session 3 Customer Issue:** [`docs/issue-01-session-03.md`](docs/issue-01-session-03.md) (`NW-S3-001`)
- **Session 4 Customer Issue:** [`docs/issue-02-session-04.md`](docs/issue-02-session-04.md) (`NW-S4-001`)
- **Session 4 Release Candidate Checklist & Browser Review Record:** [`docs/release-candidate-s4.md`](docs/release-candidate-s4.md)

| Criterion | Required Content / Verification Scope | Target |
| :--- | :--- | :--- |
| **AC-01** | `N-01` (*Nordwerk Industrie-Service*) & `N-02` (*Praktische Unterstützung für Ihren technischen Betrieb.*) | Session 3 & 4 |
| **AC-02** | All 3 services: `N-03` (*Wartungsplanung*), `N-04` (*Ersatzteilkoordination*), `N-05` (*Betriebsdokumentation*) | Session 4 |
| **AC-03** | Target groups `N-06` (*Kleine Produktionsbetriebe*, *Technische Serviceunternehmen*) & working approach `N-07` | Session 4 |
| **AC-04** | Contact CTA `N-08` (*Anfrage stellen* $\rightarrow$ `mailto:kontakt@nordwerk.example`) & visible course notice `N-09` | Session 3 & 4 |
| **AC-05** | Navigation (`#leistungen`, `#kontakt`) and local asset resolution (`styles.css`) | Session 4 |
| **AC-06** | Responsive layout at `375 px` and `1280 px` width without horizontal content overflow | Session 4 |
| **AC-07** | Document `<title>`, `lang="de"`, semantic headings (`h1`–`h3`), and visible keyboard focus (`:focus-visible`) | Session 4 |
| **AC-08** | Independent startup and separate product test execution from a fresh checkout (`R-BASE`) | Session 4 |
