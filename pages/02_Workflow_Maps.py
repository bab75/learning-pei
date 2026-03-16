"""
Page: Workflow Maps
Visual IEP lifecycle flows for Initial, Annual Review, Reevaluation and Amendment.
"""

import streamlit as st
import sys, pandas as pd
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

st.set_page_config(page_title="Workflow Maps · IEP Platform", page_icon="🗺️", layout="wide")

from utils.theme import apply_theme, page_header, sidebar_branding
from utils.pdf_loader import init_session, auto_load_pdf

apply_theme()
init_session()
sidebar_branding()
auto_load_pdf()

page_header("🗺️", "Workflow Maps", "Step-by-step visual guide to every IEP process type", "#0097A7")

# ── Data ──────────────────────────────────────────────────────────────────────
WORKFLOWS = {
    "Initial IEP": {
        "color": "#1565C0", "icon": "🆕",
        "summary": "The complete process from first referral to placement. IDEA mandates 60 school days from parent consent to IEP implementation.",
        "law": "IDEA § 300.301",
        "steps": [
            {"name":"Referral Received","days":"Day 0","owner":"Parent / Teacher / CSE","color":"#E3F2FD","accent":"#1565C0",
             "what":"A written referral is submitted to the Committee on Special Education (CSE). This starts the process but NOT the 60-day clock.",
             "docs":["Written referral letter","CSE-1 Referral Form"],
             "tests":["Referral must be in writing — verbal referral is not valid","Date stamp is recorded on day of receipt","Parent is notified within 5 school days"]},
            {"name":"Parent Notification & Consent","days":"Days 1–10","owner":"CSE Chairperson","color":"#E8EAF6","accent":"#3949AB",
             "what":"School notifies parent and requests written consent before any evaluation begins. Consent is specific to this evaluation only.",
             "docs":["Prior Written Notice (PWN)","Parent Consent Form"],
             "tests":["PWN includes all legally required elements","No evaluation begins before written consent is received","Consent for evaluation is NOT consent for placement"]},
            {"name":"Comprehensive Evaluation","days":"Days 10–40","owner":"Multi-Disciplinary Team","color":"#E0F7FA","accent":"#0097A7",
             "what":"Full evaluation across all areas of suspected disability. Must include psychological, educational, and any relevant specialist assessments.",
             "docs":["Psychoeducational Report","Speech/Language Evaluation","OT/PT Evaluation (if applicable)","Social History"],
             "tests":["All areas of suspected disability are evaluated — not just one","More than one assessment tool is used","Qualified evaluators used for each domain","Evaluation completed within 60-day window"]},
            {"name":"Eligibility Determination","days":"Days 40–50","owner":"CSE Team","color":"#EDE7F6","accent":"#6A1B9A",
             "what":"CSE meets to review evaluation data and vote on whether the student qualifies under one of 13 IDEA disability categories. Parent is a required team member.",
             "docs":["Eligibility Summary","Classification Determination Letter"],
             "tests":["Student meets criteria for at least one IDEA category","Parent participated in the eligibility meeting","Decision is documented in meeting minutes","Parent receives copy of eligibility determination"]},
            {"name":"IEP Development","days":"Days 50–58","owner":"IEP Team","color":"#E8F5E9","accent":"#2E7D32",
             "what":"Team writes the IEP document: present levels, measurable annual goals, special education and related services, accommodations, and LRE placement recommendation.",
             "docs":["IEP Document","Present Levels of Performance","Annual Goals","Service Delivery Grid","Accommodation List"],
             "tests":["Present levels based on current evaluation data","All goals are measurable with baseline and target","Service frequency, duration and location all specified","LRE determination is documented with rationale"]},
            {"name":"Placement & Implementation","days":"Day 60","owner":"Principal / CSE","color":"#FFF8E1","accent":"#F57F17",
             "what":"Parent receives the IEP and Prior Written Notice of placement. Services must begin immediately. IEP is in effect at the start of each school year.",
             "docs":["Final IEP Copy to Parent","Prior Written Notice of Placement","Parent Rights Notice"],
             "tests":["IEP implemented within 60 school days of parent consent","Parent receives IEP copy same day","All service providers have access to IEP goals","Prior Written Notice is sent before placement begins"]},
        ]
    },
    "Annual Review": {
        "color": "#0097A7", "icon": "📅",
        "summary": "IEP must be reviewed at least once every 12 months. Meeting must occur on or before the IEP anniversary date.",
        "law": "IDEA § 300.324(b)",
        "steps": [
            {"name":"Review Progress Data","days":"30 days before","owner":"Special Ed Teacher","color":"#E0F7FA","accent":"#0097A7",
             "what":"Collect all progress data on current annual goals. Determine which goals were met, partially met or not met.",
             "docs":["Progress Reports","Data Collection Sheets","Teacher Observations"],
             "tests":["Progress data collected for all measurable goals","Parent notified of upcoming annual review"]},
            {"name":"Schedule Meeting","days":"14 days before","owner":"CSE Chairperson","color":"#E8EAF6","accent":"#3949AB",
             "what":"Send written meeting notice to all required team members. Parent must be invited. Notice must allow reasonable time to attend.",
             "docs":["Meeting Notice","Parent Invitation Letter"],
             "tests":["Written notice sent at least 14 days before meeting","Notice includes meeting purpose, date, time, location","Parent informed of right to bring others to meeting"]},
            {"name":"Annual Review Meeting","days":"On or before anniversary","owner":"Full IEP Team","color":"#EDE7F6","accent":"#6A1B9A",
             "what":"Team reviews current IEP, discusses progress on goals, evaluates continued eligibility, and writes a new IEP for the next year.",
             "docs":["Updated IEP","Meeting Minutes","New Service Grid"],
             "tests":["Meeting held on or before anniversary date","All required members present or excused in writing","New measurable annual goals are written","Continued eligibility discussed and documented"]},
            {"name":"Implement New IEP","days":"Day of meeting","owner":"All Service Providers","color":"#E8F5E9","accent":"#2E7D32",
             "what":"New IEP takes effect immediately. All providers notified and given access to updated document.",
             "docs":["IEP Distribution Log","Provider Acknowledgment"],
             "tests":["New IEP sent to all service providers same day","Parent receives copy at or before meeting ends"]},
        ]
    },
    "Reevaluation": {
        "color": "#6A1B9A", "icon": "🔄",
        "summary": "Required every 3 years (triennial) OR when a parent or teacher requests one. Reviews whether student still has a disability.",
        "law": "IDEA § 300.303",
        "steps": [
            {"name":"Determine Need for Reeval","days":"3-year mark","owner":"CSE","color":"#EDE7F6","accent":"#6A1B9A",
             "what":"CSE must reevaluate at least every 3 years. Can also be triggered by parent or teacher request at any time.",
             "docs":["Reevaluation Notice"],
             "tests":["Reevaluation conducted within 3 years of last evaluation","Parent notified of right to request reevaluation at any time"]},
            {"name":"Review Existing Data","days":"Days 1–15","owner":"CSE Team","color":"#E3F2FD","accent":"#1565C0",
             "what":"Before any new testing, review all existing data: prior evaluations, classroom observations, teacher reports, parent input.",
             "docs":["Existing Data Review Summary","Parent Input Questionnaire"],
             "tests":["All prior evaluation data reviewed","Parent input solicited in writing","Determination of what new assessments are needed"]},
            {"name":"Obtain Consent (if new testing)","days":"Days 15–25","owner":"Parent","color":"#FFF8E1","accent":"#F57F17",
             "what":"If new assessments are needed, written parental consent must be obtained. If reviewing existing data only, consent is not required but parent must be notified.",
             "docs":["Consent for Reevaluation Form"],
             "tests":["Written consent obtained before any new assessments","Parent notified even when new testing is not required"]},
            {"name":"Conduct New Assessments","days":"Days 25–50","owner":"Evaluators","color":"#E0F7FA","accent":"#0097A7",
             "what":"Administer only the assessments identified as necessary. Must cover all areas related to the student's disability.",
             "docs":["Updated Evaluation Reports"],
             "tests":["Only necessary assessments are conducted","Results compared to prior evaluation data"]},
            {"name":"Eligibility Meeting","days":"Days 50–60","owner":"CSE","color":"#E8F5E9","accent":"#2E7D32",
             "what":"Review reevaluation results. Determine if student still has a disability. Update IEP if eligible, or issue de-classification notice.",
             "docs":["Updated Eligibility Determination","Revised IEP or De-Classification Notice"],
             "tests":["Eligibility re-determined based on current data","De-classification includes 1-year transition services if applicable","Parent receives written notice of outcome"]},
        ]
    },
    "Amendment": {
        "color": "#E65100", "icon": "✏️",
        "summary": "Changes to an IEP between annual reviews. Can be done with or without a meeting if parent agrees in writing.",
        "law": "IDEA § 300.324(a)(4)",
        "steps": [
            {"name":"Identify the Change Needed","days":"As needed","owner":"Parent or School","color":"#FBE9E7","accent":"#E65100",
             "what":"Either the parent or school identifies a change needed to the current IEP before the next annual review.",
             "docs":["Amendment Request Documentation"],
             "tests":["Amendment need is documented in writing","Change does not require a full annual review meeting"]},
            {"name":"Parent Agreement","days":"Days 1–5","owner":"Parent","color":"#FFF8E1","accent":"#F57F17",
             "what":"Parent must be informed of the proposed change and agree in writing. A meeting may be waived only with explicit written parent agreement.",
             "docs":["Written Agreement to Waive Meeting","Prior Written Notice"],
             "tests":["Parent agreement is in writing before change is made","Prior Written Notice provided to parent","Parent rights notice included with amendment documents"]},
            {"name":"Document and Distribute","days":"Days 5–10","owner":"CSE","color":"#E8F5E9","accent":"#2E7D32",
             "what":"IEP is amended in writing. All affected service providers are notified. Parent receives a copy of the amended pages.",
             "docs":["Amended IEP Pages","Provider Notification Log"],
             "tests":["Amendment is specific, dated and signed","All affected providers notified within 5 days","Parent receives copy of amended IEP pages only"]},
        ]
    },
}

# ── Controls ──────────────────────────────────────────────────────────────────
ctrl1, ctrl2 = st.columns([2, 1])
with ctrl1:
    wf_options = {f"{v['icon']} {k}": k for k, v in WORKFLOWS.items()}
    selected_label = st.selectbox("Select IEP Process Type", list(wf_options.keys()))
    selected = wf_options[selected_label]

with ctrl2:
    view = st.radio("View Mode", ["Step by Step", "Summary Table", "QA Test Cases"], horizontal=True)

wf   = WORKFLOWS[selected]
color = wf["color"]

# Summary banner
st.markdown(f"""
<div style="background:white;border-radius:12px;border:1px solid #E8EAF6;
            border-left:5px solid {color};padding:16px 20px;margin:12px 0 24px;
            display:flex;align-items:flex-start;gap:16px;">
    <div style="font-size:2rem;">{wf['icon']}</div>
    <div>
        <div style="font-weight:700;color:#1A1A2E;font-size:1rem;">{selected}</div>
        <div style="color:#546E7A;font-size:0.88rem;margin-top:4px;line-height:1.6;">
            {wf['summary']}</div>
        <div style="margin-top:8px;">
            <span style="background:{color}18;color:{color};border-radius:4px;
                         padding:2px 10px;font-size:0.75rem;font-weight:700;
                         font-family:'JetBrains Mono',monospace;">{wf['law']}</span>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# ── STEP BY STEP VIEW ─────────────────────────────────────────────────────────
if view == "Step by Step":
    for i, step in enumerate(wf["steps"]):
        conn_col, content_col = st.columns([1, 12])
        with conn_col:
            st.markdown(f"""
            <div style="display:flex;flex-direction:column;align-items:center;">
                <div style="width:36px;height:36px;border-radius:50%;
                            background:{step['accent']};color:white;
                            display:flex;align-items:center;justify-content:center;
                            font-weight:800;font-size:0.9rem;flex-shrink:0;">{i+1}</div>
                {f'<div style="width:2px;height:40px;background:{step["accent"]}40;margin-top:4px;"></div>' if i < len(wf["steps"])-1 else ''}
            </div>
            """, unsafe_allow_html=True)

        with content_col:
            with st.expander(
                f"{step['name']}   ·   {step['days']}   ·   Owner: {step['owner']}",
                expanded=(i == 0)
            ):
                d1, d2 = st.columns(2)
                with d1:
                    st.markdown(f"""
                    <div style="background:{step['color']};border-radius:10px;
                                padding:16px;margin-bottom:12px;">
                        <div style="font-weight:700;color:{step['accent']};
                                    font-size:0.85rem;margin-bottom:6px;">
                            What Happens</div>
                        <div style="color:#37474F;font-size:0.88rem;line-height:1.7;">
                            {step['what']}</div>
                    </div>
                    """, unsafe_allow_html=True)

                    st.markdown("**Required Documents**")
                    for doc in step["docs"]:
                        st.markdown(f"""
                        <div style="background:white;border:1px solid #E8EAF6;
                                    border-radius:6px;padding:6px 12px;margin:3px 0;
                                    font-size:0.85rem;color:#37474F;">
                            📄 {doc}</div>
                        """, unsafe_allow_html=True)

                with d2:
                    st.markdown("**QA Acceptance Criteria**")
                    for t in step["tests"]:
                        st.markdown(f"""
                        <div style="background:#F1F8E9;border:1px solid #C5E1A5;
                                    border-radius:6px;padding:7px 12px;margin:3px 0;
                                    font-size:0.83rem;color:#33691E;">
                            ✓ {t}</div>
                        """, unsafe_allow_html=True)

# ── SUMMARY TABLE VIEW ────────────────────────────────────────────────────────
elif view == "Summary Table":
    rows = [{
        "Step": i+1,
        "Phase": s["name"],
        "Timeline": s["days"],
        "Owner": s["owner"],
        "Key Documents": " | ".join(s["docs"]),
        "Test Count": len(s["tests"]),
    } for i, s in enumerate(wf["steps"])]
    st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)

# ── TEST CASES VIEW ───────────────────────────────────────────────────────────
else:
    st.markdown("### Generated Test Cases")
    st.caption("Copy these into Jira, TestRail, Azure DevOps, or any test management system.")
    tc = 0
    for step in wf["steps"]:
        st.markdown(f"**{step['name']}** &nbsp; `{step['days']}`")
        for test in step["tests"]:
            tc += 1
            st.code(
                f"TC-{tc:03d}: {selected} — {step['name']}\n"
                f"Given : Student is in the {step['name']} phase\n"
                f"When  : The IEP team processes this step\n"
                f"Then  : {test}",
                language="gherkin"
            )
    rows = [{"ID": f"TC-{i+1:03d}", "Process": selected, "Phase": s["name"],
             "Timeline": s["days"], "Owner": s["owner"], "Test": t}
            for i, step_i in enumerate(range(sum(len(s["tests"]) for s in wf["steps"])))
            for j, s in enumerate(wf["steps"]) for k, t in enumerate(s["tests"])
            if sum(len(wf["steps"][x]["tests"]) for x in range(j)) + k == step_i]

    # simpler export
    all_rows = []
    n = 0
    for s in wf["steps"]:
        for t in s["tests"]:
            n += 1
            all_rows.append({"ID": f"TC-{n:03d}", "Process": selected,
                             "Phase": s["name"], "Timeline": s["days"],
                             "Owner": s["owner"], "Test Criterion": t})
    if all_rows:
        csv = pd.DataFrame(all_rows).to_csv(index=False)
        st.download_button(
            f"Download {n} Test Cases as CSV",
            csv,
            file_name=f"IEP_{selected.replace(' ','_')}_TestCases.csv",
            mime="text/csv",
        )
