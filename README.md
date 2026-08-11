# SAP AI Test Agent

Fresh build, replacing the old Streamlit project. FastAPI backend,
plain HTML/CSS/JS frontend, no build step.

## What this version does

Runs live validation checks against your real NeonDB procurement
data (Purchase Requisitions → Purchase Orders → Goods Receipts →
Invoices), generates an AI recommendation for every failure, persists
the run to `execution_history` / `test_results` / `ai_recommendations`
/ `defects`, and renders a console-style report in the browser.

Inventory and Finance modules aren't wired up yet — the nav buttons
are there but disabled. Same pattern as Procurement: add functions to
`rule_engine.py`, a metrics function + endpoint in `routers/`, done.

## Setup

```bash
cd backend
python -m venv venv
venv\Scripts\activate          # Windows
pip install -r requirements.txt

copy .env.example .env         # then edit .env with your real values
```

Edit `.env`:
- `DATABASE_URL` — your NeonDB connection string (the one you used for the schema export)
- `GROQ_API_KEY` — optional. Leave blank and the app still works, using templated (non-LLM) recommendations instead of AI-generated ones.

## Run

```bash
cd backend
uvicorn main:app --reload --port 8000
```

Open **http://localhost:8000** — click "Run Validation".

## Project structure

```
backend/
  main.py              FastAPI app, serves API + frontend
  database.py           NeonDB connection/session
  models.py              SQLAlchemy models — matches your actual schema exactly
  rule_engine.py          Validation logic (PR/PO/GR/Invoice checks)
  ai_service.py            Groq recommendations, with fallback if no API key
  schemas.py                API response shapes
  routers/report.py          The one endpoint: GET /api/report/procurement
frontend/
  index.html
  style.css              Console/diagnostics design system
  app.js                    Fetches the report, renders everything
```

## What the validation checks right now

- PR has line items, quantities > 0
- PO vendor is approved
- PO has line items and references a PR
- GR exists for open/released POs; received qty vs ordered qty (over/under delivery)
- Invoice has a linked GR; invoice amount matches PO value (3-way match)
- Inventory at/below reorder level

Each failure gets an AI-generated (or templated) recommendation, and
the whole run is written to the DB so you have an audit trail in
`execution_history`.
