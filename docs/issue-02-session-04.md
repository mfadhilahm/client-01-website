# Issue #2: [NW-S4-001] Session 4 Release Candidate (AC-01 to AC-08)

- **Project ID:** `website-01` (**Nordwerk Industrie-Service**)
- **Task ID:** `NW-S4-001` (builds on `NW-S3-001` from Session 3)
- **Session:** Session 4 (Deliverable Release Candidate & Quality Gate Verification)
- **Target Product Files:** `site/index.html`, `site/styles.css`
- **Target Product Test:** `tests/test_website_s4.py` (3 automated check families)

---

## 1. Commission Scope & Mandatory Content (`AC-01`–`AC-08`)

Complete the first standalone **Release Candidate** for **Nordwerk Industrie-Service** (`AC-01` through `AC-08`) via the Software Factory (`agentic_ai_haw_2627`), adding the remaining services (`N-04`, `N-05`), target groups (`N-06`), working approach (`N-07`), section navigation (`AC-05`), responsive `375px`/`1280px` layout (`AC-06`), and accessibility/keyboard focus requirements (`AC-07`).

### Mandatory Verbatim Content (`N-01`–`N-09`)

| ID | Category | Required Verbatim German Text | Target AC |
| :--- | :--- | :--- | :--- |
| **N-01** | Company Name | `Nordwerk Industrie-Service` | `AC-01` |
| **N-02** | Main Statement | `Praktische Unterstützung für Ihren technischen Betrieb.` | `AC-01` |
| **N-03** | Service 1 – *Wartungsplanung* | `Wir strukturieren Wartungsaufgaben und dokumentieren Zuständigkeiten für kleine technische Betriebe.` | `AC-02` |
| **N-04** | Service 2 – *Ersatzteilkoordination* | `Wir unterstützen bei der Abstimmung von Ersatzteilbedarfen und Lieferterminen.` | `AC-02` |
| **N-05** | Service 3 – *Betriebsdokumentation* | `Wir bringen technische Unterlagen in eine nachvollziehbare und nutzbare Struktur.` | `AC-02` |
| **N-06** | Target Groups | `Kleine Produktionsbetriebe` and `Technische Serviceunternehmen` | `AC-03` |
| **N-07** | Working Approach | `Ein fester Ansprechpartner, ein gemeinsam vereinbarter Leistungsumfang und nachvollziehbare Ergebnisse.` | `AC-03` |
| **N-08** | Contact Link | Label `Anfrage stellen` with `href="mailto:kontakt@nordwerk.example"` | `AC-04` |
| **N-09** | Course Notice | `Fiktives Unternehmen – Lehrprojekt der HAW Hamburg. Keine realen Angebote oder Kontaktaufnahme.` | `AC-04` |

### Full Session 4 Acceptance Criteria (`AC-01`–`AC-08`)

| AC ID | Requirement | Verification |
| :--- | :--- | :--- |
| **AC-01** | Company name (`N-01`) and main statement (`N-02`) are easy to find on the initial view. | Automated (`Family 1`) + Browser Review |
| **AC-02** | All three services (`N-03`, `N-04`, `N-05`) with their required descriptions are identifiable. | Automated (`Family 1`) + Browser Review |
| **AC-03** | Both target groups (`N-06`) and the working approach (`N-07`) are included; no invented performance claims. | Automated (`Family 1`) + Browser Review |
| **AC-04** | Clearly labelled contact link (`Anfrage stellen`) opens `mailto:kontakt@nordwerk.example`; course notice (`N-09`) is visible. | Automated (`Family 2`) + Browser Review |
| **AC-05** | Navigation leads to Services (`#leistungen`) and Contact (`#kontakt`); internal links and local assets (`styles.css`) work. | Automated (`Family 2 & 3`) + Browser Review |
| **AC-06** | At `375 px` and `1280 px` width there is no horizontal content overflow; text and contact link remain usable. | Automated (`Family 3`) + Browser Review (`375px` / `1280px`) |
| **AC-07** | Document title, German language attribute (`lang="de"`), sensible heading hierarchy, visible keyboard focus indicators (`:focus-visible`), and image `alt` texts (where applicable). | Automated (`Family 3`) + Keyboard `Tab` Review |
| **AC-08** | Fresh product checkout starts with a documented command without Factory/LLM/DB; product tests run separately. | Verified via `README.md` & tagged commit `R-BASE` |

---

## 2. Explicit Scope Guardrails (Non-Goals)

- **No CMS or Contact Form:** Static HTML/CSS and `mailto:kontakt@nordwerk.example` only; no `<form>` elements or PHP backend.
- **No Invented Claims:** Do not add customer logos, references, ISO/TÜV certifications, 24/7 response-time SLAs, or success percentages.
- **No External Dependencies:** No external web fonts, CDN scripts, or analytics/tracking services.
- **Session 5 Items Excluded:** `CR-01` and `SR-01` are deferred to Session 5; `R-01` (*Projektkoordination*) is executed strictly as an isolated baseline experiment on a separate branch/checkout of `R-BASE` and is **not** merged into the customer Release Candidate.

---

## 3. Accountable Humans & Task Ownership (`D1`)

| Task / Responsibility | Accountable Human(s) | Expected Outcome |
| :--- | :--- | :--- |
| **Issue Scoping & Product Setup (`NW-S4-001`)** | `yaw`, `saad` | `docs/issue-02-session-04.md`, `README.md` startup/test instructions |
| **Responsive Layout & Focus Styling (`AC-06`, `AC-07`)** | `yaw`, `mirko` | `site/styles.css` supporting `375px`/`1280px` without overflow and `:focus-visible` outlines |
| **Automated Product Checks (3 Check Families, `B6`)** | `felix`, `yaw` | `tests/test_website_s4.py` covering Content, Contact/Navigation, and Local Assets/A11y |
| **Factory Workflow Execution & Fault Gate (`A1`–`A4`)** | `muhammad`, `minh`, `mirko` | Real LLM run `WF-WEBSITE01-S4-001` + controlled fault run `WF-WEBSITE01-S4-FAULT-001` |
| **Browser Review (`375px`/`1280px` + Keyboard `Tab`) & Release Approval** | `saad`, `felix`, `yaw` | `docs/release-candidate-s4.md`, human gate `review.json` (`approved`), and Git tag `R-BASE` |
