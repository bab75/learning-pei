# IEP Education Platform

A clean, user-friendly Streamlit application for understanding and working with
Individualized Education Program (IEP) processes and compliance requirements.

## Quick Start

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. (Optional) Place your SOP PDF in the docs/ folder for auto-load
cp your_iep_sop.pdf docs/

# 3. Run the app
streamlit run Home.py
```

App opens at: http://localhost:8501

---

## Project Structure

```
iep_education_platform/
│
├── Home.py                    ← Main entry point (run this)
├── requirements.txt
├── README.md
│
├── pages/
│   ├── 01_Document_Search.py  ← Upload PDF, ask questions, browse by page (dropdown)
│   ├── 02_Workflow_Maps.py    ← IEP lifecycle flows with timeline and documents
│   ├── 03_Rule_Engine.py      ← Student profile → triggered rules and services
│   ├── 04_Compliance_Checklist.py ← Role-specific checklists with export
│   ├── 05_Test_Cases.py       ← BDD Gherkin, pytest, TestRail CSV export
│   └── 06_User_Guide.py       ← Step-by-step examples for every role
│
├── utils/
│   ├── theme.py               ← Shared CSS, colors, components
│   └── pdf_loader.py          ← PDF extraction, chunking, search, auto-load
│
└── docs/                      ← Place SOP PDFs here for auto-load
    └── .gitkeep
```

---

## Key Improvements Over v1

| Issue | Fix |
|---|---|
| Page number as number input buttons | Dropdown with page preview text |
| Suggested questions did not work | Clicking a question runs the search immediately |
| Page names had emojis and numbers | Clean names: Document Search, Workflow Maps, etc. |
| NYC DOE branding | Replaced with neutral "IEP Education Platform" |
| PDF re-upload every session | Auto-loads from docs/ folder on startup |
| No user guide | Full User Guide page with role-specific examples |
| Theme inconsistent | Unified shared theme.py across all pages |

---

## How PDF Loading Works

**Option A — Auto-load (recommended for daily use):**
Place your PDF in the `docs/` folder. The app loads it automatically on startup.
No upload needed. PDF persists for the entire session.

**Option B — Manual upload:**
Go to Document Search → use the file uploader widget.
PDF is available for the current browser session only.

**Note:** PDFs are excluded from GitHub via `.gitignore`. Each team member keeps
their own copy locally in the `docs/` folder.

---

## GitHub Setup

```bash
git init
git add .
git commit -m "IEP Education Platform v2"
git remote add origin https://github.com/YOUR_ORG/iep-education-platform.git
git push -u origin main
```

The `docs/` folder is in `.gitignore` — PDFs stay local.

---

## Extending the Platform

**Add a new disability classification:**
Edit `DISABILITY_MAP` in `pages/03_Rule_Engine.py`

**Add new business rules:**
Edit `RULES` dict in `pages/03_Rule_Engine.py`

**Add new checklist items:**
Edit `ITEMS` dict in `pages/04_Compliance_Checklist.py`

**Add new test cases:**
Edit `TEST_BANK` dict in `pages/05_Test_Cases.py`

**Upgrade to semantic search:**
Uncomment the sentence-transformers lines in `requirements.txt` and
replace `keyword_search()` in `utils/pdf_loader.py` with a FAISS vector search.
