"""
Page: Rule Engine
Student profile → triggered business rules → required services, documents and timelines.
"""

import streamlit as st, json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

st.set_page_config(page_title="Rule Engine · IEP Platform", page_icon="⚡", layout="wide")

from utils.theme import apply_theme, page_header, sidebar_branding
from utils.pdf_loader import init_session, auto_load_pdf

apply_theme()
init_session()
sidebar_branding()
auto_load_pdf()

page_header("⚡", "Rule Engine", "Configure a student profile to see all applicable IEP rules, required services and documents", "#6A1B9A")

# ── Data ──────────────────────────────────────────────────────────────────────
RULES = {
    "R-001": {"name":"60-Day Evaluation Timeline","law":"IDEA §300.301(c)(1)",
               "trigger":"Parent consent for initial evaluation received",
               "outcome":"Evaluation must be completed within 60 school days of receiving consent",
               "exceptions":["Parent repeatedly fails to make child available","Child transfers during evaluation"]},
    "R-002": {"name":"Annual Review Requirement","law":"IDEA §300.324(b)",
               "trigger":"Student has an active IEP",
               "outcome":"IEP must be reviewed at least once every 12 months",
               "exceptions":["Parent and school agree to revise IEP without meeting"]},
    "R-003": {"name":"Least Restrictive Environment","law":"IDEA §300.114",
               "trigger":"Any placement decision",
               "outcome":"Student must be educated in the least restrictive environment appropriate to their needs",
               "exceptions":["Nature/severity of disability requires more restrictive setting — must be documented"]},
    "R-004": {"name":"Parental Consent Required","law":"IDEA §300.300",
               "trigger":"Initial evaluation OR initial placement",
               "outcome":"Written informed consent must be obtained before evaluation and before initial placement",
               "exceptions":["Annual review does not require new consent","Amendment with written parent agreement"]},
    "R-005": {"name":"Prior Written Notice (PWN)","law":"IDEA §300.503",
               "trigger":"School proposes or refuses any action regarding identification, evaluation or placement",
               "outcome":"PWN must be provided in reasonable time before action is taken",
               "exceptions":[]},
    "R-006": {"name":"Transition Planning Required","law":"IDEA §300.320(b)",
               "trigger":"Student is age 15 or older (some states age 14)",
               "outcome":"IEP must include measurable post-secondary goals and transition services",
               "exceptions":[]},
    "R-007": {"name":"Triennial Reevaluation","law":"IDEA §300.303",
               "trigger":"3 years since last evaluation OR parent/teacher request",
               "outcome":"Full reevaluation must be conducted to determine continued eligibility",
               "exceptions":["Parent and school agree reevaluation is unnecessary"]},
}

DISABILITY_MAP = {
    "Autism Spectrum Disorder": {
        "color":"#1565C0",
        "evals":["Psychological","Educational","Speech/Language","Occupational Therapy","Behavioral Assessment (ADOS-2 recommended)"],
        "services":["Special Education Instruction","Speech/Language Therapy","Occupational Therapy","ABA Therapy (if appropriate)","Counseling"],
        "flags":["Consider Behavioral Intervention Plan (BIP)","Assess communication across all environments","Evaluate sensory processing needs","Consider Extended School Year (ESY)"],
    },
    "Learning Disability": {
        "color":"#0097A7",
        "evals":["Psychological","Educational Achievement","Processing Speed Assessment","Working Memory Assessment","Reading/Math Diagnostics"],
        "services":["Resource Room","Integrated Co-Teaching (ICT)","Consultant Teacher","Reading Specialist"],
        "flags":["Document specific deficit areas (reading, math, writing)","Include RTI data if available","Address assistive technology needs","Specify homework and testing accommodations"],
    },
    "Speech/Language Impairment": {
        "color":"#2E7D32",
        "evals":["Speech/Language Evaluation (ASHA-certified SLP)","Hearing Screening","Educational Assessment"],
        "services":["Speech/Language Therapy — individual","Speech/Language Therapy — group"],
        "flags":["Distinguish between articulation, language and fluency goals","Specify exact frequency and session duration","Consider AAC devices if communication is severely impaired"],
    },
    "Emotional Disturbance": {
        "color":"#E65100",
        "evals":["Psychological","Social History","Psychiatric Evaluation (if applicable)","Educational Assessment"],
        "services":["Counseling","Social Work Services","Special Class (if needed)","Crisis Intervention Plan"],
        "flags":["FBA required if BIP is developed","Document manifestation determination if discipline is involved","Consider trauma-informed approaches","Coordinate with mental health providers"],
    },
    "Intellectual Disability": {
        "color":"#6A1B9A",
        "evals":["Psychological (IQ testing)","Adaptive Behavior Assessment (Vineland/ABAS)","Educational","Medical Documentation"],
        "services":["Special Class","Life Skills Instruction","Vocational Training (age 14+)","Community-Based Instruction"],
        "flags":["Adaptive behavior assessed across multiple settings","Transition planning begins at age 14–15","Consider community-based instruction options"],
    },
    "Other Health Impairment (incl. ADHD)": {
        "color":"#00838F",
        "evals":["Medical Documentation from Physician","Educational Assessment","Psychological (if applicable)"],
        "services":["Accommodations-based support","Resource Room (if needed)","Related health services"],
        "flags":["Medical diagnosis documentation required","Address how condition impacts educational performance","Consider 504 Plan if special ed services not required","Medication management plan if applicable"],
    },
}

PLACEMENTS = [
    ("General Education only",1),("Consultant Teacher in Gen Ed",2),
    ("Resource Room (part-time pull-out)",3),("Integrated Co-Teaching (ICT)",3),
    ("Special Class 12:1:1",4),("Special Class 8:1:1",5),
    ("Special Class 6:1:1",6),("Special Day School",7),("Residential Placement",8),
]

# ── Layout ────────────────────────────────────────────────────────────────────
tab_profile, tab_rules, tab_lre = st.tabs(["Student Profile & Output", "All Business Rules", "LRE Continuum"])

# ── TAB 1 ─────────────────────────────────────────────────────────────────────
with tab_profile:
    st.markdown("### Configure Student Profile")
    st.caption("Fill in the fields below. The rule engine will instantly show all applicable rules, required evaluations and recommended services.")

    c1, c2, c3 = st.columns(3)
    with c1:
        iep_type   = st.selectbox("IEP Process Stage", ["Initial Evaluation","Annual Review","Reevaluation","Amendment"])
        disability = st.selectbox("Disability Classification", list(DISABILITY_MAP.keys()))
        grade      = st.selectbox("Grade Level", ["PreK","K","1","2","3","4","5","6","7","8","9","10","11","12"])
    with c2:
        age        = st.number_input("Student Age", 3, 21, 10)
        placement  = st.selectbox("Current/Proposed Placement", [p[0] for p in PLACEMENTS])
        consent    = st.checkbox("Parent Consent on File", value=True)
    with c3:
        has_bip    = st.checkbox("Has Behavioral Intervention Plan (BIP)")
        esy        = st.checkbox("Extended School Year (ESY) Consideration")
        transition = age >= 15
        if transition:
            st.warning("Transition planning required — student is age 15 or older.")

    run = st.button("Generate Rule Engine Output", type="primary", use_container_width=True)

    if run:
        dm = DISABILITY_MAP[disability]
        placement_level = next(p[1] for p in PLACEMENTS if p[0] == placement)
        st.markdown("---")

        # Required evaluations
        st.markdown("#### Required Evaluations")
        ecols = st.columns(len(dm["evals"]))
        for col, ev in zip(ecols, dm["evals"]):
            with col:
                st.markdown(f"""
                <div style="background:{dm['color']}12;border:1.5px solid {dm['color']}40;
                            border-radius:8px;padding:10px;text-align:center;
                            font-size:0.82rem;font-weight:600;color:{dm['color']};">
                    {ev}</div>
                """, unsafe_allow_html=True)

        # Recommended services
        st.markdown("#### Recommended Services")
        scols = st.columns(min(len(dm["services"]), 4))
        for i, svc in enumerate(dm["services"]):
            with scols[i % len(scols)]:
                st.markdown(f"""
                <div style="background:#E8F5E9;border:1px solid #A5D6A7;border-radius:8px;
                            padding:10px 14px;font-size:0.85rem;font-weight:600;
                            color:#2E7D32;margin-bottom:8px;">✓ {svc}</div>
                """, unsafe_allow_html=True)

        # Key flags
        st.markdown("#### Important Flags for This Profile")
        for flag in dm["flags"]:
            st.markdown(f"""
            <div style="background:#FFF8E1;border-left:3px solid #F57F17;border-radius:6px;
                        padding:8px 14px;margin:4px 0;font-size:0.85rem;color:#E65100;">
                ⚠️ {flag}</div>
            """, unsafe_allow_html=True)
        if transition:
            st.markdown(f"""
            <div style="background:#FFEBEE;border-left:3px solid #C62828;border-radius:6px;
                        padding:8px 14px;margin:4px 0;font-size:0.85rem;color:#C62828;">
                🔴 TRANSITION PLANNING IS MANDATORY — Include post-secondary goals in this IEP</div>
            """, unsafe_allow_html=True)
        if has_bip:
            st.markdown(f"""
            <div style="background:#FFEBEE;border-left:3px solid #C62828;border-radius:6px;
                        padding:8px 14px;margin:4px 0;font-size:0.85rem;color:#C62828;">
                🔴 FBA must be conducted BEFORE the BIP is developed — verify documentation</div>
            """, unsafe_allow_html=True)

        # Triggered rules
        st.markdown("#### Triggered Business Rules")
        triggered = ["R-002","R-003","R-005"]
        if iep_type == "Initial Evaluation": triggered = ["R-001","R-004"] + triggered
        if not consent:                      triggered.append("R-004")
        if transition:                        triggered.append("R-006")
        if iep_type == "Reevaluation":        triggered.append("R-007")

        for rid in dict.fromkeys(triggered):
            r = RULES[rid]
            st.markdown(f"""
            <div style="background:white;border:1px solid #E8EAF6;border-left:4px solid #1565C0;
                        border-radius:8px;padding:16px;margin:6px 0;">
                <div style="display:flex;gap:10px;margin-bottom:6px;align-items:center;">
                    <span style="background:#E3F2FD;color:#1565C0;border-radius:4px;
                                 padding:2px 8px;font-size:0.72rem;font-weight:700;
                                 font-family:'JetBrains Mono',monospace;">{rid}</span>
                    <span style="background:#F3E5F5;color:#6A1B9A;border-radius:4px;
                                 padding:2px 8px;font-size:0.72rem;font-weight:600;
                                 font-family:'JetBrains Mono',monospace;">{r['law']}</span>
                </div>
                <div style="font-weight:700;color:#1A1A2E;margin-bottom:4px;">{r['name']}</div>
                <div style="color:#546E7A;font-size:0.88rem;">{r['outcome']}</div>
                {f'<div style="color:#F57F17;font-size:0.82rem;margin-top:6px;">⚠️ Exceptions: {"; ".join(r["exceptions"])}</div>' if r["exceptions"] else ''}
            </div>
            """, unsafe_allow_html=True)

        # Export
        export = {
            "student_profile": {"iep_type":iep_type,"disability":disability,"grade":grade,
                                  "age":age,"placement":placement,"consent_on_file":consent,
                                  "has_bip":has_bip,"esy":esy,"transition_required":transition},
            "required_evaluations": dm["evals"],
            "recommended_services": dm["services"],
            "flags": dm["flags"],
            "triggered_rules": {rid: RULES[rid]["name"] for rid in dict.fromkeys(triggered)},
        }
        st.download_button("Download Rule Output as JSON", json.dumps(export, indent=2),
                           file_name="IEP_Rule_Output.json", mime="application/json")

# ── TAB 2 ─────────────────────────────────────────────────────────────────────
with tab_rules:
    st.markdown("### All Business Rules Reference")
    search = st.text_input("Filter rules", placeholder="Type rule name, law or keyword…")
    for rid, rule in RULES.items():
        if search and search.lower() not in json.dumps(rule).lower():
            continue
        with st.expander(f"{rid} · {rule['name']} · {rule['law']}"):
            st.markdown(f"**Trigger:** {rule['trigger']}")
            st.markdown(f"**Required Outcome:** {rule['outcome']}")
            if rule["exceptions"]:
                st.markdown("**Exceptions:**")
                for ex in rule["exceptions"]:
                    st.markdown(f"- {ex}")

# ── TAB 3 ─────────────────────────────────────────────────────────────────────
with tab_lre:
    st.markdown("### Least Restrictive Environment (LRE) Continuum")
    st.info("IDEA requires students be educated in the **least restrictive environment** appropriate for their needs. More restrictive placements require documented justification.")
    colors = {1:"#2E7D32",2:"#388E3C",3:"#1565C0",4:"#0097A7",5:"#F57F17",6:"#E65100",7:"#C62828",8:"#880E4F"}
    for name, level in PLACEMENTS:
        c = colors[level]
        bar = "█" * level + "░" * (8-level)
        st.markdown(f"""
        <div style="background:white;border:1px solid #E8EAF6;border-left:5px solid {c};
                    border-radius:8px;padding:14px 18px;margin:6px 0;
                    display:flex;align-items:center;gap:20px;">
            <span style="font-family:'JetBrains Mono',monospace;color:{c};
                         font-size:0.9rem;min-width:90px;">{bar}</span>
            <div>
                <span style="font-weight:700;color:#1A1A2E;">{name}</span>
                <span style="color:#90A4AE;font-size:0.8rem;margin-left:8px;">
                    Restrictiveness level {level}/8</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
