"""
PDF loader utility — auto-loads from docs/ folder or manual upload.
Caches results in st.session_state so re-upload is never needed within a session.
"""

import streamlit as st
from pathlib import Path
import re

DOCS_DIR = Path(__file__).parent.parent / "docs"


def extract_text(file_obj) -> dict:
    """Extract {page_num: text} from a PDF file object. Tries pdfplumber then PyMuPDF."""
    pages = {}
    try:
        import pdfplumber, io
        data = file_obj.read() if hasattr(file_obj, 'read') else open(file_obj, 'rb').read()
        with pdfplumber.open(io.BytesIO(data)) as pdf:
            for i, page in enumerate(pdf.pages, 1):
                pages[i] = page.extract_text() or ""
        return pages
    except Exception:
        pass
    try:
        import fitz, io
        data = file_obj.read() if hasattr(file_obj, 'read') else open(file_obj, 'rb').read()
        doc = fitz.open(stream=data, filetype="pdf")
        for i, page in enumerate(doc, 1):
            pages[i] = page.get_text()
        return pages
    except Exception as e:
        st.error(f"Could not read PDF. Install pdfplumber or PyMuPDF. Error: {e}")
        return {}


def chunk_pages(pages: dict, chunk_size: int = 400, overlap: int = 80) -> list:
    """Split pages into overlapping word chunks for search."""
    chunks = []
    for page_num, text in pages.items():
        words = text.split()
        step = chunk_size - overlap
        for start in range(0, max(1, len(words) - chunk_size + 1), step):
            chunk = " ".join(words[start: start + chunk_size])
            chunks.append({"page": page_num, "text": chunk, "start": start})
    return chunks


def keyword_search(chunks: list, query: str, top_k: int = 6) -> list:
    """Score chunks by keyword relevance and return top results."""
    if not query.strip():
        return []
    terms = re.findall(r'\w+', query.lower())
    # IEP domain-specific term boosts
    domain_weights = {
        "iep": 4, "evaluation": 3, "eligibility": 3, "placement": 3,
        "annual": 2, "review": 2, "amendment": 2, "consent": 3,
        "disability": 2, "classification": 2, "services": 2,
        "least restrictive": 4, "lre": 4, "transition": 2,
        "prior written notice": 4, "pwn": 4, "parent": 2,
        "goals": 2, "present levels": 3, "fape": 4, "idea": 3,
    }
    scored = []
    for chunk in chunks:
        text_lower = chunk["text"].lower()
        exact_bonus = 8 if query.lower() in text_lower else 0
        tf_score = sum(text_lower.count(t) for t in terms)
        domain_score = sum(w for kw, w in domain_weights.items() if kw in text_lower)
        score = tf_score + exact_bonus + domain_score
        if score > 0:
            scored.append({**chunk, "score": score})
    scored.sort(key=lambda x: x["score"], reverse=True)
    return scored[:top_k]


def highlight_text(text: str, query: str) -> str:
    """Wrap matching terms with highlight spans."""
    terms = sorted(re.findall(r'\w+', query), key=len, reverse=True)
    for term in terms:
        text = re.sub(
            rf'\b({re.escape(term)})\b',
            r'<mark style="background:#FFF59D;border-radius:3px;padding:0 2px;">\1</mark>',
            text, flags=re.IGNORECASE
        )
    return text


def auto_load_pdf():
    """
    Try to auto-load a PDF from the docs/ folder.
    Falls back gracefully if no PDF is present.
    Returns True if loaded successfully.
    """
    if st.session_state.get("doc_loaded"):
        return True

    pdf_files = list(DOCS_DIR.glob("*.pdf"))
    if not pdf_files:
        return False

    pdf_path = pdf_files[0]
    try:
        pages = extract_text(pdf_path)
        if pages:
            st.session_state.doc_pages  = pages
            st.session_state.doc_chunks = chunk_pages(pages)
            st.session_state.doc_name   = pdf_path.name
            st.session_state.doc_loaded = True
            return True
    except Exception:
        pass
    return False


def init_session():
    """Initialize all session state keys safely."""
    defaults = {
        "doc_pages":    {},
        "doc_chunks":   [],
        "doc_name":     "",
        "doc_loaded":   False,
        "search_query": "",
        "search_results": [],
        "qa_history":   [],
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v
