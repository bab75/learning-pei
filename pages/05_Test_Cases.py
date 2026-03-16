"""
Page: Test Cases
Auto-generate BDD Gherkin, pytest stubs and TestRail CSV from IEP business rules.
"""

import streamlit as st, pandas as pd, json, sys
from pathlib import Path
from datetime import datetime
sys.path.insert(0, str(Path(__file__).parent.parent))

st.set_page_config(page_title="Test Cases · IEP Platform", page_icon="🧪", layout="wide")

from utils.theme import apply_theme, page_header, sidebar_branding
from utils.pdf_loader import init_session, auto_load_pdf

apply_theme()
init_session()
sidebar_branding()
auto_load_pdf()

page_header("🧪", "Test Cases", "Auto-generate Gherkin, pytest and TestRail test cases from IEP business rules", "#E65100")

TEST_BANK = {
    "Referral and Intake": [
        {"id":"TC-REF-001","title":"Written referral required","priority":"Critical","rule":"IDEA §300.301",
         "given":"A parent or teacher wishes to refer a student for special education evaluation",
         "when":"The referral is submitted to the CSE",
         "then":"The system must require the referral to be in writing with a date stamp",
         "negative":"A verbal referral alone is not accepted as a valid initiation of the process",
         "role":"CSE Chairperson","type":"Functional"},
        {"id":"TC-REF-002","title":"60-day clock starts on consent","priority":"Critical","rule":"R-001",
         "given":"A valid written referral has been received and processed by the CSE",
         "when":"The parent provides written consent for evaluation",
         "then":"The 60 school-day evaluation clock must begin on the date consent is signed — not the referral date",
         "negative":"Starting the clock on the referral date is a compliance violation",
         "role":"CSE Chairperson","type":"Timing"},
        {"id":"TC-REF-003","title":"Parent notified within 10 school days","priority":"Required","rule":"IDEA §300.321",
         "given":"A referral has been received from a classroom teacher",
         "when":"The CSE processes the referral",
         "then":"The parent must receive written notification of the referral within 10 school days",
         "negative":"Delaying parent notification pending internal review is non-compliant",
         "role":"CSE Chairperson","type":"Timing"},
    ],
    "Evaluation": [
        {"id":"TC-EVAL-001","title":"All suspected disability areas evaluated","priority":"Critical","rule":"IDEA §300.304(c)(4)",
         "given":"A student is referred with suspected autism and learning disabilities",
         "when":"The evaluation team designs the assessment plan",
         "then":"The plan must include assessments for ALL suspected disability areas — both autism and learning disability domains",
         "negative":"Evaluating only one suspected area when multiple are present is a compliance failure",
         "role":"School Psychologist","type":"Functional"},
        {"id":"TC-EVAL-002","title":"Multiple evaluation tools required","priority":"Critical","rule":"IDEA §300.304(b)(2)",
         "given":"A school psychologist is planning an initial evaluation",
         "when":"Assessment instruments are selected",
         "then":"A variety of valid assessment tools must be used — eligibility cannot be based on a single test",
         "negative":"Determining eligibility from one standardized test alone is non-compliant",
         "role":"School Psychologist","type":"Validation"},
        {"id":"TC-EVAL-003","title":"Evaluation completed within 60 school days","priority":"Critical","rule":"R-001",
         "given":"Parent consent for evaluation is signed on Day 0",
         "when":"The evaluation process concludes",
         "then":"All evaluations must be complete and a CSE eligibility meeting must occur by Day 60",
         "negative":"Scheduling the eligibility meeting on Day 61 or later is an IDEA violation",
         "role":"CSE Chairperson","type":"Timing"},
    ],
    "IEP Development": [
        {"id":"TC-IEP-001","title":"Annual goals are measurable","priority":"Critical","rule":"IDEA §300.320(a)(2)",
         "given":"A special education teacher is writing annual goals for a student with a reading deficit",
         "when":"Goals are entered into the IEP document",
         "then":"Each goal must include a measurable target, baseline, timeline and measurement method",
         "negative":"A goal that states only 'improve reading' without measurable criteria is non-compliant",
         "role":"Special Education Teacher","type":"Data Validation"},
        {"id":"TC-IEP-002","title":"Present levels are linked to goals","priority":"Critical","rule":"IDEA §300.320",
         "given":"Present levels document a reading level of 2nd grade equivalent",
         "when":"Annual reading goals are written",
         "then":"Reading goals must reference the 2nd grade baseline and target realistic measurable growth",
         "negative":"A reading goal written at 4th grade level without justification is inconsistent with present levels",
         "role":"Special Education Teacher","type":"Consistency"},
        {"id":"TC-IEP-003","title":"Service delivery grid is complete","priority":"Critical","rule":"IDEA §300.320(a)(4)",
         "given":"The IEP team determines a student needs speech therapy twice per week",
         "when":"Services are entered into the IEP service grid",
         "then":"The entry must include service type, frequency, session duration, setting and start/end dates",
         "negative":"A service listed with frequency only and no duration or setting is incomplete and non-compliant",
         "role":"CSE Chairperson","type":"Data Completeness"},
        {"id":"TC-IEP-004","title":"LRE determination documented","priority":"Critical","rule":"R-003",
         "given":"The CSE recommends a 12:1:1 special class placement",
         "when":"The placement decision is finalized in the IEP",
         "then":"The IEP must document that less restrictive options were considered and explain why they are not appropriate",
         "negative":"Recommending a 12:1:1 class without any LRE analysis in the IEP is non-compliant",
         "role":"CSE","type":"Documentation"},
    ],
    "Parental Rights": [
        {"id":"TC-PAR-001","title":"Prior Written Notice before placement change","priority":"Critical","rule":"R-005",
         "given":"The CSE proposes to change a student from ICT to a 12:1:1 special class",
         "when":"The placement change is decided",
         "then":"Prior Written Notice must be provided to the parent before the change is implemented",
         "negative":"Implementing a placement change without first sending PWN is a procedural IDEA violation",
         "role":"CSE Chairperson","type":"Compliance"},
        {"id":"TC-PAR-002","title":"Procedural Safeguards provided at annual review","priority":"Required","rule":"IDEA §300.504",
         "given":"An annual IEP review meeting is scheduled",
         "when":"The parent attends the meeting",
         "then":"A copy of the Procedural Safeguards must be provided to the parent and documented in meeting records",
         "negative":"Failing to provide Procedural Safeguards at the annual meeting is a documentation gap",
         "role":"CSE Chairperson","type":"Compliance"},
    ],
    "Transition Planning": [
        {"id":"TC-TRANS-001","title":"Transition goals required at age 15","priority":"Critical","rule":"IDEA §300.320(b)",
         "given":"A student is 15 years old during the current IEP year",
         "when":"The IEP is developed or reviewed",
         "then":"The IEP must include measurable post-secondary goals for education, employment and (if applicable) independent living, plus transition services",
         "negative":"An IEP for a student age 15 or older that lacks transition goals is non-compliant",
         "role":"IEP Team","type":"Compliance"},
    ],
}

# ── Controls ──────────────────────────────────────────────────────────────────
c1, c2, c3, c4 = st.columns(4)
with c1: domain_f   = st.selectbox("Domain", ["All"] + list(TEST_BANK.keys()))
with c2: priority_f = st.selectbox("Priority", ["All","Critical","Required"])
with c3: type_f     = st.selectbox("Type", ["All","Functional","Compliance","Timing","Data Validation","Data Completeness","Documentation","Validation","Consistency"])
with c4: fmt        = st.selectbox("Export Format", ["Gherkin BDD","CSV for TestRail","JSON","Python pytest"])

all_tests = [dict(t, domain=d) for d, tests in TEST_BANK.items() for t in tests]
filtered  = [t for t in all_tests
             if (domain_f   == "All" or t["domain"]    == domain_f)
             and (priority_f == "All" or t["priority"] == priority_f)
             and (type_f     == "All" or t["type"]     == type_f)]

# Metrics
m1,m2,m3,m4 = st.columns(4)
for col,(v,l) in zip([m1,m2,m3,m4],[
    (len(all_tests),"Total Cases"),
    (sum(1 for t in all_tests if t["priority"]=="Critical"),"Critical"),
    (len(filtered),"Showing"),
    (len(TEST_BANK),"Domains"),
]):
    with col: st.metric(l, v)

st.markdown(f"### Test Cases — {len(filtered)} shown")
pc = {"Critical":"#C62828","Required":"#1565C0"}

for t in filtered:
    c = pc.get(t["priority"],"#546E7A")
    with st.expander(f"{t['id']}  ·  {t['title']}  ·  {t['priority']}  ·  {t['type']}"):
        g_tab, s_tab, d_tab = st.tabs(["Gherkin", "Structured Table", "Developer Notes"])

        with g_tab:
            st.code(
                f"Feature: {t['domain']}\n\n"
                f"  # {t['id']} | Rule: {t['rule']} | Priority: {t['priority']}\n"
                f"  # Role: {t['role']} | Type: {t['type']}\n\n"
                f"  Scenario: {t['title']}\n"
                f"    Given {t['given']}\n"
                f"    When  {t['when']}\n"
                f"    Then  {t['then']}\n\n"
                f"  Scenario: {t['title']} — Negative Case\n"
                f"    Given {t['given']}\n"
                f"    When  a non-compliant action occurs\n"
                f"    Then  {t['negative']}",
                language="gherkin"
            )
        with s_tab:
            st.markdown(f"""
| Field | Value |
|---|---|
| **Test ID** | `{t['id']}` |
| **Domain** | {t['domain']} |
| **Priority** | {t['priority']} |
| **Rule Reference** | {t['rule']} |
| **Responsible Role** | {t['role']} |
| **Test Type** | {t['type']} |
| **Given (Precondition)** | {t['given']} |
| **When (Action)** | {t['when']} |
| **Then — Pass** | {t['then']} |
| **Then — Fail / Negative** | {t['negative']} |
""")
        with d_tab:
            st.markdown(f"**System Assertion:** Verify that: *{t['then']}*")
            st.markdown(f"**Regression Risk:** {'HIGH — IDEA violation if this fails' if t['priority']=='Critical' else 'MEDIUM — Required compliance item'}")
            st.code(
                f"def test_{t['id'].lower().replace('-','_')}():\n"
                f"    \"\"\"{t['title']} — {t['rule']}\"\"\"\n"
                f"    # Arrange: {t['given']}\n"
                f"    # Act:     {t['when']}\n"
                f"    # Assert:  {t['then']}\n"
                f"    raise NotImplementedError('Implement this test')",
                language="python"
            )

# Export
st.markdown("---")
if st.button(f"Export {len(filtered)} Test Cases as {fmt}", use_container_width=True, type="primary"):
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    if fmt == "CSV for TestRail":
        rows = [{"ID":t["id"],"Domain":t["domain"],"Title":t["title"],"Priority":t["priority"],
                 "Rule":t["rule"],"Role":t["role"],"Type":t["type"],"Given":t["given"],
                 "When":t["when"],"Then":t["then"],"Negative":t["negative"]} for t in filtered]
        st.download_button("Download CSV", pd.DataFrame(rows).to_csv(index=False),
                           f"IEP_TestCases_{ts}.csv","text/csv")
    elif fmt == "JSON":
        st.download_button("Download JSON", json.dumps(filtered, indent=2),
                           f"IEP_TestCases_{ts}.json","application/json")
    elif fmt == "Python pytest":
        lines = ["import pytest\n"]
        for t in filtered:
            lines.append(f"def test_{t['id'].lower().replace('-','_')}():")
            lines.append(f"    \"\"\"{t['title']} — {t['rule']}\"\"\"")
            lines.append(f"    # Given: {t['given']}")
            lines.append(f"    # When:  {t['when']}")
            lines.append(f"    # Then:  {t['then']}")
            lines.append(f"    raise NotImplementedError\n")
        st.download_button("Download .py", "\n".join(lines), f"test_iep_{ts}.py","text/plain")
    else:  # Gherkin
        lines, domain = [], None
        for t in filtered:
            if t["domain"] != domain:
                domain = t["domain"]
                lines.append(f"\nFeature: {domain}\n")
            lines.append(f"  Scenario: {t['title']}\n    # {t['id']} | {t['rule']}")
            lines.append(f"    Given {t['given']}\n    When  {t['when']}\n    Then  {t['then']}\n")
        st.download_button("Download .feature", "\n".join(lines),
                           f"IEP_TestCases_{ts}.feature","text/plain")
