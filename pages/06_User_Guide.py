"""
Page: User Guide
Step-by-step examples for every role. Business users first, then IT.
"""

import streamlit as st, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

st.set_page_config(page_title="User Guide · IEP Platform", page_icon="📖", layout="wide")

from utils.theme import apply_theme, page_header, sidebar_branding
from utils.pdf_loader import init_session, auto_load_pdf

apply_theme()
init_session()
sidebar_branding()
auto_load_pdf()

page_header("📖", "User Guide", "Step-by-step examples for every role — start here if you are new to this platform", "#00838F")

# ── Overview ──────────────────────────────────────────────────────────────────
st.markdown("""
<div style="background:white;border-radius:12px;border:1px solid #E8EAF6;
            padding:24px;margin-bottom:24px;line-height:1.8;color:#37474F;">
    <div style="font-weight:800;color:#1A1A2E;font-size:1.1rem;margin-bottom:12px;">
        What is this platform?
    </div>
    This platform turns complex IEP (Individualized Education Program) legal requirements into 
    practical, role-specific tools. Whether you are a teacher preparing for a CSE meeting, 
    a developer building an IEP management system, or a QA tester validating compliance rules — 
    this guide walks you through real examples step by step.
    <br><br>
    <b>The IEP process is governed by IDEA (Individuals with Disabilities Education Act)</b>, 
    a federal law. Every state must follow IDEA minimums, and states may add additional requirements. 
    This platform references federal IDEA rules as the baseline.
</div>
""", unsafe_allow_html=True)

# ── Tabs: Business first, IT second ──────────────────────────────────────────
tab_ba, tab_coord, tab_qa, tab_dev, tab_law = st.tabs([
    "Business Analyst", "Special Ed Coordinator", "QA Tester", "Developer / Architect", "Law & Guidelines Reference"
])

# ─────────────────────────────────────────────────────────────────────────────
# BUSINESS ANALYST
# ─────────────────────────────────────────────────────────────────────────────
with tab_ba:
    st.markdown("### Your Goal as a Business Analyst")
    st.markdown("""
    You need to understand the **IEP process end-to-end** so you can document requirements, 
    identify system gaps, and communicate accurately with developers and coordinators.
    """)

    st.markdown("---")
    st.markdown("### Example Scenario")
    st.markdown("""
    <div style="background:#E3F2FD;border-left:4px solid #1565C0;border-radius:8px;
                padding:16px 20px;margin:12px 0;font-size:0.9rem;color:#0D47A1;">
        <b>Scenario:</b> Your organization is building a new IEP management system. 
        You need to document what happens from the moment a student is referred until 
        their first IEP is implemented. You also need to know what rules the system 
        must enforce.
    </div>
    """, unsafe_allow_html=True)

    steps_ba = [
        ("Step 1", "Understand the full process", "Workflow Maps",
         "Go to Workflow Maps → select 'Initial IEP' → choose 'Step by Step' view.\n\nYou will see all 6 phases: Referral → Consent → Evaluation → Eligibility → IEP Development → Placement. Each phase shows the owner, timeline, required documents and acceptance criteria. This is your requirements source of truth."),
        ("Step 2", "Look up a specific rule", "Document Search",
         "Go to Document Search → upload your SOP PDF → type a question like:\n'What is the 60-day evaluation timeline?'\n\nThe system returns the exact page and passage from your SOP. You can trace any requirement back to the source document."),
        ("Step 3", "Understand what triggers what", "Rule Engine",
         "Go to Rule Engine → set IEP Stage to 'Initial Evaluation' → select 'Autism Spectrum Disorder' → set age to 10 → click Generate.\n\nThe engine shows: which evaluations are required, which services are typically needed, and which IDEA rules are triggered. This becomes your functional requirements list."),
        ("Step 4", "Document gaps and export", "Rule Engine + Workflow Maps",
         "Use the Download JSON button in the Rule Engine to export the full rule output for a given student profile.\n\nIn Workflow Maps, switch to 'Summary Table' view and export to CSV. These two exports together give you a complete requirements traceability matrix."),
    ]

    for label, title, module, detail in steps_ba:
        with st.expander(f"{label}: {title}  —  Use: {module}", expanded=False):
            st.markdown(f"""
            <div style="background:#FAFBFF;border-radius:8px;padding:16px;
                        font-size:0.88rem;line-height:1.8;color:#37474F;
                        white-space:pre-line;">{detail}</div>
            """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### Key IEP Terms Every BA Should Know")
    terms = [
        ("CSE","Committee on Special Education — the team that makes IEP decisions"),
        ("FAPE","Free Appropriate Public Education — what IDEA guarantees every eligible student"),
        ("LRE","Least Restrictive Environment — students must be educated alongside non-disabled peers as much as possible"),
        ("PWN","Prior Written Notice — school must notify parents in writing before making any change to the IEP"),
        ("IDEA","Individuals with Disabilities Education Act — the federal law governing all IEP processes"),
        ("Present Levels","The section of the IEP that documents the student's current academic and functional performance"),
        ("Annual Goals","Measurable targets the student is expected to achieve within one year"),
        ("Related Services","Supplementary services like speech therapy, OT, PT that support the IEP goals"),
    ]
    t1, t2 = st.columns(2)
    for i, (term, defn) in enumerate(terms):
        with (t1 if i % 2 == 0 else t2):
            st.markdown(f"""
            <div style="background:white;border:1px solid #E8EAF6;border-radius:8px;
                        padding:12px 16px;margin:4px 0;">
                <span style="font-weight:700;color:#1565C0;font-family:'JetBrains Mono',monospace;
                             font-size:0.85rem;">{term}</span>
                <div style="color:#546E7A;font-size:0.85rem;margin-top:4px;">{defn}</div>
            </div>
            """, unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# SPECIAL ED COORDINATOR
# ─────────────────────────────────────────────────────────────────────────────
with tab_coord:
    st.markdown("### Your Goal as a Special Ed Coordinator")
    st.markdown("You need to ensure every IEP meeting is legally compliant, every document is filed, and every deadline is met.")

    st.markdown("""
    <div style="background:#E8F5E9;border-left:4px solid #2E7D32;border-radius:8px;
                padding:16px 20px;margin:12px 0;font-size:0.9rem;color:#1B5E20;">
        <b>Scenario:</b> You have an Initial IEP meeting scheduled for next week. 
        You want to make sure you have everything ready and nothing is missed.
    </div>
    """, unsafe_allow_html=True)

    steps_coord = [
        ("Step 1", "Generate your pre-meeting checklist",
         "Go to Compliance Checklist → select 'Initial IEP' → select your role 'CSE Chairperson'.\n\nYou will see every required action sorted by priority. Red items labeled 'Critical' are IDEA-mandated — missing them is a legal violation. Complete each item as you go."),
        ("Step 2", "Check what the teacher needs to prepare",
         "Still in Compliance Checklist → change Role to 'Special Education Teacher'.\n\nYou can see exactly what the teacher must bring to the meeting: current evaluation data, measurable goals, service grid. Share this list with the teacher as a preparation reminder."),
        ("Step 3", "Verify the process timeline",
         "Go to Workflow Maps → select 'Initial IEP' → Step by Step view.\n\nExpand each step to review the timeline. If you received consent on October 1, the evaluation must be complete and the eligibility meeting held by the 60th school day — use this to confirm your meeting date is compliant."),
        ("Step 4", "Export and file your records",
         "After the meeting, go back to Compliance Checklist → check off all completed items → add the student name and OSIS number → click Export CSV.\n\nThis gives you a dated compliance record you can attach to the student file."),
    ]
    for label, title, detail in steps_coord:
        with st.expander(f"{label}: {title}", expanded=False):
            st.markdown(f"""
            <div style="background:#FAFBFF;border-radius:8px;padding:16px;
                        font-size:0.88rem;line-height:1.8;color:#37474F;
                        white-space:pre-line;">{detail}</div>
            """, unsafe_allow_html=True)

    st.info("**Important:** This platform is a reference and compliance tool. Always consult your district's legal counsel and state education department for official guidance on any contested IEP matter.")

# ─────────────────────────────────────────────────────────────────────────────
# QA TESTER
# ─────────────────────────────────────────────────────────────────────────────
with tab_qa:
    st.markdown("### Your Goal as a QA Tester")
    st.markdown("You need test cases that cover every IEP business rule so the system under test cannot process a non-compliant IEP without raising an error.")

    st.markdown("""
    <div style="background:#FFF8E1;border-left:4px solid #F57F17;border-radius:8px;
                padding:16px 20px;margin:12px 0;font-size:0.9rem;color:#E65100;">
        <b>Scenario:</b> Your team is testing a new IEP module. You need to build a test 
        suite that covers the 60-day timeline rule, consent requirements, and measurable 
        goals validation. You use Jira + Cucumber for BDD testing.
    </div>
    """, unsafe_allow_html=True)

    steps_qa = [
        ("Step 1", "Generate your test suite",
         "Go to Test Cases → set Domain to 'Evaluation' → Priority to 'Critical' → Export Format to 'Gherkin BDD'.\n\nClick Export. You get a .feature file with ready-to-use Cucumber scenarios including positive and negative cases. Import directly into your Cucumber framework."),
        ("Step 2", "Export to TestRail or Jira",
         "Change Export Format to 'CSV for TestRail' → click Export.\n\nThe CSV maps to TestRail's import format: ID, Title, Priority, Preconditions (Given), Steps (When), Expected Result (Then). Import it and your test suite is built."),
        ("Step 3", "Validate test coverage against the rule engine",
         "Go to Rule Engine → set up a student profile (e.g. Autism, age 10, Initial Evaluation) → click Generate.\n\nCompare the triggered rules (R-001, R-003, R-005 etc.) against your test cases. Every triggered rule should have at least one Critical test case covering it."),
        ("Step 4", "Use Workflow Maps for edge case discovery",
         "Go to Workflow Maps → select any process → Step by Step → expand each phase.\n\nEach phase shows QA Acceptance Criteria. These are additional test scenarios beyond the main test bank — especially useful for boundary conditions like 'Day 60 exactly' or 'parent consent received after referral date'."),
    ]
    for label, title, detail in steps_qa:
        with st.expander(f"{label}: {title}", expanded=False):
            st.markdown(f"""
            <div style="background:#FAFBFF;border-radius:8px;padding:16px;
                        font-size:0.88rem;line-height:1.8;color:#37474F;
                        white-space:pre-line;">{detail}</div>
            """, unsafe_allow_html=True)

    st.markdown("### Test Priority Guide")
    st.markdown("""
    | Priority | What it means | Risk if it fails |
    |---|---|---|
    | **Critical** | Mandated by IDEA federal law | Legal violation — potential IDEA complaint |
    | **Required** | Required by best practice or state guidance | Compliance gap — audit finding |
    | **Recommended** | Best practice, not legally mandated | Process quality issue |
    """)

# ─────────────────────────────────────────────────────────────────────────────
# DEVELOPER / ARCHITECT
# ─────────────────────────────────────────────────────────────────────────────
with tab_dev:
    st.markdown("### Your Goal as a Developer or Architect")
    st.markdown("You need to understand the business rules well enough to implement them correctly in code, and have a traceable spec to reference during code review.")

    st.markdown("""
    <div style="background:#EDE7F6;border-left:4px solid #6A1B9A;border-radius:8px;
                padding:16px 20px;margin:12px 0;font-size:0.9rem;color:#4A148C;">
        <b>Scenario:</b> You are building the IEP intake API. You need to know: 
        which fields are mandatory, what validations to apply, and what the system 
        must do when a 60-day deadline is approaching.
    </div>
    """, unsafe_allow_html=True)

    steps_dev = [
        ("Step 1", "Get the rules as a JSON spec",
         "Go to Rule Engine → configure a student profile → click Generate → click Download Rule Output as JSON.\n\nThis JSON file contains: required evaluations, recommended services, all triggered rule IDs with names and IDEA citations. Use it as your API validation spec. Every field in the JSON maps to a required system behavior."),
        ("Step 2", "Map rules to API endpoints",
         "Example mapping from the JSON output:\n\n  R-001 (60-day timeline) → POST /api/iep/consent must record consent_date\n                            → GET /api/iep/{id}/deadline must return consent_date + 60 school days\n  R-004 (consent required) → POST /api/iep/evaluation must validate consent_on_file == true\n  R-005 (PWN required)     → PATCH /api/iep/{id}/placement must trigger PWN notification event\n\nThis gives you a traceable line from IDEA law → business rule → API endpoint → test case."),
        ("Step 3", "Use the rule reference for code comments",
         "In the Rule Engine → All Business Rules tab, you can see every rule ID, law citation and exact outcome statement.\n\nCopy these directly into your code as comments:\n\n  # R-001: IDEA §300.301(c)(1)\n  # Evaluation must be completed within 60 school days of consent\n  deadline = add_school_days(consent_date, 60)"),
        ("Step 4", "Architecture guidance for IEP systems",
         "Key design patterns for IEP systems based on the business rules:\n\n  1. TIMELINE ENGINE — school-day-aware date calculator (not calendar days)\n  2. CONSENT STATE MACHINE — evaluation cannot start until consent state is RECEIVED\n  3. NOTIFICATION SERVICE — PWN must be sent before any placement change is committed\n  4. AUDIT LOG — every IEP action must be timestamped and attributed to a user role\n  5. ROLE-BASED ACCESS — CSE Chairperson, Teacher, Parent, Evaluator have different write permissions"),
    ]
    for label, title, detail in steps_dev:
        with st.expander(f"{label}: {title}", expanded=False):
            st.markdown(f"""
            <div style="background:#F3E5F5;border-radius:8px;padding:16px;
                        font-size:0.88rem;line-height:1.8;color:#37474F;
                        white-space:pre-line;font-family:'JetBrains Mono',monospace;">{detail}</div>
            """, unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# LAW & GUIDELINES REFERENCE
# ─────────────────────────────────────────────────────────────────────────────
with tab_law:
    st.markdown("### Federal Law and Guidelines Reference")
    st.markdown("This platform is based on the following publicly available federal laws and guidance documents.")

    refs = [
        ("IDEA — Individuals with Disabilities Education Act",
         "The primary federal law governing special education in the United States. All IEP processes must comply with IDEA.",
         "https://sites.ed.gov/idea/","Federal Law","#C62828"),
        ("IDEA Part B Regulations (34 CFR Part 300)",
         "The federal regulations implementing IDEA Part B, which covers students ages 3–21. This is the detailed rule book.",
         "https://www.ecfr.gov/current/title-34/subtitle-B/chapter-III/part-300","Federal Regulation","#E65100"),
        ("U.S. Department of Education — IDEA Website",
         "Official DOE resource for IDEA guidance, policy letters, Q&A documents and training materials.",
         "https://sites.ed.gov/idea/","Federal Guidance","#1565C0"),
        ("OSEP — Office of Special Education Programs",
         "The federal office that oversees IDEA implementation. Issues policy guidance and monitors state compliance.",
         "https://www2.ed.gov/about/offices/list/osers/osep/index.html","Federal Office","#0097A7"),
        ("Wrightslaw — Special Education Law",
         "Widely used plain-language resource for IDEA law and case summaries. Useful for non-lawyers.",
         "https://www.wrightslaw.com/","Reference Resource","#6A1B9A"),
        ("CPIR — Center for Parent Information and Resources",
         "Federally funded resource with plain-language guides on IEP rights, processes and dispute resolution.",
         "https://www.parentcenterhub.org/","Parent Resource","#2E7D32"),
    ]

    for title, desc, url, tag, color in refs:
        st.markdown(f"""
        <div style="background:white;border:1px solid #E8EAF6;border-radius:12px;
                    padding:18px 20px;margin:8px 0;
                    border-left:4px solid {color};">
            <div style="display:flex;justify-content:space-between;align-items:flex-start;gap:12px;">
                <div style="flex:1;">
                    <div style="font-weight:700;color:#1A1A2E;margin-bottom:4px;">{title}</div>
                    <div style="color:#546E7A;font-size:0.87rem;line-height:1.6;margin-bottom:10px;">{desc}</div>
                    <a href="{url}" target="_blank" style="color:{color};font-size:0.82rem;
                       font-weight:600;text-decoration:none;">🔗 {url}</a>
                </div>
                <span style="background:{color}15;color:{color};border-radius:6px;
                             padding:3px 10px;font-size:0.72rem;font-weight:700;
                             white-space:nowrap;">{tag}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("""
    <div style="background:#FFF8E1;border:1px solid #FFE082;border-radius:10px;
                padding:16px 20px;font-size:0.88rem;color:#F57F17;">
        <b>Important Disclaimer</b><br>
        This platform is a reference and compliance assistance tool based on publicly available 
        federal IDEA guidelines. It does not constitute legal advice. State-specific requirements 
        may differ from federal minimums. Always consult your state education department and 
        qualified legal counsel for official guidance on specific IEP matters.
    </div>
    """, unsafe_allow_html=True)
