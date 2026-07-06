"""Theme engine + reusable UI components.

Streamlit has no built-in runtime theme switching, so this module implements it:
the chosen theme lives in st.session_state["theme"], and apply_theme() injects a
CSS design-token block that restyles every widget. Call sidebar_header() first
(it renders the toggle), then apply_theme(), at the top of every page.
"""
from __future__ import annotations

from string import Template

import streamlit as st

# ---------------------------------------------------------------- tokens ----

DARK = {
    "bg": "#0A0C12",
    "bg2": "#0E1119",
    "surface": "#121623",
    "surface2": "#1A2030",
    "text": "#E7EAF3",
    "muted": "#98A2B8",
    "border": "rgba(255,255,255,.09)",
    "primary": "#818CF8",
    "primary2": "#C084FC",
    "chip": "rgba(129,140,248,.16)",
    "glow": "rgba(129,140,248,.10)",
    "shadow": "0 12px 34px rgba(0,0,0,.45)",
    "danger": "#F87171",
}

LIGHT = {
    "bg": "#FFFFFF",
    "bg2": "#F6F7FB",
    "surface": "#FFFFFF",
    "surface2": "#F1F3F9",
    "text": "#0F172A",
    "muted": "#5B6472",
    "border": "#E5E9F2",
    "primary": "#4F46E5",
    "primary2": "#7C3AED",
    "chip": "#EEF0FF",
    "glow": "rgba(79,70,229,.07)",
    "shadow": "0 10px 30px rgba(15,23,42,.08)",
    "danger": "#DC2626",
}

_CSS = Template("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@500;600;700&family=Inter:wght@400;500;600&family=JetBrains+Mono:wght@500&display=swap');

html, body, .stApp { color: $text; font-family: 'Inter', sans-serif; }
.stApp {
  background:
    radial-gradient(1100px 520px at 12% -8%, $glow, transparent 60%),
    radial-gradient(900px 480px at 95% 0%, $glow, transparent 55%),
    $bg;
}
[data-testid="stHeader"] { background: transparent; }

h1, h2, h3, h4, h5, h6 { font-family: 'Space Grotesk', sans-serif; letter-spacing: -.02em; color: $text; }
p, li, label, .stMarkdown, [data-testid="stWidgetLabel"] p { color: $text; }
[data-testid="stCaptionContainer"], .stCaption, small { color: $muted !important; }
a { color: $primary; }
hr { border-color: $border; }

/* ---------- sidebar ---------- */
[data-testid="stSidebar"] { background: $bg2; border-right: 1px solid $border; }
[data-testid="stSidebar"] * { color: $text; }
[data-testid="stSidebar"] [data-testid="stCaptionContainer"] { color: $muted !important; }

/* ---------- buttons ---------- */
.stButton button, .stDownloadButton button, .stFormSubmitButton button {
  background: linear-gradient(135deg, $primary, $primary2);
  color: #fff; border: 0; border-radius: 12px;
  padding: .55rem 1.1rem; font-weight: 600;
  box-shadow: $shadow; transition: transform .15s ease, filter .15s ease;
}
.stButton button:hover, .stDownloadButton button:hover {
  transform: translateY(-1px); filter: brightness(1.06); color: #fff;
}
.stButton button[kind="secondary"] {
  background: $surface; color: $text; border: 1px solid $border; box-shadow: none;
}
.stButton button[kind="secondary"]:hover { border-color: $primary; color: $primary; }

/* ---------- inputs ---------- */
.stTextInput input, .stTextArea textarea, .stNumberInput input {
  background: $surface !important; color: $text !important;
}
[data-baseweb="input"], [data-baseweb="base-input"], [data-baseweb="textarea"] {
  background: $surface !important; border: 1px solid $border !important; border-radius: 10px;
}
[data-baseweb="input"]:focus-within { border-color: $primary !important; }
.stTextInput input::placeholder, .stTextArea textarea::placeholder { color: $muted; }

/* ---------- tabs ---------- */
.stTabs [data-baseweb="tab-list"] { gap: 4px; border-bottom: 1px solid $border; }
.stTabs [data-baseweb="tab"] {
  background: transparent; color: $muted; border-radius: 10px 10px 0 0; padding: 8px 14px;
}
.stTabs [aria-selected="true"] { color: $primary !important; border-bottom: 2px solid $primary; }

/* ---------- chat ---------- */
[data-testid="stChatMessage"] {
  background: $surface; border: 1px solid $border; border-radius: 14px;
  padding: 4px 10px; margin-bottom: 6px;
}
[data-testid="stChatInput"] { background: transparent; }
[data-testid="stChatInput"] textarea { background: $surface !important; color: $text !important; }
[data-testid="stChatInput"] > div { border: 1px solid $border; border-radius: 14px; background: $surface; }

/* ---------- containers ---------- */
[data-testid="stExpander"] {
  background: $surface; border: 1px solid $border; border-radius: 12px;
}
[data-testid="stExpander"] summary { color: $text; }
[data-testid="stFileUploader"] {
  background: $surface; border: 1px dashed $border; border-radius: 12px; padding: 6px;
}
[data-testid="stFileUploader"] section { background: transparent; }
[data-testid="stMetric"] {
  background: $surface; border: 1px solid $border; border-radius: 12px; padding: 10px 14px;
}
[data-testid="stAlert"] { border-radius: 12px; }

/* uploaded pdf card */
[data-testid="stFileUploader"] li,
[data-testid^="stFileUploaderFile"],
[data-testid="stFileUploader"] [class*="uploadedFile"] {
  background: $surface !important;
  border: 1px solid $border !important;
  border-radius: 10px;
}
[data-testid="stFileUploader"] li *,
[data-testid^="stFileUploaderFile"] * {
  background: transparent !important;
  color: $text !important;
}
[data-testid="stFileUploader"] svg { fill: $text !important; }

/* ---------- light-mode parity ---------- */
[data-testid="stFileUploaderDropzone"] { background: $surface2 !important; }
[data-testid="stFileUploaderDropzone"] span,
[data-testid="stFileUploaderDropzone"] small,
[data-testid="stFileUploaderDropzone"] div { color: $muted !important; }
[data-testid="stFileUploader"] button {
  background: $surface !important; color: $text !important;
  border: 1px solid $border !important; border-radius: 8px !important;
}
[data-testid="stExpander"] summary p,
[data-testid="stExpander"] summary span { color: $text !important; }
[data-testid="stChatInput"] textarea::placeholder { color: $muted !important; }
[data-testid="stBottom"],
[data-testid="stBottom"] > div,
[data-testid="stBottomBlockContainer"],
.stChatFloatingInputContainer {
  background: $bg !important;
}
[data-testid="stExpander"] details,
[data-testid="stExpander"] summary {
  background: $surface !important;
  border-radius: 12px;
}
[data-testid="stExpander"] summary svg { fill: $text !important; }
[data-testid="stTooltipContent"], div[data-baseweb="tooltip"] {
  background: $surface2 !important; color: $text !important;
  border: 1px solid $border; border-radius: 8px;
}
[data-testid="stSpinner"], [data-testid="stCacheSpinner"], .stSpinner {
  background: $surface !important;
  border: 1px solid $border; border-radius: 10px; padding: 6px 10px;
}
[data-testid="stSpinner"] p, .stSpinner p,
[data-testid="stSpinner"] span, .stSpinner span { color: $text !important; }
/* toast notifications */
[data-testid="stToast"] {
  background: $surface !important; color: $text !important;
  border: 1px solid $border; border-radius: 12px;
}
[data-testid="stToast"] p, [data-testid="stToast"] span { color: $text !important; }

/* uploaded file cards inside the uploader */
[data-testid="stFileUploaderFile"] {
  background: $surface !important;
  border: 1px solid $border; border-radius: 10px;
}
[data-testid="stFileUploaderFile"] p, [data-testid="stFileUploaderFile"] span,
[data-testid="stFileUploaderFile"] small, [data-testid="stFileUploaderFile"] div { color: $text !important; }
[data-testid="stFileUploaderFile"] svg { fill: $text !important; }
[data-testid="stFileUploaderDeleteBtn"] button { background: transparent !important; box-shadow: none !important; }
[data-testid="stFileUploaderDeleteBtn"] svg { fill: $muted !important; }

/* ---------- custom components ---------- */
.rp-hero { padding: 1.6rem 0 .6rem; }
.rp-eyebrow {
  color: $primary; font-weight: 700; letter-spacing: .18em; font-size: .72rem;
  font-family: 'JetBrains Mono', monospace;
}
.rp-title { font-family: 'Space Grotesk'; font-size: 3rem; line-height: 1.06; margin: .35rem 0 .5rem; color: $text; }
.rp-title em { font-style: italic; font-family: Georgia, 'Times New Roman', serif; font-weight: 500; }
.grad {
  background: linear-gradient(135deg, $primary, $primary2);
  -webkit-background-clip: text; background-clip: text; color: transparent;
}
.rp-sub { color: $muted; font-size: 1.04rem; max-width: 660px; margin-bottom: .4rem; }

.rp-card {
  background: $surface; border: 1px solid $border; border-radius: 16px;
  padding: 1.25rem 1.35rem; box-shadow: $shadow; height: 100%;
  transition: transform .15s ease, border-color .15s ease;
}
.rp-card:hover { transform: translateY(-2px); border-color: $primary; }
.rp-kicker { font-size: 1.55rem; }
.rp-card h3 { margin: .35rem 0 .35rem; font-size: 1.15rem; }
.rp-card p { color: $muted; font-size: .92rem; margin: 0; }

.rp-pillrow { display: flex; gap: 8px; flex-wrap: wrap; align-items: center; margin: 10px 0 4px; }
.rp-pill {
  padding: 6px 13px; border-radius: 999px; font-size: .78rem; font-weight: 600;
  font-family: 'JetBrains Mono', monospace;
  border: 1px solid $border; color: $muted; background: $surface;
}
.rp-pill.active { border-color: $primary; color: $primary; background: $chip; }
.rp-pill.done { border-color: transparent; background: linear-gradient(135deg,$primary,$primary2); color: #fff; }
.rp-pill.error { border-color: $danger; color: $danger; }
.rp-arrow { color: $muted; font-size: .8rem; }

.rp-chip {
  display: inline-block; padding: 3px 10px; margin: 3px 4px 0 0; border-radius: 999px;
  font-size: .74rem; font-weight: 600; background: $chip; color: $primary; border: 1px solid $border;
}
.rp-badge {
  display: inline-block; padding: 4px 11px; margin: 3px; border-radius: 8px; font-size: .76rem;
  font-family: 'JetBrains Mono', monospace; background: $surface; border: 1px solid $border; color: $muted;
}
.rp-step-num {
  width: 26px; height: 26px; border-radius: 8px; background: $chip; color: $primary;
  display: inline-flex; align-items: center; justify-content: center; font-weight: 700;
  font-size: .8rem; margin-right: 9px; font-family: 'JetBrains Mono', monospace;
}
.rp-muted { color: $muted; }
</style>
""")

# ------------------------------------------------------------- functions ----


def _theme() -> dict:
    if "theme" not in st.session_state:
        st.session_state.theme = "dark"
    return DARK if st.session_state.theme == "dark" else LIGHT


def apply_theme() -> None:
    """Inject the CSS token block for the active theme. Call on every page."""
    st.markdown(_CSS.substitute(_theme()), unsafe_allow_html=True)


def sidebar_header() -> None:
    """Brand + dark/light toggle at the top of the sidebar. Call before apply_theme()."""
    if "theme" not in st.session_state:
        st.session_state.theme = "dark"
    with st.sidebar:
        st.markdown(
            "<div style='font-family:Space Grotesk,sans-serif;font-size:1.15rem;"
            "font-weight:700;padding:.2rem 0 0'>📄 RP&nbsp;Assistant</div>",
            unsafe_allow_html=True,
        )
        st.caption("Research papers, both directions.")
        dark_on = st.toggle(
            "🌙 Dark background",
            value=st.session_state.theme == "dark",
            key="_theme_toggle",
            help="Switch between black and white backgrounds",
        )
        st.session_state.theme = "dark" if dark_on else "light"
        st.divider()


def hero(eyebrow: str, title_html: str, subtitle: str) -> None:
    st.markdown(
        f"""
        <div class="rp-hero">
          <div class="rp-eyebrow">{eyebrow}</div>
          <div class="rp-title">{title_html}</div>
          <p class="rp-sub">{subtitle}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def feature_card(icon: str, title: str, body: str) -> None:
    st.markdown(
        f"""
        <div class="rp-card">
          <div class="rp-kicker">{icon}</div>
          <h3>{title}</h3>
          <p>{body}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def step_pills(steps: list[str], current: int, error: bool = False) -> str:
    """Pipeline pills: done < current, active == current (or error), pending > current.

    current == len(steps) marks everything done.
    """
    parts: list[str] = []
    for i, name in enumerate(steps):
        if i < current:
            cls, label = "done", f"✓ {name}"
        elif i == current:
            cls, label = ("error", f"✕ {name}") if error else ("active", f"● {name}")
        else:
            cls, label = "", name
        parts.append(f'<span class="rp-pill {cls}">{label}</span>')
        if i < len(steps) - 1:
            parts.append('<span class="rp-arrow">→</span>')
    return f'<div class="rp-pillrow">{"".join(parts)}</div>'


def chips(items: list[str]) -> str:
    return "".join(f'<span class="rp-chip">📄 {i}</span>' for i in items)


def badges(items: list[str]) -> None:
    st.markdown(
        "".join(f'<span class="rp-badge">{i}</span>' for i in items),
        unsafe_allow_html=True,
    )
