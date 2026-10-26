# Nordwerk Industrie-Service – Website (`client-01-website`)

> **Course Notice / Übungshinweis (N-09):**  
> Fiktives Unternehmen – Lehrprojekt der HAW Hamburg. Keine realen Angebote oder Kontaktaufnahme.

Customer product repository for **Customer Project 01 (Nordwerk Industrie-Service)**, produced and verified through the separate Software Factory repository (`agentic_ai_haw_2627`).

---

## 1. Independent Startup (Without Factory Process, LLM, or Database)

This static website has **no runtime dependency** on the Software Factory, LLM provider, or PostgreSQL database.

### Option A: Serve via Local HTTP Server (Recommended)
Run from the root of `client-01-website`:

```powershell
python -m http.server 8080 --directory site
```

Then open <http://localhost:8080> in your browser.

### Option B: Direct File Open
Open `site/index.html` directly in any web browser.

---

## 2. Separate Product Test Command

The automated product checks verify the Session 3 acceptance criteria (`AC-01`, one service from `AC-02`, `AC-04`, and `B6` content rules) using only the Python standard library (`unittest` + `html.parser`), and also work with `pytest`:

```powershell
python -m unittest discover -s tests -p "test_*.py" -v
```

Or with `pytest`:

```powershell
python -m pytest tests/test_website_s3.py -q
```

---

## 3. Session 3 Scope & Customer Issue

See [`docs/issue-01-session-03.md`](docs/issue-01-session-03.md) (and GitHub Issue `#1` in this repository) for the full commission scope, required German strings (`N-01`, `N-02`, `N-03`, `N-08`, `N-09`), customer clarifications, explicit assumptions, and accountable humans.

| Criterion | Required Content ID | Status Target |
| :--- | :--- | :--- |
| **AC-01** | `N-01` (*Nordwerk Industrie-Service*) & `N-02` (*Praktische Unterstützung für Ihren technischen Betrieb.*) | Session 3 |
| **AC-02 (Slice)** | `N-03` (*Wartungsplanung: Wir strukturieren Wartungsaufgaben und dokumentieren Zuständigkeiten für kleine technische Betriebe.*) | Session 3 |
| **AC-04** | `N-08` (*Anfrage stellen* $\rightarrow$ `mailto:kontakt@nordwerk.example`) & `N-09` (*Fiktives Unternehmen – Lehrprojekt der HAW Hamburg. Keine realen Angebote oder Kontaktaufnahme.*) | Session 3 |
