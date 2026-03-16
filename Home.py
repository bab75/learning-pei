"""
IEP Education Platform
Entry point — run with: streamlit run Home.py
"""

import streamlit as st
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

st.set_page_config(
    page_title="IEP Education Platform",
    page_icon="📋",
    layout="wide",
    initial_sidebar_state="expanded",
)

from utils.theme import apply_theme, page_header, card, badge, sidebar_branding
from utils.pdf_loader import init_session, auto_load_pdf

apply_theme()
init_session()
sidebar_branding()

# ── Auto-load PDF silently ────────────────────────────────────────────────────
auto_load_pdf()

# ── Hero ──────────────────────────────────────────────────────────────────────
page_header(
    "📋",
    "IEP Education Platform",
    "Your complete guide to Individualized Education Program processes, rules and compliance",
    "#1565C0"
)

# ── PDF status banner ─────────────────────────────────────────────────────────
if st.session_state.doc_loaded:
    st.markdown(f"""
    <div style="background:#E8F5E9;border:1px solid #A5D6A7;border-radius:10px;
                padding:12px 20px;margin-bottom:20px;display:flex;
                align-items:center;gap:12px;">
        <span style="font-size:1.3rem;">✅</span>
        <div>
            <span style="font-weight:700;color:#2E7D32;">SOP Document Loaded</span>
            <span style="color:#388E3C;font-size:0.88rem;margin-left:8px;">
                {st.session_state.doc_name} &nbsp;·&nbsp;
                {len(st.session_state.doc_pages)} pages indexed &nbsp;·&nbsp;
                {len(st.session_state.doc_chunks)} searchable sections
            </span>
        </div>
    </div>
    """, unsafe_allow_html=True)
else:
    st.info("💡 No SOP PDF loaded yet. Go to **Document Search** to upload your IEP SOP document, or place a PDF in the `docs/` folder to auto-load it.")

# ── Metric row ────────────────────────────────────────────────────────────────
m1, m2, m3, m4, m5 = st.columns(5)
for col, (val, lbl, delta) in zip([m1,m2,m3,m4,m5], [
    ("6", "Platform Modules", "All roles covered"),
    ("4", "IEP Process Types", "Initial · Annual · Reeval · Amendment"),
    ("80+", "SOP Pages Indexed", "When PDF uploaded"),
    ("60", "Day IDEA Timeline", "Initial evaluation"),
    ("4", "User Roles", "BA · QA · Dev · Coordinator"),
]):
    with col:
        st.metric(lbl, val, delta)

st.markdown("<div style='margin-top:8px'></div>", unsafe_allow_html=True)

# ── Module cards ──────────────────────────────────────────────────────────────
st.markdown("""
<div style="font-size:1.2rem;font-weight:800;color:#1A1A2E;
            margin:24px 0 16px;letter-spacing:-0.01em;">
    Platform Modules
</div>
""", unsafe_allow_html=True)

row1 = st.columns(3)
row2 = st.columns(3)

modules = [
    ("🔍", "Document Search", "Upload your SOP PDF and ask questions in plain English. Results show exact page numbers.", "#1565C0", "Business Analyst · Developer"),
    ("🗺️", "Workflow Maps", "Step-by-step visual flows for every IEP process. See timelines, owners and required documents.", "#0097A7", "Business Analyst · Coordinator"),
    ("⚡", "Rule Engine", "Enter a student profile and instantly see which rules apply, what services are required and why.", "#6A1B9A", "Developer · QA Tester"),
    ("✅", "Compliance Checklist", "Role-specific checklists for every IEP type. Track progress and export for your records.", "#2E7D32", "Coordinator · QA Tester"),
    ("🧪", "Test Cases", "Generate Gherkin, pytest and TestRail test cases from IEP business rules automatically.", "#E65100", "QA Tester · Developer"),
    ("📖", "User Guide", "Step-by-step examples for every role. Business users and IT architects both covered.", "#00838F", "All Roles"),
]

all_cols = row1 + row2
for col, (icon, title, desc, color, roles) in zip(all_cols, modules):
    with col:
        st.markdown(f"""
        <div style="background:white;border-radius:14px;border:1px solid #E8EAF6;
                    border-top:4px solid {color};padding:22px 20px;
                    box-shadow:0 4px 20px rgba(21,101,192,0.06);
                    height:100%;transition:box-shadow 0.2s;margin-bottom:12px;">
            <div style="font-size:1.8rem;margin-bottom:10px;">{icon}</div>
            <div style="font-weight:800;color:#1A1A2E;font-size:1rem;
                        margin-bottom:8px;">{title}</div>
            <div style="color:#546E7A;font-size:0.85rem;line-height:1.6;
                        margin-bottom:14px;">{desc}</div>
            <div style="font-size:0.72rem;color:{color};font-weight:700;
                        letter-spacing:0.03em;text-transform:uppercase;">{roles}</div>
        </div>
        """, unsafe_allow_html=True)

# ── Quick start ───────────────────────────────────────────────────────────────
st.markdown("""
<div style="font-size:1.2rem;font-weight:800;color:#1A1A2E;
            margin:24px 0 16px;letter-spacing:-0.01em;">
    Where to Start?
</div>
""", unsafe_allow_html=True)

r1, r2, r3, r4 = st.columns(4)
roles = [
    ("👩‍💼", "Business Analyst", "Start with Workflow Maps to understand the IEP lifecycle, then use Document Search to look up specific rules.", "#1565C0"),
    ("🧪", "QA Tester", "Go to Test Cases to export Gherkin scenarios, then use the Rule Engine to validate your test coverage.", "#E65100"),
    ("💻", "Developer", "Use the Rule Engine to export JSON business rules, then Document Search to trace rules back to the SOP.", "#6A1B9A"),
    ("🏫", "Special Ed Coordinator", "Start with the Compliance Checklist for your IEP type and role. Use Workflow Maps for process questions.", "#2E7D32"),
]
for col, (icon, role, tip, color) in zip([r1,r2,r3,r4], roles):
    with col:
        st.markdown(f"""
        <div style="background:white;border-radius:12px;padding:18px;
                    border:1px solid #E8EAF6;border-left:4px solid {color};
                    box-shadow:0 2px 12px rgba(0,0,0,0.04);">
            <div style="font-size:1.5rem;margin-bottom:8px;">{icon}</div>
            <div style="font-weight:700;color:{color};font-size:0.9rem;
                        margin-bottom:8px;">{role}</div>
            <div style="color:#546E7A;font-size:0.82rem;line-height:1.6;">{tip}</div>
        </div>
        """, unsafe_allow_html=True)

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("""
<div style="text-align:center;color:#90A4AE;font-size:0.75rem;
            margin-top:40px;padding:16px;border-top:1px solid #E8EAF6;">
    IEP Education Platform · Built on IDEA Federal Guidelines · State Compliance Reference Tool
</div>
""", unsafe_allow_html=True)
