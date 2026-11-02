# Session 4 Release Candidate Verification & Browser Review (`docs/release-candidate-s4.md`)

- **Project ID:** `website-01` (**Nordwerk Industrie-Service**)
- **Customer Task ID:** `NW-S4-001`
- **Release Candidate Tag:** `R-BASE`
- **Date:** 2026-11-02
- **Reviewers:** `saad`, `felix`, `yaw`

---

## 1. Release Candidate Checklist (`AC-01`–`AC-08`) (`B1`–`B6`)

| AC ID | Requirement | Automated Check (`tests/test_website_s4.py`) | Manual Browser / Checkout Verification | Status |
| :--- | :--- | :--- | :--- | :--- |
| **AC-01** | Company name (`N-01`) and main statement (`N-02`) easy to find on initial view. | `test_family1_required_content_ac01_ac02_ac03` | Verified in hero section (`#start`) at both `375 px` and `1280 px`. | **Passed** |
| **AC-02** | All three services (`N-03` *Wartungsplanung*, `N-04` *Ersatzteilkoordination*, `N-05` *Betriebsdokumentation*) with required descriptions present. | `test_family1_required_content_ac01_ac02_ac03` | Verified 3 distinct `.service-card` elements under `#leistungen`. | **Passed** |
| **AC-03** | Both target groups (`N-06`: *Kleine Produktionsbetriebe*, *Technische Serviceunternehmen*) and working approach (`N-07`) included; no invented claims. | `test_family1_required_content_ac01_ac02_ac03` | Verified `#zielgruppen` list and `#arbeitsweise` statement; zero invented SLAs/certifications. | **Passed** |
| **AC-04** | Contact link `Anfrage stellen` opens `mailto:kontakt@nordwerk.example` (`N-08`); course notice (`N-09`) visible. | `test_family2_contact_and_navigation_targets_ac04_ac05` | Verified top course notice banner and `mailto:kontakt@nordwerk.example` link in hero and `#kontakt`. | **Passed** |
| **AC-05** | Navigation leads to Services (`#leistungen`) and Contact (`#kontakt`); internal links and local assets (`styles.css`) work. | `test_family2_contact_and_navigation_targets_ac04_ac05` + `test_family3_local_assets_and_usability_ac05_ac06_ac07` | Clicking `<nav>` links scrolls to `#leistungen`, `#zielgruppen`, `#arbeitsweise`, and `#kontakt`; `styles.css` loads with HTTP `200`. | **Passed** |
| **AC-06** | At `375 px` and `1280 px` width no horizontal content overflow; text and contact usable. | `test_family3_local_assets_and_usability_ac05_ac06_ac07` (`viewport` + `@media`) | Verified in browser DevTools at `375 px` and `1280 px` (see Section 2 below). | **Passed** |
| **AC-07** | Document `<title>`, `lang="de"`, sensible headings (`h1`–`h3`), visible keyboard focus (`:focus-visible`), image `alt` texts. | `test_family3_local_assets_and_usability_ac05_ac06_ac07` | Verified sequential `Tab` focus ring across skip-link, `<nav>` links, and CTA links (see Section 2 below). | **Passed** |
| **AC-08** | Fresh product checkout starts with documented command without Factory/LLM/DB; product tests run separately. | `python -m unittest discover -s tests -p "test_*.py" -v` (7/7 passed) | Verified standalone server `python -m http.server 8080 --directory site` on fresh checkout of `R-BASE`. | **Passed** |

---

## 2. Browser Responsive & Keyboard Accessibility Review Protocol (`B3`, `B4`, `D1`)

- **Reviewers:** `yaw` (Responsive & Layout), `saad` (Content & Release Approval), `felix` (Keyboard Navigation & QA)
- **Browser & Environment:** Chromium / Edge DevTools Device Mode against `http://localhost:8080` (`python -m http.server 8080 --directory site`)
- **Review Date:** 2026-11-02

### 2.1 Viewport Width Verification (`AC-06`)

| Viewport Width | Measured `document.documentElement.scrollWidth` | Horizontal Overflow (`scrollWidth > clientWidth`) | Layout & Readability Observations | Result |
| :--- | :--- | :--- | :--- | :--- |
| **`375 px` (Mobile)** | `375 px` (`clientWidth = 375 px`) | **None (`0 px` overflow)** | `.header-inner` and `.nav-list` wrap cleanly (`flex-wrap: wrap`); `.service-grid` collapses to a single column (`1fr`); `.cta-link` spans full container width (`width: 100%`) and remains easily tappable. | **Passed (`yaw`, `felix`)** |
| **`1280 px` (Desktop)** | `1280 px` (`clientWidth = 1280 px`) | **None (`0 px` overflow)** | Centered `.container` (`max-width: 1080px`); all 3 service cards render side-by-side in `.service-grid`; generous whitespace and clear visual hierarchy. | **Passed (`yaw`, `saad`)** |

### 2.2 Keyboard Navigation & Focus Verification (`AC-07`)

| Tab Stop # | Element Focused | Selector / Target | Visible Focus Ring | Activation (`Enter`) Behavior | Result |
| :---: | :--- | :--- | :--- | :--- | :--- |
| **1** | Skip Link (`Zum Hauptinhalt springen`) | `a.skip-link[href="#main-content"]` | Slides into view at top-left (`left: 0.75rem`) with `3px solid #1d4ed8` outline | Jumps focus to `<main id="main-content">` | **Passed (`felix`)** |
| **2** | Nav Link: `Leistungen` | `.site-nav a[href="#leistungen"]` | `3px solid #1d4ed8` outline (`outline-offset: 2px`) + `#f1f5f9` background | Scrolls viewport to `<section id="leistungen">` | **Passed (`felix`)** |
| **3** | Nav Link: `Zielgruppen` | `.site-nav a[href="#zielgruppen"]` | `3px solid #1d4ed8` outline (`outline-offset: 2px`) | Scrolls viewport to `<section id="zielgruppen">` | **Passed (`felix`)** |
| **4** | Nav Link: `Arbeitsweise` | `.site-nav a[href="#arbeitsweise"]` | `3px solid #1d4ed8` outline (`outline-offset: 2px`) | Scrolls viewport to `<section id="arbeitsweise">` | **Passed (`felix`)** |
| **5** | Nav Link: `Kontakt` | `.site-nav a[href="#kontakt"]` | `3px solid #1d4ed8` outline (`outline-offset: 2px`) | Scrolls viewport to `<section id="kontakt">` | **Passed (`felix`)** |
| **6** | Hero CTA: `Anfrage stellen` | `#start a.cta-link[href="mailto:kontakt@nordwerk.example"]` | `3px solid #1d4ed8` outline (`outline-offset: 2px`) | Targets `mailto:kontakt@nordwerk.example` | **Passed (`saad`)** |
| **7** | Contact Section CTA: `Anfrage stellen` | `#kontakt a.cta-link[href="mailto:kontakt@nordwerk.example"]` | `3px solid #1d4ed8` outline (`outline-offset: 2px`) | Targets `mailto:kontakt@nordwerk.example` | **Passed (`saad`)** |

---

## 3. Distinction Between Release Candidate (`R-BASE`) and Controlled Fault Test (`D1`, `A3`)

- **Controlled Fault Run (`WF-WEBSITE01-S4-FAULT-001`):** Executed in an isolated temporary copy with a broken contact address (`mailto:falsch@nordwerk.example`). Automated check `test_family2_contact_and_navigation_targets_ac04_ac05` failed (`exit_code = 1`), the workflow set `human_gate_status = "escalate_to_human"`, approval was technically blocked, and reviewer `felix` recorded `decision = "changes_requested"`.
- **Approved Release Candidate (`WF-WEBSITE01-S4-001` $\rightarrow$ Tag `R-BASE`):** Passes all 3 automated check families (`7/7` tests across `test_website_s3.py` and `test_website_s4.py`) and the human browser/keyboard review above; approved by `saad` (`decision = "approved"` in `runs/website-01/WF-WEBSITE01-S4-001/review.json`).
