"""
Shared theme, CSS and UI helpers for IEP Education Platform.
Import this in every page: from utils.theme import apply_theme, card, badge
"""

import streamlit as st

# ── Master palette ────────────────────────────────────────────────────────────
PRIMARY   = "#1565C0"   # deep blue
SECONDARY = "#0097A7"   # teal
ACCENT    = "#FF6F00"   # amber
SUCCESS   = "#2E7D32"
WARNING   = "#F57F17"
DANGER    = "#C62828"
LIGHT_BG  = "#F0F4FF"
CARD_BG   = "#FFFFFF"


def apply_theme():
    """Inject global CSS. Call once at the top of every page."""
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;600&display=swap');

    :root {
        --primary:   #1565C0;
        --primary-light: #E3F2FD;
        --secondary: #0097A7;
        --accent:    #FF6F00;
        --success:   #2E7D32;
        --success-light: #E8F5E9;
        --warning:   #F57F17;
        --warning-light: #FFF8E1;
        --danger:    #C62828;
        --danger-light:  #FFEBEE;
        --text:      #1A1A2E;
        --text-muted:#5C6BC0;
        --bg:        #F0F4FF;
        --card:      #FFFFFF;
        --border:    #E8EAF6;
        --mono: 'JetBrains Mono', monospace;
        --sans: 'Plus Jakarta Sans', sans-serif;
        --radius: 12px;
        --shadow: 0 4px 20px rgba(21,101,192,0.08);
        --shadow-hover: 0 8px 32px rgba(21,101,192,0.16);
    }

    html, body, [class*="css"] {
        font-family: var(--sans) !important;
        color: var(--text);
    }

    /* ── App background ── */
    .stApp { background: var(--bg) !important; }
    .main .block-container {
        padding: 2rem 2.5rem !important;
        max-width: 1200px !important;
    }

    /* ── Sidebar ── */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0D1B4B 0%, #1565C0 100%) !important;
        border-right: none !important;
    }
    [data-testid="stSidebar"] * { color: #E3F2FD !important; }
    [data-testid="stSidebarNav"] a {
        font-family: var(--sans) !important;
        font-size: 0.9rem !important;
        font-weight: 500 !important;
        padding: 10px 16px !important;
        border-radius: 8px !important;
        margin: 2px 8px !important;
        transition: all 0.2s !important;
        border: none !important;
    }
    [data-testid="stSidebarNav"] a:hover {
        background: rgba(255,255,255,0.15) !important;
        transform: translateX(4px) !important;
    }
    [data-testid="stSidebarNav"] a[aria-current="page"] {
        background: rgba(255,111,0,0.3) !important;
        border-left: 3px solid #FF6F00 !important;
        font-weight: 700 !important;
    }

    /* ── Buttons ── */
    .stButton > button {
        background: linear-gradient(135deg, var(--primary), var(--secondary)) !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        font-family: var(--sans) !important;
        font-weight: 600 !important;
        font-size: 0.88rem !important;
        padding: 10px 24px !important;
        transition: all 0.2s !important;
        box-shadow: 0 2px 8px rgba(21,101,192,0.25) !important;
    }
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(21,101,192,0.35) !important;
    }

    /* ── Inputs ── */
    .stTextInput > div > div > input,
    .stSelectbox > div > div,
    .stTextArea textarea {
        border-radius: 8px !important;
        border: 2px solid var(--border) !important;
        font-family: var(--sans) !important;
        background: white !important;
        transition: border-color 0.2s !important;
    }
    .stTextInput > div > div > input:focus,
    .stTextArea textarea:focus {
        border-color: var(--primary) !important;
        box-shadow: 0 0 0 3px rgba(21,101,192,0.1) !important;
    }

    /* ── Tabs ── */
    .stTabs [data-baseweb="tab-list"] {
        background: white !important;
        border-radius: 10px !important;
        padding: 6px !important;
        gap: 4px !important;
        box-shadow: var(--shadow) !important;
        border: 1px solid var(--border) !important;
    }
    .stTabs [data-baseweb="tab"] {
        font-family: var(--sans) !important;
        font-size: 0.85rem !important;
        font-weight: 600 !important;
        border-radius: 8px !important;
        padding: 10px 20px !important;
        color: var(--text-muted) !important;
    }
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, var(--primary), var(--secondary)) !important;
        color: white !important;
        box-shadow: 0 2px 8px rgba(21,101,192,0.3) !important;
    }

    /* ── Expanders ── */
    .streamlit-expanderHeader {
        background: white !important;
        border-radius: 8px !important;
        border: 1px solid var(--border) !important;
        font-weight: 600 !important;
        font-family: var(--sans) !important;
    }
    .streamlit-expanderContent {
        border: 1px solid var(--border) !important;
        border-top: none !important;
        border-radius: 0 0 8px 8px !important;
        background: #FAFBFF !important;
    }

    /* ── Dataframe ── */
    .stDataFrame { border-radius: 10px !important; overflow: hidden !important; }
    .stDataFrame thead th {
        background: var(--primary) !important;
        color: white !important;
    }

    /* ── Alerts ── */
    .stAlert { border-radius: 10px !important; border: none !important; }

    /* ── Metric ── */
    [data-testid="metric-container"] {
        background: white !important;
        border-radius: 12px !important;
        padding: 16px !important;
        border: 1px solid var(--border) !important;
        box-shadow: var(--shadow) !important;
    }

    /* ── Progress bar ── */
    .stProgress > div > div > div > div {
        background: linear-gradient(90deg, var(--primary), var(--secondary)) !important;
        border-radius: 4px !important;
    }

    /* ── Hide streamlit branding ── */
    #MainMenu, footer, header { visibility: hidden !important; }
    </style>
    """, unsafe_allow_html=True)


def page_header(icon: str, title: str, subtitle: str, color: str = "#1565C0"):
    """Render a beautiful gradient page header."""
    st.markdown(f"""
    <div style="
        background: linear-gradient(135deg, {color} 0%, {color}dd 60%, #0097A7 100%);
        border-radius: 16px;
        padding: 32px 36px;
        margin-bottom: 28px;
        position: relative;
        overflow: hidden;
    ">
        <div style="position:absolute;top:-40px;right:-40px;width:200px;height:200px;
                    background:rgba(255,255,255,0.05);border-radius:50%;"></div>
        <div style="position:absolute;bottom:-60px;right:80px;width:150px;height:150px;
                    background:rgba(255,255,255,0.04);border-radius:50%;"></div>
        <div style="position:relative;z-index:1;">
            <div style="font-size:2.4rem;margin-bottom:8px;">{icon}</div>
            <div style="font-size:1.8rem;font-weight:800;color:white;
                        letter-spacing:-0.02em;line-height:1.2;">{title}</div>
            <div style="font-size:0.95rem;color:rgba(255,255,255,0.8);
                        margin-top:6px;font-weight:400;">{subtitle}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)


def card(content: str, accent_color: str = "#1565C0", padding: str = "20px 24px"):
    """Render a styled card."""
    st.markdown(f"""
    <div style="
        background: white;
        border-radius: 12px;
        border: 1px solid #E8EAF6;
        border-top: 4px solid {accent_color};
        padding: {padding};
        box-shadow: 0 4px 20px rgba(21,101,192,0.06);
        margin-bottom: 12px;
        transition: box-shadow 0.2s;
    ">{content}</div>
    """, unsafe_allow_html=True)


def badge(text: str, color: str = "blue") -> str:
    """Return HTML badge string."""
    colors = {
        "blue":   ("#E3F2FD", "#1565C0"),
        "green":  ("#E8F5E9", "#2E7D32"),
        "orange": ("#FFF8E1", "#F57F17"),
        "red":    ("#FFEBEE", "#C62828"),
        "teal":   ("#E0F7FA", "#00838F"),
        "purple": ("#EDE7F6", "#6A1B9A"),
    }
    bg, fg = colors.get(color, colors["blue"])
    return (f'<span style="background:{bg};color:{fg};border-radius:20px;'
            f'padding:3px 10px;font-size:0.75rem;font-weight:600;'
            f'font-family:\'JetBrains Mono\',monospace;letter-spacing:0.03em;">'
            f'{text}</span>')


def sidebar_branding():
    """Render sidebar logo and branding."""
    with st.sidebar:
        st.markdown("""
        <div style="padding:20px 12px 28px;">
            <div style="display:flex;align-items:center;gap:10px;margin-bottom:16px;">
                <div style="width:42px;height:42px;background:rgba(255,255,255,0.15);
                            border-radius:10px;display:flex;align-items:center;
                            justify-content:center;font-size:1.4rem;">📋</div>
                <div>
                    <div style="font-weight:800;font-size:1rem;color:white;line-height:1.1;">
                        IEP Education</div>
                    <div style="font-size:0.7rem;color:rgba(255,255,255,0.6);
                                font-weight:400;letter-spacing:0.05em;">
                        PLATFORM</div>
                </div>
            </div>
            <div style="height:1px;background:rgba(255,255,255,0.15);margin-bottom:16px;"></div>
            <div style="font-size:0.72rem;color:rgba(255,255,255,0.5);
                        font-weight:600;letter-spacing:0.1em;text-transform:uppercase;
                        margin-bottom:8px;">Navigation</div>
        </div>
        """, unsafe_allow_html=True)
