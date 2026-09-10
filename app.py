"""
AI Job Mentor for Informal Workers
Powered by IBM Granite via watsonx.ai

Run: streamlit run app.py
"""

import os
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

# ── Page config (must be first Streamlit call) ───────────────────────────────
st.set_page_config(
    page_title="AI Job Mentor",
    page_icon="🌟",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Internal imports ─────────────────────────────────────────────────────────
from i18n.translations import t
from data.demo_data import (
    DEMO_WORKERS,
    JOB_SKILL_REQUIREMENTS,
    get_demo_worker,
)
from agents.job_agent import get_job_recommendations, get_recommendation_narrative
from agents.skill_agent import get_skill_gaps, get_skill_gap_narrative
from agents.training_agent import get_training_recommendations, get_training_narrative
from agents.scheme_agent import get_scheme_recommendations, get_scheme_narrative
from agents.mentor_agent import get_mentor_response, get_greeting

# ── Custom CSS — Professional Dark Aesthetic ─────────────────────────────────
st.markdown(
    """
    <style>
    /* ── Google Font import ── */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

    /* ── Root variables ── */
    :root {
        --bg-base:        #0a0f1e;
        --bg-surface:     #111827;
        --bg-elevated:    #1a2235;
        --bg-glass:       rgba(255,255,255,0.04);
        --border:         rgba(255,255,255,0.08);
        --border-accent:  rgba(0,212,255,0.35);
        --cyan:           #00d4ff;
        --cyan-dim:       #0099bb;
        --gold:           #f5a623;
        --green:          #10d9a0;
        --red:            #ff6b6b;
        --orange:         #ffa94d;
        --purple:         #9b59f7;
        --text-primary:   #e2e8f0;
        --text-secondary: #94a3b8;
        --text-muted:     #64748b;
    }

    /* ── Global overrides ── */
    html, body, [class*="css"] {
        font-family: 'Inter', -apple-system, sans-serif !important;
    }
    .stApp {
        background: var(--bg-base) !important;
        background-image:
            radial-gradient(ellipse 80% 50% at 20% -10%, rgba(0,212,255,0.06) 0%, transparent 60%),
            radial-gradient(ellipse 60% 40% at 80% 100%, rgba(155,89,247,0.05) 0%, transparent 55%);
    }
    section[data-testid="stSidebar"] {
        background: var(--bg-surface) !important;
        border-right: 1px solid var(--border) !important;
    }
    section[data-testid="stSidebar"] * { color: var(--text-primary) !important; }

    /* ── Headings ── */
    h1, h2, h3, h4, h5, h6 { color: var(--text-primary) !important; font-weight: 700 !important; }
    p, li, span, label { color: var(--text-secondary) !important; }

    /* ── Inputs / Selects / Textareas ── */
    .stTextInput > div > div > input,
    .stSelectbox > div > div > div,
    .stNumberInput > div > div > input,
    .stTextArea > div > div > textarea {
        background: var(--bg-elevated) !important;
        border: 1px solid var(--border) !important;
        border-radius: 8px !important;
        color: var(--text-primary) !important;
        transition: border-color 0.2s;
    }
    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus {
        border-color: var(--cyan) !important;
        box-shadow: 0 0 0 3px rgba(0,212,255,0.12) !important;
    }

    /* ── Buttons ── */
    .stButton > button {
        background: var(--bg-elevated) !important;
        border: 1px solid var(--border) !important;
        color: var(--text-secondary) !important;
        border-radius: 8px !important;
        font-weight: 500 !important;
        transition: all 0.2s !important;
        font-family: 'Inter', sans-serif !important;
    }
    .stButton > button:hover {
        border-color: var(--cyan) !important;
        color: var(--cyan) !important;
        box-shadow: 0 0 14px rgba(0,212,255,0.15) !important;
        transform: translateY(-1px);
    }
    .stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #0099bb 0%, #00d4ff 100%) !important;
        border: none !important;
        color: #0a0f1e !important;
        font-weight: 700 !important;
        box-shadow: 0 4px 20px rgba(0,212,255,0.3) !important;
    }
    .stButton > button[kind="primary"]:hover {
        box-shadow: 0 6px 28px rgba(0,212,255,0.5) !important;
        transform: translateY(-2px);
        color: #0a0f1e !important;
    }

    /* ── Expanders ── */
    .streamlit-expanderHeader {
        background: var(--bg-elevated) !important;
        border: 1px solid var(--border) !important;
        border-radius: 10px !important;
        color: var(--text-primary) !important;
        font-weight: 600 !important;
        transition: border-color 0.2s;
    }
    .streamlit-expanderHeader:hover { border-color: var(--border-accent) !important; }
    .streamlit-expanderContent {
        background: var(--bg-elevated) !important;
        border: 1px solid var(--border) !important;
        border-top: none !important;
        border-radius: 0 0 10px 10px !important;
    }

    /* ── Progress bars ── */
    .stProgress > div > div { background: var(--bg-elevated) !important; border-radius: 99px !important; }
    .stProgress > div > div > div {
        background: linear-gradient(90deg, var(--cyan-dim), var(--cyan)) !important;
        border-radius: 99px !important;
        box-shadow: 0 0 8px rgba(0,212,255,0.4);
    }
    /* Progress bar label text — make it clearly readable */
    .stProgress p { color: #cbd5e1 !important; font-size: 0.82rem !important; font-weight: 600 !important; }

    /* ── st.info / st.warning boxes — ensure body text is readable ── */
    [data-testid="stAlert"] p,
    [data-testid="stAlert"] li,
    [data-testid="stAlert"] span,
    [data-testid="stAlert"] { color: #e2e8f0 !important; }

    /* ── Form ── */
    [data-testid="stForm"] {
        background: var(--bg-elevated) !important;
        border: 1px solid var(--border) !important;
        border-radius: 14px !important;
        padding: 1.5rem !important;
    }

    /* ── Checkboxes ── */
    .stCheckbox > label > div:first-child {
        background: var(--bg-elevated) !important;
        border: 1px solid var(--border) !important;
    }

    /* ── Metrics ── */
    [data-testid="stMetricValue"] { color: var(--cyan) !important; font-weight: 700 !important; }
    [data-testid="stMetricLabel"] { color: var(--text-secondary) !important; }

    /* ── Dividers ── */
    hr { border-color: var(--border) !important; }

    /* ── Scrollbar ── */
    ::-webkit-scrollbar { width: 6px; height: 6px; }
    ::-webkit-scrollbar-track { background: var(--bg-surface); }
    ::-webkit-scrollbar-thumb { background: #2d3748; border-radius: 3px; }
    ::-webkit-scrollbar-thumb:hover { background: var(--cyan-dim); }

    /* ═══════════════════════════════════════════════════════════════
       COMPONENT CLASSES
    ═══════════════════════════════════════════════════════════════ */

    /* ── Main header banner ── */
    .main-header {
        background: linear-gradient(135deg, #0d1b2e 0%, #0f2744 50%, #0d1b2e 100%);
        border: 1px solid var(--border-accent);
        border-radius: 16px;
        padding: 2rem 2.5rem;
        margin-bottom: 2rem;
        text-align: center;
        position: relative;
        overflow: hidden;
        box-shadow: 0 0 60px rgba(0,212,255,0.08), inset 0 1px 0 rgba(255,255,255,0.05);
    }
    .main-header::before {
        content: '';
        position: absolute;
        top: -50%;
        left: 50%;
        transform: translateX(-50%);
        width: 300px;
        height: 300px;
        background: radial-gradient(circle, rgba(0,212,255,0.08) 0%, transparent 70%);
        pointer-events: none;
    }
    .main-header h1 {
        margin: 0;
        font-size: 2.2rem;
        font-weight: 800;
        color: #ffffff !important;
        letter-spacing: -0.5px;
        text-shadow: 0 0 30px rgba(0,212,255,0.4);
    }
    .main-header p {
        margin: 0.5rem 0 0;
        color: var(--cyan) !important;
        font-size: 0.9rem;
        font-weight: 500;
        letter-spacing: 0.5px;
        opacity: 0.9;
    }

    /* ── Metric cards ── */
    .metric-card {
        background: var(--bg-glass);
        border: 1px solid var(--border);
        border-radius: 12px;
        padding: 1.2rem 1rem;
        text-align: center;
        backdrop-filter: blur(10px);
        transition: border-color 0.2s, box-shadow 0.2s;
    }
    .metric-card:hover {
        border-color: var(--border-accent);
        box-shadow: 0 0 20px rgba(0,212,255,0.1);
    }
    .metric-card .value {
        font-size: 2rem;
        font-weight: 800;
        background: linear-gradient(135deg, var(--cyan), var(--purple));
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    .metric-card .label {
        font-size: 0.78rem;
        color: var(--text-muted) !important;
        margin-top: 0.3rem;
        text-transform: uppercase;
        letter-spacing: 0.6px;
        font-weight: 500;
    }

    /* ── Badges ── */
    .badge {
        display: inline-block;
        padding: 0.22rem 0.7rem;
        border-radius: 20px;
        font-size: 0.73rem;
        font-weight: 600;
        margin: 0.18rem;
        letter-spacing: 0.3px;
    }
    .badge-green  { background: rgba(16,217,160,0.15);  color: #10d9a0; border: 1px solid rgba(16,217,160,0.3); }
    .badge-blue   { background: rgba(0,212,255,0.12);   color: #00d4ff; border: 1px solid rgba(0,212,255,0.3); }
    .badge-orange { background: rgba(245,166,35,0.13);  color: #f5a623; border: 1px solid rgba(245,166,35,0.3); }
    .badge-red    { background: rgba(255,107,107,0.13); color: #ff6b6b; border: 1px solid rgba(255,107,107,0.3); }
    .badge-gray   { background: rgba(255,255,255,0.06); color: #94a3b8; border: 1px solid rgba(255,255,255,0.1); }

    /* ── Scheme cards ── */
    .scheme-card {
        border-left: 3px solid var(--cyan);
        background: linear-gradient(135deg, rgba(0,212,255,0.04) 0%, var(--bg-glass) 100%);
        border-radius: 0 12px 12px 0;
        padding: 1.1rem 1.3rem;
        margin-bottom: 0.8rem;
        backdrop-filter: blur(8px);
    }
    .scheme-ineligible {
        border-left-color: #2d3748;
        background: rgba(255,255,255,0.02);
        opacity: 0.55;
    }

    /* ── Chat bubbles ── */
    .chat-bubble-user {
        background: linear-gradient(135deg, #0099bb 0%, #006680 100%);
        color: #ffffff !important;
        border-radius: 18px 18px 4px 18px;
        padding: 0.8rem 1.1rem;
        margin: 0.6rem 0 0.6rem 18%;
        font-size: 0.92rem;
        box-shadow: 0 4px 15px rgba(0,212,255,0.2);
        border: 1px solid rgba(0,212,255,0.2);
        line-height: 1.55;
    }
    .chat-bubble-aasha {
        background: var(--bg-elevated);
        color: var(--text-primary) !important;
        border-radius: 18px 18px 18px 4px;
        padding: 0.8rem 1.1rem;
        margin: 0.6rem 18% 0.6rem 0;
        font-size: 0.92rem;
        border: 1px solid var(--border-accent);
        box-shadow: 0 4px 15px rgba(0,0,0,0.3);
        line-height: 1.55;
    }
    .chat-bubble-aasha b { color: var(--cyan) !important; }

    /* ── Status banners ── */
    .ai-banner {
        background: linear-gradient(135deg, rgba(16,217,160,0.1), rgba(16,217,160,0.05));
        border: 1px solid rgba(16,217,160,0.3);
        border-radius: 10px;
        padding: 0.6rem 1rem;
        color: #10d9a0 !important;
        font-size: 0.84rem;
        font-weight: 500;
        margin-bottom: 1rem;
    }
    .offline-banner {
        background: linear-gradient(135deg, rgba(245,166,35,0.1), rgba(245,166,35,0.05));
        border: 1px solid rgba(245,166,35,0.3);
        border-radius: 10px;
        padding: 0.6rem 1rem;
        color: #f5a623 !important;
        font-size: 0.84rem;
        font-weight: 500;
        margin-bottom: 1rem;
    }

    /* ── Profile summary box ── */
    .profile-summary {
        background: var(--bg-elevated);
        border: 1px solid var(--border);
        border-radius: 14px;
        padding: 1.4rem 1.6rem;
    }
    .profile-summary .prow {
        display: flex;
        justify-content: space-between;
        padding: 0.35rem 0;
        border-bottom: 1px solid rgba(255,255,255,0.04);
        font-size: 0.88rem;
    }
    .profile-summary .prow:last-child { border-bottom: none; }
    .profile-summary .pkey { color: var(--text-muted) !important; font-weight: 500; }
    .profile-summary .pval { color: var(--text-primary) !important; font-weight: 600; text-align: right; }

    /* ── Section title pill ── */
    .section-pill {
        display: inline-block;
        background: rgba(0,212,255,0.08);
        border: 1px solid var(--border-accent);
        color: var(--cyan) !important;
        font-size: 0.75rem;
        font-weight: 700;
        letter-spacing: 1px;
        text-transform: uppercase;
        padding: 0.25rem 0.8rem;
        border-radius: 20px;
        margin-bottom: 0.6rem;
    }

    /* ── Sidebar active nav ── */
    .sidebar-nav-active {
        background: rgba(0,212,255,0.1) !important;
        border-left: 3px solid var(--cyan) !important;
        color: var(--cyan) !important;
    }

    /* ── Glow divider ── */
    .glow-divider {
        height: 1px;
        background: linear-gradient(90deg, transparent, var(--border-accent), transparent);
        border: none;
        margin: 1.5rem 0;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# ── Session state initialisation ─────────────────────────────────────────────
def _init_state():
    defaults = {
        "lang": "en",
        "worker": get_demo_worker("W001"),
        "chat_history": [],
        "chat_greeted": False,
        "active_section": "profile",
        "ai_status": None,   # True / False / None (not yet tested)
    }
    for key, val in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = val


_init_state()

lang = st.session_state["lang"]


def T(key: str) -> str:
    return t(key, lang)


# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown(
        """
        <div style="padding:0.8rem 0 0.4rem; text-align:center;">
            <div style="font-size:1.6rem; font-weight:800; color:#00d4ff; letter-spacing:-0.5px; line-height:1.2;">
                🌟 AI Job Mentor
            </div>
            <div style="font-size:0.72rem; color:#64748b; letter-spacing:1px; text-transform:uppercase; margin-top:0.2rem;">
                Your Personal Career Guide
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown('<hr style="border-color:rgba(255,255,255,0.07); margin:0.8rem 0;">', unsafe_allow_html=True)

    # Language selector
    lang_choice = st.selectbox(
        T("select_language"),
        options=["English", "हिंदी", "தமிழ்"],
        index=["English", "हिंदी", "தமிழ்"].index(
            {"en": "English", "hi": "हिंदी", "ta": "தமிழ்"}[st.session_state["lang"]]
        ),
    )
    new_lang = {"English": "en", "हिंदी": "hi", "தமிழ்": "ta"}[lang_choice]
    if new_lang != st.session_state["lang"]:
        st.session_state["lang"] = new_lang
        st.session_state["chat_greeted"] = False
        st.rerun()
    lang = st.session_state["lang"]

    st.markdown('<p style="font-size:0.7rem; color:#64748b; text-transform:uppercase; letter-spacing:0.8px; margin:0 0 0.4rem;">Navigation</p>', unsafe_allow_html=True)

    # Navigation — one real button per section; active item highlighted via inline CSS
    sections = [
        ("profile",  T("nav_profile")),
        ("jobs",     T("nav_jobs")),
        ("skills",   T("nav_skills")),
        ("training", T("nav_training")),
        ("schemes",  T("nav_schemes")),
        ("chat",     T("nav_chat")),
    ]
    active_section = st.session_state.get("active_section", "profile")
    for sec_key, label in sections:
        is_active = sec_key == active_section
        if is_active:
            # Inject a scoped rule that overrides the very next stButton in this sidebar
            st.markdown(
                "<style>.nav-active-next + div[data-testid='stButton'] > button,"
                ".nav-active-next ~ div[data-testid='stButton']:first-of-type > button"
                "{ background:rgba(0,212,255,0.13)!important;"
                "  border:1px solid rgba(0,212,255,0.42)!important;"
                "  color:#00d4ff!important; font-weight:600!important; }</style>"
                "<span class='nav-active-next'></span>",
                unsafe_allow_html=True,
            )
        if st.button(label, key=f"nav_{sec_key}", use_container_width=True):
            st.session_state["active_section"] = sec_key
            st.rerun()

    st.markdown('<hr style="border-color:rgba(255,255,255,0.07); margin:0.8rem 0;">', unsafe_allow_html=True)
    st.markdown('<p style="font-size:0.7rem; color:#64748b; text-transform:uppercase; letter-spacing:0.8px; margin:0 0 0.4rem;">Demo Profiles</p>', unsafe_allow_html=True)

    # Demo worker quick-select
    worker_names = [f"{w['id']} – {w['name']}" for w in DEMO_WORKERS]
    sel = st.selectbox(T("select_worker"), worker_names, label_visibility="collapsed")
    selected_id = sel.split(" – ")[0]
    if st.button(T("profile_load_demo"), use_container_width=True):
        st.session_state["worker"] = get_demo_worker(selected_id)
        st.session_state["chat_greeted"] = False
        st.session_state["chat_history"] = []
        st.session_state["active_section"] = "profile"
        st.rerun()

    st.markdown('<hr style="border-color:rgba(255,255,255,0.07); margin:0.8rem 0;">', unsafe_allow_html=True)
    st.markdown(
        f"<div style='font-size:0.7rem; color:#374151; text-align:center; line-height:1.5;'>"
        f"<span style='color:#00d4ff;'>●</span> AI-powered career guidance</div>",
        unsafe_allow_html=True,
    )


# ── Header ────────────────────────────────────────────────────────────────────
st.markdown(
    f"""
    <div class="main-header">
        <h1>🌟 {T("app_title")}</h1>
        <p>{T("app_subtitle")}</p>
    </div>
    """,
    unsafe_allow_html=True,
)

worker: dict = st.session_state["worker"]
section = st.session_state.get("active_section", "profile")


# ── Helper: score colour ──────────────────────────────────────────────────────
def score_colour(score: int) -> str:
    if score >= 75:
        return "badge-green"
    if score >= 50:
        return "badge-blue"
    if score >= 30:
        return "badge-orange"
    return "badge-red"


def progress_colour(score: int) -> str:
    if score >= 75:
        return "green"
    if score >= 50:
        return "blue"
    return "orange"


# ─────────────────────────────────────────────────────────────────────────────
# SECTION: Worker Profile
# ─────────────────────────────────────────────────────────────────────────────
if section == "profile":
    st.markdown('<div class="section-pill">👤 Profile</div>', unsafe_allow_html=True)
    st.header(T("profile_header"))

    col1, col2 = st.columns([2, 1])

    with col1:
        with st.form("profile_form"):
            fc1, fc2 = st.columns(2)
            with fc1:
                name = st.text_input(T("profile_name"), value=worker.get("name", ""))
                age  = st.number_input(T("profile_age"), min_value=16, max_value=80, value=worker.get("age", 25))
                gender = st.selectbox(T("profile_gender"), ["Male", "Female", "Other"],
                                      index=["Male", "Female", "Other"].index(worker.get("gender", "Male")))
                location = st.text_input(T("profile_location"), value=worker.get("location", ""))
            with fc2:
                edu_options = [
                    "Class 5", "Class 8", "Class 10 (SSC)", "Class 12 (HSC)",
                    "ITI Certificate", "Diploma", "Graduate", "Post Graduate",
                ]
                edu_idx = next(
                    (i for i, e in enumerate(edu_options) if e.lower() in worker.get("education","").lower()),
                    2,
                )
                education = st.selectbox(T("profile_education"), edu_options, index=edu_idx)
                occupation = st.text_input(T("profile_occupation"), value=worker.get("current_occupation", ""))
                income = st.number_input(T("profile_income"), min_value=0, max_value=200000,
                                         value=worker.get("monthly_income", 8000), step=500)
                exp = st.number_input(T("profile_experience"), min_value=0, max_value=50,
                                      value=worker.get("experience_years", 0))

            skills_raw = st.text_input(
                T("profile_skills"),
                value=", ".join(worker.get("skills", [])),
            )
            langs_raw = st.text_input(
                T("profile_languages"),
                value=", ".join(worker.get("languages", [])),
            )

            bc1, bc2, bc3, bc4 = st.columns(4)
            with bc1:
                ration = st.selectbox(T("profile_ration"), ["BPL", "AAY", "PHH", "APL"],
                                      index=["BPL", "AAY", "PHH", "APL"].index(worker.get("ration_card", "PHH")))
            with bc2:
                family = st.number_input(T("profile_family"), min_value=1, max_value=15,
                                         value=worker.get("family_size", 3))
            with bc3:
                smartphone = st.checkbox(T("profile_smartphone"), value=worker.get("has_smartphone", True))
            with bc4:
                bank = st.checkbox(T("profile_bank"), value=worker.get("has_bank_account", True))

            if st.form_submit_button(T("profile_save"), use_container_width=True, type="primary"):
                st.session_state["worker"] = {
                    "id": worker.get("id", "CUSTOM"),
                    "name": name,
                    "age": int(age),
                    "gender": gender,
                    "location": location,
                    "education": education,
                    "current_occupation": occupation,
                    "monthly_income": int(income),
                    "experience_years": int(exp),
                    "skills": [s.strip() for s in skills_raw.split(",") if s.strip()],
                    "languages": [l.strip() for l in langs_raw.split(",") if l.strip()],
                    "has_smartphone": smartphone,
                    "has_bank_account": bank,
                    "family_size": int(family),
                    "ration_card": ration,
                }
                st.session_state["chat_greeted"] = False
                st.success(T("profile_saved"))
                st.rerun()

    with col2:
        st.markdown('<div class="section-pill">📋 Summary</div>', unsafe_allow_html=True)
        w = st.session_state["worker"]
        smartphone_icon = "✅" if w.get("has_smartphone") else "❌"
        bank_icon = "✅" if w.get("has_bank_account") else "❌"
        rows = [
            ("Name", w.get("name", "—")),
            ("Age", str(w.get("age", "—"))),
            ("Location", w.get("location", "—")),
            ("Occupation", w.get("current_occupation", "—")),
            ("Income", f"₹{w.get('monthly_income', 0):,}{T('per_month')}"),
            ("Education", w.get("education", "—")),
            ("Experience", f"{w.get('experience_years', 0)} {T('years_exp')}"),
            ("Smartphone", smartphone_icon),
            ("Bank Account", bank_icon),
            ("Ration Card", w.get("ration_card", "—")),
            ("Family Size", f"{w.get('family_size', '—')} members"),
        ]
        rows_html = "".join(
            f'<div class="prow"><span class="pkey">{k}</span><span class="pval">{v}</span></div>'
            for k, v in rows
        )
        st.markdown(
            f'<div class="profile-summary">{rows_html}</div>',
            unsafe_allow_html=True,
        )
        skills = w.get("skills", [])
        if skills:
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown('<p style="color:#64748b; font-size:0.78rem; text-transform:uppercase; letter-spacing:0.7px; margin-bottom:0.4rem;">Skills</p>', unsafe_allow_html=True)
            st.markdown(
                "".join(f"<span class='badge badge-blue'>{s}</span>" for s in skills),
                unsafe_allow_html=True,
            )


# ─────────────────────────────────────────────────────────────────────────────
# SECTION: Job Recommendations
# ─────────────────────────────────────────────────────────────────────────────
elif section == "jobs":
    st.markdown('<div class="section-pill">💼 Jobs</div>', unsafe_allow_html=True)
    st.header(T("jobs_header"))
    st.caption(T("jobs_subheader"))

    with st.spinner("Matching jobs to your profile..."):
        top_jobs = get_job_recommendations(worker, top_n=5)

    # Summary metrics
    scores = [j["match"]["overall"] for j in top_jobs]
    avg_score = sum(scores) / len(scores) if scores else 0

    m1, m2, m3, m4 = st.columns(4)
    m1.markdown(
        f'<div class="metric-card"><div class="value">{len(top_jobs)}</div><div class="label">Jobs Found</div></div>',
        unsafe_allow_html=True,
    )
    m2.markdown(
        f'<div class="metric-card"><div class="value">{scores[0] if scores else 0}%</div><div class="label">Best Match</div></div>',
        unsafe_allow_html=True,
    )
    m3.markdown(
        f'<div class="metric-card"><div class="value">{int(avg_score)}%</div><div class="label">Avg Match</div></div>',
        unsafe_allow_html=True,
    )
    m4.markdown(
        f'<div class="metric-card"><div class="value">₹{max(j["salary_max"] for j in top_jobs):,}</div><div class="label">Max Salary</div></div>',
        unsafe_allow_html=True,
    )
    st.markdown("<br>", unsafe_allow_html=True)

    for job in top_jobs:
        score = job["match"]["overall"]
        badge_cls = score_colour(score)

        with st.expander(
            f"**{job['title']}** — {job['employer']} | "
            f"₹{job['salary_min']:,}–{job['salary_max']:,}/mo",
            expanded=(score >= 70),
        ):
            c1, c2 = st.columns([3, 1])
            with c1:
                st.markdown(
                    f"<span class='badge {badge_cls}'>{T('match_score')}: {score}%</span>"
                    f"<span class='badge badge-gray'>{job['job_type']}</span>"
                    f"<span class='badge badge-blue'>{job['sector']}</span>",
                    unsafe_allow_html=True,
                )
                st.markdown(f"📍 **{job['location']}** · {job['category']}")
                st.markdown(job["description"])
                st.markdown(
                    f"**{T('required_skills')}:** "
                    + "  ".join(
                        f"`{s}`" for s in job["required_skills"]
                    )
                )

            with c2:
                st.markdown(f"**Match Breakdown**")
                m = job["match"]
                st.progress(m["skill_match"] / 100, text=f"{T('skill_match')}: {m['skill_match']}%")
                st.progress(m["education_fit"] / 100, text=f"{T('edu_fit')}: {m['education_fit']}%")
                st.progress(m["experience_fit"] / 100, text=f"{T('exp_fit')}: {m['experience_fit']}%")
                st.progress(m["salary_potential"] / 100, text=f"{T('salary_potential')}: {m['salary_potential']}%")

    # AI narrative
    st.markdown('<div class="glow-divider"></div>', unsafe_allow_html=True)
    st.subheader(T("ai_recommendation"))
    if st.button("🤖 Generate AI Recommendation", key="gen_job_ai"):
        with st.spinner("Generating your personalised recommendation..."):
            narrative, is_live = get_recommendation_narrative(worker, top_jobs, lang)
        if not is_live and narrative == "Sorry, I'm temporarily unable to respond. Please try again in a moment.":
            st.warning(narrative)
        else:
            st.info(narrative)


# ─────────────────────────────────────────────────────────────────────────────
# SECTION: Skill Gap Analysis
# ─────────────────────────────────────────────────────────────────────────────
elif section == "skills":
    st.markdown('<div class="section-pill">📊 Skill Analysis</div>', unsafe_allow_html=True)
    st.header(T("skills_header"))

    target_job = st.selectbox(
        T("target_job"),
        list(JOB_SKILL_REQUIREMENTS.keys()),
    )

    gap = get_skill_gaps(worker.get("skills", []), target_job)
    readiness = gap["readiness_percentage"]
    readiness_col = progress_colour(readiness)

    col1, col2 = st.columns([2, 1])

    with col1:
        st.subheader(f"📊 {target_job}")
        colour_map = {"green": "#10d9a0", "blue": "#00d4ff", "orange": "#f5a623"}
        glow_map   = {"green": "rgba(16,217,160,0.3)", "blue": "rgba(0,212,255,0.3)", "orange": "rgba(245,166,35,0.3)"}
        rc = readiness_col
        st.markdown(
            f"""
            <div style="background:rgba(255,255,255,0.03); border:1px solid rgba(255,255,255,0.07);
                        border-radius:12px; padding:1.2rem 1.5rem; margin-bottom:1rem; display:flex;
                        align-items:center; gap:1.5rem;">
                <div>
                    <div style="font-size:0.75rem; color:#64748b; text-transform:uppercase; letter-spacing:0.7px;">{T('readiness')}</div>
                    <div style="font-size:3rem; font-weight:800; color:{colour_map.get(rc,'#00d4ff')};
                                text-shadow:0 0 20px {glow_map.get(rc,'rgba(0,212,255,0.3)')};
                                line-height:1.1;">{readiness}%</div>
                </div>
                <div style="flex:1; height:10px; background:rgba(255,255,255,0.06); border-radius:99px; overflow:hidden;">
                    <div style="width:{readiness}%; height:100%;
                                background:linear-gradient(90deg,{colour_map.get(rc,'#00d4ff')}88,{colour_map.get(rc,'#00d4ff')});
                                border-radius:99px; box-shadow:0 0 10px {glow_map.get(rc,'rgba(0,212,255,0.4)')};"></div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        sc1, sc2 = st.columns(2)
        with sc1:
            st.markdown(f"**{T('skills_you_have')}**")
            if gap["present_skills"]:
                for s in gap["present_skills"]:
                    st.markdown(f"<span class='badge badge-green'>{s}</span>", unsafe_allow_html=True)
            else:
                st.caption("None matching yet")
        with sc2:
            st.markdown(f"**{T('skills_to_develop')}**")
            if gap["missing_skills"]:
                for s in gap["missing_skills"]:
                    st.markdown(f"<span class='badge badge-red'>{s}</span>", unsafe_allow_html=True)
            else:
                st.success(T("no_skills_gap"))

    with col2:
        st.subheader(T("skill_categories"))
        from data.demo_data import SKILL_TAXONOMY
        worker_norm = {s.lower() for s in worker.get("skills", [])}
        for cat, skills in SKILL_TAXONOMY.items():
            owned = [s for s in skills if any(s.lower() in wn or wn in s.lower() for wn in worker_norm)]
            pct = int(len(owned) / max(len(skills), 1) * 100)
            st.progress(pct / 100, text=f"{cat}: {pct}%")

    # AI narrative
    st.markdown('<div class="glow-divider"></div>', unsafe_allow_html=True)
    st.subheader(T("ai_analysis"))
    if st.button("🤖 Generate AI Analysis", key="gen_skill_ai"):
        with st.spinner("Analysing your skill profile..."):
            narrative, is_live = get_skill_gap_narrative(worker, gap, lang)
        if not is_live and narrative == "Sorry, I'm temporarily unable to respond. Please try again in a moment.":
            st.warning(narrative)
        else:
            st.info(narrative)


# ─────────────────────────────────────────────────────────────────────────────
# SECTION: Training Recommendations
# ─────────────────────────────────────────────────────────────────────────────
elif section == "training":
    st.markdown('<div class="section-pill">🎓 Training</div>', unsafe_allow_html=True)
    st.header(T("training_header"))
    st.caption(T("training_subheader"))

    # Collect missing skills from all job gaps
    from agents.skill_agent import get_all_skill_gaps
    all_gaps = get_all_skill_gaps(worker)
    missing_all: list[str] = []
    for g in all_gaps:
        missing_all.extend(g["missing_skills"])
    missing_all = list(dict.fromkeys(missing_all))  # deduplicate

    programmes = get_training_recommendations(worker, missing_all, top_n=6)

    # Summary
    free_count = sum(1 for p in programmes if p["cost"].lower() == "free")
    st.markdown(
        f'<div style="background:rgba(0,212,255,0.06); border:1px solid rgba(0,212,255,0.2); '
        f'border-radius:10px; padding:0.7rem 1.2rem; color:#cbd5e1; font-size:0.88rem; margin-bottom:1rem;">'
        f'Found <b style="color:#00d4ff">{len(programmes)}</b> programmes · '
        f'<b style="color:#10d9a0">{free_count} free</b> · '
        f'addressing <b style="color:#f5a623">{len(missing_all)}</b> skill gaps</div>',
        unsafe_allow_html=True,
    )
    st.markdown('<div class="glow-divider"></div>', unsafe_allow_html=True)

    for prog in programmes:
        rel = prog["relevance_score"]
        badge_cls = score_colour(rel)

        with st.expander(
            f"**{prog['name']}** — {prog['provider']} | {prog['cost']}",
            expanded=(rel >= 60),
        ):
            c1, c2 = st.columns([3, 1])
            with c1:
                st.markdown(
                    f"<span class='badge {badge_cls}'>{T('relevance')}: {rel}%</span>"
                    f"<span class='badge badge-gray'>{prog['mode']}</span>"
                    f"<span class='badge badge-blue'>{prog['cost']}</span>",
                    unsafe_allow_html=True,
                )
                st.markdown(f"**{T('duration')}:** {prog['duration']}")
                st.markdown(f"**{T('certification')}:** {prog['certification']}")
                st.markdown(f"**{T('eligibility')}:** {prog['eligibility']}")
                st.markdown(
                    f"**Skills:** "
                    + "  ".join(f"`{s}`" for s in prog["skills_covered"])
                )
                st.markdown(f"[{T('enroll_now')} →]({prog['link']})")
            with c2:
                st.progress(rel / 100, text=f"Relevance: {rel}%")
                st.metric(T("cost"), prog["cost"])
                st.metric(T("duration"), prog["duration"])

    # AI narrative
    st.markdown('<div class="glow-divider"></div>', unsafe_allow_html=True)
    st.subheader(T("ai_recommendation"))
    if st.button("🤖 Generate Training Guidance", key="gen_train_ai"):
        with st.spinner("Building your personalised training path..."):
            narrative, is_live = get_training_narrative(worker, programmes, missing_all, lang)
        if not is_live and narrative == "Sorry, I'm temporarily unable to respond. Please try again in a moment.":
            st.warning(narrative)
        else:
            st.info(narrative)


# ─────────────────────────────────────────────────────────────────────────────
# SECTION: Government Schemes
# ─────────────────────────────────────────────────────────────────────────────
elif section == "schemes":
    st.markdown('<div class="section-pill">🏛️ Schemes</div>', unsafe_allow_html=True)
    st.header(T("schemes_header"))
    st.caption(T("schemes_subheader"))

    schemes = get_scheme_recommendations(worker)
    eligible = [s for s in schemes if s["is_eligible"]]
    ineligible = [s for s in schemes if not s["is_eligible"]]

    em1, em2, em3 = st.columns(3)
    em1.markdown(
        f'<div class="metric-card"><div class="value">{len(eligible)}</div><div class="label">Schemes Eligible</div></div>',
        unsafe_allow_html=True,
    )
    em2.markdown(
        f'<div class="metric-card"><div class="value">₹0</div><div class="label">Min. Annual Cost</div></div>',
        unsafe_allow_html=True,
    )
    em3.markdown(
        f'<div class="metric-card"><div class="value">₹{2+len(eligible)}L+</div><div class="label">Combined Coverage</div></div>',
        unsafe_allow_html=True,
    )
    st.markdown("<br>", unsafe_allow_html=True)

    def render_scheme(scheme: dict, expanded: bool = True):
        elig_label = T("eligible") if scheme["is_eligible"] else T("not_eligible")
        card_cls = "scheme-card" + ("" if scheme["is_eligible"] else " scheme-ineligible")
        with st.expander(f"{elig_label} · **{scheme['name']}** — {scheme['category']}", expanded=expanded):
            st.markdown(
                f"<div class='{card_cls}'>",
                unsafe_allow_html=True,
            )
            c1, c2 = st.columns(2)
            with c1:
                st.markdown(f"**{T('benefit')}:** {scheme['benefit']}")
                st.markdown(f"**{T('eligibility')}:** {scheme['eligibility']}")
                st.markdown(f"**Note:** _{scheme['eligibility_note']}_")
            with c2:
                st.markdown(f"**{T('contribution')}:** {scheme.get('contribution', 'N/A')}")
                st.markdown(f"**{T('enroll_at')}:** {scheme['enroll_at']}")
                docs = scheme.get("documents", [])
                if docs:
                    st.markdown(f"**{T('documents')}:** {', '.join(docs)}")
                st.markdown(f"[Learn More & Enroll →]({scheme['link']})")
            st.markdown("</div>", unsafe_allow_html=True)

    st.subheader(f"✅ Eligible Schemes ({len(eligible)})")
    for s in eligible:
        render_scheme(s, expanded=True)

    if ineligible:
        st.subheader(f"ℹ️ Other Schemes ({len(ineligible)})")
        for s in ineligible:
            render_scheme(s, expanded=False)

    # AI narrative
    st.markdown('<div class="glow-divider"></div>', unsafe_allow_html=True)
    st.subheader(T("ai_analysis"))
    if st.button("🤖 Generate Scheme Guidance", key="gen_scheme_ai"):
        with st.spinner("Checking your eligible schemes..."):
            narrative, is_live = get_scheme_narrative(worker, schemes, lang)
        if not is_live and narrative == "Sorry, I'm temporarily unable to respond. Please try again in a moment.":
            st.warning(narrative)
        else:
            st.info(narrative)


# ─────────────────────────────────────────────────────────────────────────────
# SECTION: AI Mentor Chat
# ─────────────────────────────────────────────────────────────────────────────
elif section == "chat":
    st.markdown('<div class="section-pill">🤖 AI Chat</div>', unsafe_allow_html=True)
    st.header(T("chat_header"))

    # Greeting on first load or language change
    if not st.session_state["chat_greeted"]:
        greeting = get_greeting(lang)
        st.session_state["chat_history"] = [{"role": "assistant", "content": greeting}]
        st.session_state["chat_greeted"] = True

    # Render history
    for msg in st.session_state["chat_history"]:
        if msg["role"] == "user":
            st.markdown(
                f'<div class="chat-bubble-user">👤 {msg["content"]}</div>',
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                f'<div class="chat-bubble-aasha">🌟 <b>Aasha:</b> {msg["content"]}</div>',
                unsafe_allow_html=True,
            )

    st.markdown("<br>", unsafe_allow_html=True)

    # Quick-question chips
    quick_questions = {
        "en": [
            "What jobs can I apply for?",
            "How do I enroll in PM-SYM?",
            "What free training is available?",
            "How can I increase my income?",
        ],
        "hi": [
            "मैं कौन सी नौकरी के लिए आवेदन कर सकता हूँ?",
            "PM-SYM में नामांकन कैसे करें?",
            "मुफ्त प्रशिक्षण कहाँ मिलेगा?",
            "अपनी आय कैसे बढ़ाएँ?",
        ],
        "ta": [
            "நான் எந்த வேலைக்கு விண்ணப்பிக்கலாம்?",
            "PM-SYM-ல் எவ்வாறு பதிவு செய்வது?",
            "இலவச பயிற்சி எங்கே கிடைக்கும்?",
            "என் வருமானத்தை எவ்வாறு அதிகரிப்பது?",
        ],
    }
    st.markdown('<p style="color:#64748b; font-size:0.8rem; text-transform:uppercase; letter-spacing:0.7px; margin-bottom:0.5rem;">Quick Questions</p>', unsafe_allow_html=True)
    q_cols = st.columns(4)
    for i, q in enumerate(quick_questions.get(lang, quick_questions["en"])):
        if q_cols[i].button(q, key=f"quick_{i}"):
            # Treat as user input
            st.session_state["chat_history"].append({"role": "user", "content": q})
            with st.spinner(T("thinking")):
                reply, is_live = get_mentor_response(
                    q,
                    st.session_state["chat_history"],
                    worker,
                    lang,
                )
            st.session_state["chat_history"].append({"role": "assistant", "content": reply})
            if not is_live:
                st.session_state["ai_status"] = False
            else:
                st.session_state["ai_status"] = True
            st.rerun()

    # Input
    with st.form("chat_form", clear_on_submit=True):
        user_input = st.text_input(
            T("chat_placeholder"),
            placeholder=T("chat_placeholder"),
            label_visibility="collapsed",
        )
        cs1, cs2 = st.columns([4, 1])
        submitted = cs1.form_submit_button(T("chat_send"), use_container_width=True, type="primary")
        cleared = cs2.form_submit_button(T("chat_clear"), use_container_width=True)

    if cleared:
        st.session_state["chat_history"] = []
        st.session_state["chat_greeted"] = False
        st.rerun()

    if submitted and user_input.strip():
        st.session_state["chat_history"].append({"role": "user", "content": user_input.strip()})
        with st.spinner(T("thinking")):
            reply, is_live = get_mentor_response(
                user_input.strip(),
                st.session_state["chat_history"],
                worker,
                lang,
            )
        st.session_state["chat_history"].append({"role": "assistant", "content": reply})
        st.session_state["ai_status"] = is_live
        st.rerun()

    st.markdown(
        '<div style="text-align:center; margin-top:2rem; padding-top:1rem; '
        'border-top:1px solid rgba(255,255,255,0.06); color:#374151; font-size:0.72rem; letter-spacing:0.5px;">'
        'AI Job Mentor · <span style="color:#00d4ff;">Aasha</span> · Your Career Guide</div>',
        unsafe_allow_html=True,
    )
