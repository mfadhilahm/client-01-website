# Issue #1: [NW-S3-001] Session 3 Initial Website Slice (AC-01, AC-02 Slice N-03, AC-04)

- **Project ID:** `website-01`
- **Task ID:** `NW-S3-001`
- **Session:** Session 3 (First customer delivery through the Software Factory)
- **Target Product Path:** `site/index.html`, `site/styles.css`
- **Target Product Test:** `tests/test_website_s3.py`

---

## 1. Commission Summary & Today's Scope

Deliver the first runnable static website slice for **Nordwerk Industrie-Service** (fictional B2B service provider in Hamburg) in a standalone product repository (`client-01-website`), generated and checked through our Software Factory.

### Acceptance Criteria in Scope for Session 3

| AC ID | Requirement | Required Verbatim German Content |
| :--- | :--- | :--- |
| **AC-01** | Company name and main statement are easy to find on the initial view. | **N-01:** `Nordwerk Industrie-Service`<br>**N-02:** `Praktische Unterstützung für Ihren technischen Betrieb.` |
| **AC-02 (1st service)** | One service from AC-02 including its required description is identifiable. | **N-03 (Wartungsplanung):** `Wir strukturieren Wartungsaufgaben und dokumentieren Zuständigkeiten für kleine technische Betriebe.` |
| **AC-04** | Clearly labelled contact link targets `mailto:kontakt@nordwerk.example`; the course notice is visible. | **N-08:** Link label `Anfrage stellen` targeting `mailto:kontakt@nordwerk.example`<br>**N-09:** `Fiktives Unternehmen – Lehrprojekt der HAW Hamburg. Keine realen Angebote oder Kontaktaufnahme.` |

---

## 2. Open Questions, Customer Answers & Explicit Assumptions

| Topic | Question / Choice | Binding Clarification / Explicit Assumption |
| :--- | :--- | :--- |
| **Technology & Hosting** | Replace legacy PHP website with CMS and contact form? | **Clarified in Brief:** Static HTML/CSS website with a `mailto:` email link is accepted. CMS and contact form are outside scope. |
| **Language** | Should the initial release be German or English? | **Clarified in Brief:** Initial website is strictly in German (`lang="de"`), using the supplied strings verbatim. |
| **Service Selection for S3** | Which of the three AC-02 services (`N-03`, `N-04`, `N-05`) is delivered in Session 3? | **Explicit Assumption:** We deliver **N-03 (Wartungsplanung)** in Session 3. Services `N-04` (*Ersatzteilkoordination*) and `N-05` (*Betriebsdokumentation*), plus `AC-03` (`N-06`, `N-07`) and `AC-05`–`AC-08`, are scheduled for Session 4. |
| **Additional Claims / Assets** | Should we add customer references, SLAs/response times, certifications, or external fonts? | **Clarified in Brief:** Strictly forbidden. No invented customer logos, certifications, references, response times, or statistics. No external font or tracking services. |
| **Email Placeholder** | Is `kontakt@nordwerk.example` a live mailbox? | **Clarified in Brief:** Placeholder only; must link via `mailto:kontakt@nordwerk.example` with label `Anfrage stellen`, but no emails may be sent. |

---

## 3. Accountable Humans

| Responsibility | Accountable Human(s) | Factory Role(s) |
| :--- | :--- | :--- |
| **Commission & Customer Lead** | `yaw`, `saad` | `managing_director_customer_lead`, `product_owner_requirements` |
| **Planning & Delivery Tracking** | `felix` | `project_manager` |
| **Technical Delivery & Factory Run** | `minh`, `mirko`, `muhammad`, `saad` | `software_architect`, `backend_api_engineer`, `agent_engineer`, `integration_engineer` |
| **Automated & Manual Checks** | `felix`, `mirko` | `qa_test_engineer`, `ai_safety_security_engineer` |
| **Human Gate & Release Approval** | `saad`, `felix`, `yaw` | Explicit human review decision after visual + link verification |

---

## 4. Definition of Done (Session 3)

1. `site/index.html` is generated/updated by a real Factory run in `client-01-website` with a traceable commit diff from the frozen input commit.
2. All required verbatim strings (`N-01`, `N-02`, `N-03`, `N-08`, `N-09`) and `mailto:kontakt@nordwerk.example` are present and verified by `tests/test_website_s3.py`.
3. The site starts independently without the Factory (`python -m http.server 8080 --directory site`).
4. Visible content and the contact link are inspected by an accountable human and recorded in the human gate review artifact.
