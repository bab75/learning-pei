"""
Page: Document Search
Upload or auto-load SOP PDF. Ask questions. Results show page numbers via dropdown.
"""

import streamlit as st
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

st.set_page_config(page_title="Document Search · IEP Platform", page_icon="🔍", layout="wide")

from utils.theme import apply_theme, page_header, sidebar_branding
from utils.pdf_loader import (
    init_session, auto_load_pdf, extract_text, chunk_pages,
    keyword_search, highlight_text
)

apply_theme()
init_session()
sidebar_branding()
auto_load_pdf()

page_header("🔍", "Document Search", "Ask plain-English questions about your IEP SOP document", "#1565C0")

# ── Suggested questions data ──────────────────────────────────────────────────
SUGGESTED = [
    "What is the 60-day evaluation timeline?",
    "When is parental consent required?",
    "What are the eligibility criteria for classification?",
    "How often must an IEP be reviewed annually?",
    "What related services must be documented in the IEP?",
    "What is the Least Restrictive Environment (LRE)?",
    "What triggers a reevaluation?",
    "What must be included in Present Levels of Performance?",
    "What is Prior Written Notice (PWN)?",
    "What happens if a parent disagrees with placement?",
    "What is a Functional Behavioral Assessment (FBA)?",
    "When is a Behavioral Intervention Plan (BIP) required?",
]

left, right = st.columns([1, 2], gap="large")

# ── LEFT panel ────────────────────────────────────────────────────────────────
with left:

    # Document status
    if st.session_state.doc_loaded:
        st.markdown(f"""
        <div style="background:#E8F5E9;border:1px solid #A5D6A7;border-radius:10px;
                    padding:16px;margin-bottom:20px;">
            <div style="font-weight:700;color:#2E7D32;font-size:0.9rem;margin-bottom:4px;">
                ✅ Document Loaded
            </div>
            <div style="color:#388E3C;font-size:0.82rem;">
                {st.session_state.doc_name}<br>
                {len(st.session_state.doc_pages)} pages &nbsp;·&nbsp;
                {len(st.session_state.doc_chunks)} sections
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style="background:#FFF8E1;border:1px solid #FFE082;border-radius:10px;
                    padding:16px;margin-bottom:20px;">
            <div style="font-weight:700;color:#F57F17;font-size:0.9rem;margin-bottom:4px;">
                ⚠️ No Document Loaded
            </div>
            <div style="color:#F9A825;font-size:0.82rem;">
                Upload your IEP SOP PDF below, or place it in the docs/ folder to auto-load.
            </div>
        </div>
        """, unsafe_allow_html=True)

    # Upload widget
    st.markdown("**Upload SOP Document**")
    uploaded = st.file_uploader(
        "IEP SOP PDF (up to 80 pages)",
        type=["pdf"],
        help="Upload your IEP Standard Operating Procedures PDF. Text is extracted locally.",
        label_visibility="collapsed",
    )
    if uploaded:
        if uploaded.name != st.session_state.doc_name:
            with st.spinner("Reading and indexing document…"):
                pages = extract_text(uploaded)
                if pages:
                    st.session_state.doc_pages  = pages
                    st.session_state.doc_chunks = chunk_pages(pages)
                    st.session_state.doc_name   = uploaded.name
                    st.session_state.doc_loaded = True
                    st.session_state.qa_history = []
                    st.success(f"Indexed {len(pages)} pages successfully!")
                    st.rerun()

    st.markdown("---")

    # Suggested questions — clicking one RUNS the search immediately
    st.markdown("**Common Questions**")
    st.markdown(
        '<div style="color:#78909C;font-size:0.8rem;margin-bottom:10px;">'
        'Click any question to search instantly</div>',
        unsafe_allow_html=True
    )
    for q in SUGGESTED:
        if st.button(q, key=f"sq_{q[:25]}", use_container_width=True):
            if not st.session_state.doc_chunks:
                st.warning("Please upload a PDF document first.")
            else:
                results = keyword_search(st.session_state.doc_chunks, q)
                st.session_state.qa_history.insert(0, {"query": q, "results": results})
                st.session_state.search_query = q
                st.rerun()

# ── RIGHT panel ───────────────────────────────────────────────────────────────
with right:

    # Search bar
    st.markdown("**Ask a Question**")
    query_input = st.text_input(
        "Ask a question",
        value=st.session_state.get("search_query", ""),
        placeholder="e.g. What is the timeline for initial IEP evaluation?",
        label_visibility="collapsed",
        key="main_query_input",
    )

    btn_col, clear_col = st.columns([3, 1])
    with btn_col:
        search_btn = st.button("Search Document", use_container_width=True, type="primary")
    with clear_col:
        if st.button("Clear", use_container_width=True):
            st.session_state.qa_history   = []
            st.session_state.search_query = ""
            st.rerun()

    if search_btn and query_input:
        if not st.session_state.doc_chunks:
            st.warning("Please upload a PDF first using the panel on the left.")
        else:
            results = keyword_search(st.session_state.doc_chunks, query_input)
            st.session_state.qa_history.insert(0, {"query": query_input, "results": results})
            st.session_state.search_query = query_input

    # ── Results ───────────────────────────────────────────────────────────────
    if st.session_state.qa_history:
        for entry in st.session_state.qa_history[:5]:
            st.markdown(f"""
            <div style="background:#E3F2FD;border-left:4px solid #1565C0;
                        border-radius:8px;padding:12px 16px;margin:16px 0 8px;">
                <span style="font-size:0.72rem;color:#5C6BC0;font-weight:600;
                             text-transform:uppercase;letter-spacing:0.05em;">
                    Your Question</span><br>
                <span style="font-weight:700;color:#1A1A2E;font-size:0.95rem;">
                    {entry['query']}</span>
            </div>
            """, unsafe_allow_html=True)

            if not entry["results"]:
                st.info("No matching passages found. Try different keywords or check your PDF has readable text.")
            else:
                st.markdown(f'<div style="color:#546E7A;font-size:0.82rem;margin-bottom:8px;">'
                            f'Found {len(entry["results"])} relevant sections</div>',
                            unsafe_allow_html=True)
                for i, r in enumerate(entry["results"], 1):
                    snippet  = r["text"][:500] + ("…" if len(r["text"]) > 500 else "")
                    hl       = highlight_text(snippet, entry["query"])
                    with st.expander(f"Result {i} — Page {r['page']}  (relevance score: {r['score']})", expanded=(i==1)):
                        st.markdown(f"""
                        <div style="font-size:0.88rem;line-height:1.8;color:#37474F;">
                            {hl}
                        </div>
                        <div style="margin-top:12px;">
                            <span style="background:#E3F2FD;color:#1565C0;
                                         border-radius:6px;padding:4px 12px;
                                         font-size:0.78rem;font-weight:600;">
                                📄 Page {r['page']} of {len(st.session_state.doc_pages)}
                            </span>
                        </div>
                        """, unsafe_allow_html=True)

    # ── Page browser with DROPDOWN ────────────────────────────────────────────
    if st.session_state.doc_pages:
        st.markdown("---")
        st.markdown("**Browse Document by Page**")

        total = len(st.session_state.doc_pages)
        # Build dropdown options with first few words as preview
        options = {}
        for pg in range(1, total + 1):
            preview = " ".join(st.session_state.doc_pages[pg].split()[:6])
            preview = preview[:40] + "…" if len(preview) > 40 else preview
            options[f"Page {pg}  —  {preview}"] = pg

        selected_label = st.selectbox(
            "Jump to page",
            list(options.keys()),
            label_visibility="collapsed",
        )
        selected_page = options[selected_label]

        page_text = st.session_state.doc_pages.get(selected_page, "(No text on this page)")
        word_count = len(page_text.split())

        st.markdown(f"""
        <div style="display:flex;justify-content:space-between;align-items:center;
                    margin-bottom:8px;">
            <span style="font-weight:700;color:#1565C0;">Page {selected_page} of {total}</span>
            <span style="font-size:0.78rem;color:#90A4AE;">{word_count} words</span>
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <div style="background:white;border:1px solid #E8EAF6;border-radius:10px;
                    padding:20px;max-height:420px;overflow-y:auto;
                    font-size:0.85rem;line-height:1.9;color:#37474F;
                    font-family:'JetBrains Mono',monospace;white-space:pre-wrap;">
{page_text if page_text.strip() else "(No readable text extracted from this page)"}
        </div>
        """, unsafe_allow_html=True)
