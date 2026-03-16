"""
Page: Compliance Checklist
Role-specific checklists per IEP type. Track, complete and export.
"""

import streamlit as st, pandas as pd, json, sys
from pathlib import Path
from datetime import date, datetime
sys.path.insert(0, str(Path(__file__).parent.parent))

st.set_page_config(page_title="Compliance Checklist · IEP Platform", page_icon="✅", layout="wide")

from utils.theme import apply_theme, page_header, sidebar_branding
from utils.pdf_loader import init_session, auto_load_pdf

apply_theme()
init_session()
sidebar_branding()
auto_load_pdf()

page_header("✅", "Compliance Checklist", "Generate, track and export role-specific IEP compliance checklists", "#2E7D32")

# ── Checklist data ─────────────────────────────────────────────────────────────
ITEMS = {
    "Initial IEP": {
        "CSE Chairperson": [
            ("Prior Written Notice (PWN) sent to parent before meeting","R-005","Critical"),
            ("Written parental consent obtained before evaluation begins","R-004","Critical"),
            ("Meeting notice sent at least 14 days in advance","IDEA §300.322","Required"),
            ("All required IEP team members notified or excused in writing","IDEA §300.321","Required"),
            ("Parent rights / Procedural Safeguards notice provided","IDEA §300.504","Critical"),
            ("Student invited if age 15 or older (transition)","IDEA §300.321(b)","Required"),
        ],
        "School Psychologist": [
            ("Evaluation completed within 60 school days of consent","R-001","Critical"),
            ("All areas of suspected disability assessed","IDEA §300.304","Critical"),
            ("Multiple assessment tools used — not a single test","IDEA §300.304(b)","Critical"),
            ("Assessments are valid and non-discriminatory","IDEA §300.304(c)","Critical"),
            ("Report includes eligibility recommendation","Best Practice","Required"),
        ],
        "Special Education Teacher": [
            ("Present levels of performance documented with current data","IDEA §300.320(a)(1)","Critical"),
            ("All annual goals are measurable with baseline and target","IDEA §300.320(a)(2)","Critical"),
            ("Goals are directly linked to present levels","Best Practice","Required"),
            ("Service delivery grid is complete (frequency, duration, location)","IDEA §300.320(a)(4)","Critical"),
            ("Accommodations and modifications are listed","IDEA §300.320(a)(4)","Required"),
            ("LRE determination and rationale documented","IDEA §300.114","Critical"),
        ],
        "Parent / Guardian": [
            ("Received and understood Prior Written Notice","R-005","Critical"),
            ("Received Procedural Safeguards notice","IDEA §300.504","Critical"),
            ("Provided written consent for evaluation","R-004","Critical"),
            ("Participated in IEP meeting","IDEA §300.321","Required"),
            ("Received copy of completed IEP","IDEA §300.322","Critical"),
        ],
    },
    "Annual Review": {
        "CSE Chairperson": [
            ("Meeting scheduled on or before IEP anniversary date","R-002","Critical"),
            ("Meeting notice sent at least 14 days in advance","IDEA §300.322","Required"),
            ("Prior Written Notice sent if changes proposed","R-005","Required"),
            ("All required team members present or excused in writing","IDEA §300.321","Required"),
        ],
        "Special Education Teacher": [
            ("Progress on all annual goals reviewed and documented","IDEA §300.324(b)","Critical"),
            ("New measurable annual goals written","IDEA §300.320(a)(2)","Critical"),
            ("Present levels updated with current performance data","IDEA §300.320(a)(1)","Critical"),
            ("Services reviewed and updated as appropriate","IDEA §300.324(b)(1)","Required"),
            ("ESY eligibility reviewed and documented","IDEA §300.106","Required"),
        ],
        "Parent / Guardian": [
            ("Participated in annual review meeting","IDEA §300.322","Required"),
            ("Received updated IEP copy","IDEA §300.322(f)","Critical"),
            ("Informed of right to request additional evaluation","IDEA §300.305","Required"),
        ],
    },
    "Reevaluation": {
        "CSE Chairperson": [
            ("Reevaluation conducted within 3 years of last evaluation","R-007","Critical"),
            ("Parent notified of reevaluation process and purpose","IDEA §300.304","Required"),
            ("Written consent obtained if new assessments needed","IDEA §300.300(c)","Critical"),
        ],
        "School Psychologist": [
            ("Existing evaluation data reviewed before new testing","IDEA §300.305(a)","Critical"),
            ("Determination made of what new assessments are needed","IDEA §300.305(b)","Required"),
            ("Continued eligibility determination documented","IDEA §300.305(e)","Critical"),
            ("De-classification notice provided if no longer eligible","IDEA §300.305(e)(2)","Critical"),
        ],
    },
    "Amendment": {
        "CSE Chairperson": [
            ("Amendment need is documented in writing","Best Practice","Required"),
            ("Written parent agreement to waive meeting obtained","IDEA §300.324(a)(4)","Critical"),
            ("Prior Written Notice of amendment provided to parent","R-005","Critical"),
            ("All affected service providers notified of changes","Best Practice","Required"),
        ],
        "Special Education Teacher": [
            ("Specific IEP pages amended and dated","Best Practice","Required"),
            ("Amendment is consistent with existing annual review goals","Best Practice","Required"),
        ],
        "Parent / Guardian": [
            ("Received Prior Written Notice of proposed amendment","R-005","Critical"),
            ("Provided written agreement if meeting is waived","IDEA §300.324(a)(4)","Critical"),
            ("Received copy of amended IEP pages","Best Practice","Required"),
        ],
    },
}

# ── Session init ──────────────────────────────────────────────────────────────
if "checklists" not in st.session_state:
    st.session_state.checklists = {}

# ── Controls ──────────────────────────────────────────────────────────────────
ctrl1, ctrl2, ctrl3 = st.columns([2, 2, 1])
with ctrl1:
    iep_type = st.selectbox("IEP Process Type", list(ITEMS.keys()))
with ctrl2:
    roles_avail = list(ITEMS[iep_type].keys())
    role = st.selectbox("Your Role", roles_avail)
with ctrl3:
    show_filter = st.selectbox("Show", ["All","Critical","Required"])

# Case info
with st.expander("Case Information (optional — used in export)", expanded=False):
    ci1, ci2, ci3 = st.columns(3)
    with ci1:
        student_id = st.text_input("Student ID / OSIS")
        student_name = st.text_input("Student Name")
    with ci2:
        school = st.text_input("School Name")
        cse_date = st.date_input("CSE Meeting Date", date.today())
    with ci3:
        reviewer = st.text_input("Completed By")
        notes = st.text_area("Notes", height=70)

items = ITEMS[iep_type][role]
key  = f"{iep_type}_{role}"
if key not in st.session_state.checklists:
    st.session_state.checklists[key] = [False] * len(items)
state = st.session_state.checklists[key]

# Filter
filtered = [(i, item) for i, item in enumerate(items)
            if show_filter == "All" or item[2] == show_filter]

# Progress
done  = sum(state)
total = len(items)
pct   = int(done / total * 100) if total else 0
pbar_color = "#2E7D32" if pct == 100 else "#1565C0" if pct >= 50 else "#E65100"

st.markdown(f"""
<div style="background:white;border:1px solid #E8EAF6;border-radius:12px;
            padding:16px 20px;margin:16px 0;">
    <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:10px;">
        <span style="font-weight:700;color:#1A1A2E;">{iep_type} — {role}</span>
        <span style="font-weight:700;color:{pbar_color};font-size:1rem;">
            {done}/{total} complete &nbsp; {pct}%</span>
    </div>
    <div style="background:#F0F4FF;border-radius:6px;height:10px;overflow:hidden;">
        <div style="background:linear-gradient(90deg,{pbar_color},{pbar_color}bb);
                    height:100%;width:{pct}%;border-radius:6px;
                    transition:width 0.4s ease;"></div>
    </div>
    {'<div style="color:#2E7D32;font-weight:700;font-size:0.85rem;margin-top:8px;">✅ All items complete!</div>' if pct == 100 else ''}
</div>
""", unsafe_allow_html=True)

# Checklist items
priority_colors = {"Critical":("#FFEBEE","#C62828"),"Required":("#E3F2FD","#1565C0"),"Recommended":("#E8F5E9","#2E7D32")}

st.markdown("### Checklist")
for idx, (task, rule_ref, priority) in filtered:
    bg, fg = priority_colors.get(priority, ("#F0F4FF","#1565C0"))
    cb_col, task_col = st.columns([1, 11])
    with cb_col:
        checked = st.checkbox("", value=state[idx], key=f"cb_{key}_{idx}")
        if checked != state[idx]:
            st.session_state.checklists[key][idx] = checked
            st.rerun()
    with task_col:
        done_style = "text-decoration:line-through;color:#B0BEC5;" if state[idx] else "color:#1A1A2E;"
        st.markdown(f"""
        <div style="display:flex;align-items:center;gap:10px;padding:6px 0;min-height:36px;">
            <div style="{done_style}font-size:0.9rem;flex:1;">{task}</div>
            <span style="background:{bg};color:{fg};border-radius:20px;padding:2px 10px;
                         font-size:0.7rem;font-weight:700;white-space:nowrap;">{priority}</span>
            <span style="color:#90A4AE;font-size:0.75rem;font-family:'JetBrains Mono',monospace;
                         white-space:nowrap;">{rule_ref}</span>
        </div>
        """, unsafe_allow_html=True)

# Actions
st.markdown("---")
a1, a2, a3, a4 = st.columns(4)
with a1:
    if st.button("Mark All Complete", use_container_width=True):
        st.session_state.checklists[key] = [True]*len(items)
        st.rerun()
with a2:
    if st.button("Clear All", use_container_width=True):
        st.session_state.checklists[key] = [False]*len(items)
        st.rerun()
with a3:
    rows = [{"Student ID":student_id,"Name":student_name,"School":school,
             "CSE Date":str(cse_date),"IEP Type":iep_type,"Role":role,
             "Task":t,"Rule":r,"Priority":p,
             "Complete":"Yes" if state[i] else "No","By":reviewer,"Notes":notes}
            for i,(t,r,p) in enumerate(items)]
    st.download_button("Export CSV", pd.DataFrame(rows).to_csv(index=False),
                       f"Checklist_{iep_type}_{role}.csv".replace(" ","_"), "text/csv",
                       use_container_width=True)
with a4:
    export_json = {"generated":datetime.now().isoformat(),
                   "case":{"id":student_id,"name":student_name,"school":school,"date":str(cse_date),"by":reviewer},
                   "checklist":{"type":iep_type,"role":role,"done":f"{done}/{total}",
                                "items":[{"task":t,"rule":r,"priority":p,"complete":state[i]}
                                         for i,(t,r,p) in enumerate(items)]}}
    st.download_button("Export JSON", json.dumps(export_json,indent=2),
                       f"Checklist_{iep_type}.json".replace(" ","_"), "application/json",
                       use_container_width=True)

# All roles summary
st.markdown("---")
st.markdown("### All Roles Summary")
summary = []
for r in roles_avail:
    k2  = f"{iep_type}_{r}"
    its = ITEMS[iep_type][r]
    if k2 not in st.session_state.checklists:
        st.session_state.checklists[k2] = [False]*len(its)
    s2 = st.session_state.checklists[k2]
    d2 = sum(s2)
    cr = sum(1 for _,_,p in its if p=="Critical")
    cd = sum(1 for i,(_,_,p) in enumerate(its) if p=="Critical" and s2[i])
    summary.append({"Role":r,"Completed":f"{d2}/{len(its)}",
                    "Percent":f"{int(d2/len(its)*100)}%","Critical":f"{cd}/{cr}",
                    "Status":"✅ Done" if d2==len(its) else ("🔄 In Progress" if d2>0 else "⬜ Not Started")})
st.dataframe(pd.DataFrame(summary), use_container_width=True, hide_index=True)
