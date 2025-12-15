from __future__ import annotations

import html
from typing import Optional, List

import streamlit as st
from .theme import (
    ACCENT_COLOR,
    BACKGROUND_COLOR,
    MUTED_TEXT_COLOR,
    PRIMARY_FONT,
    SECONDARY_FONT,
    TEXT_COLOR,
)


def inject_css() -> None:
    st.markdown(
        f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&family=Inter:wght@400;500;600&display=swap');

:root {{
  --bg: {BACKGROUND_COLOR};
  --text: {TEXT_COLOR};
  --muted: {MUTED_TEXT_COLOR};
  --accent: {ACCENT_COLOR};
  --accent-amber: #FEC306;
  --accent-green: #A6B727;
  --accent-orange: #DF5327;
  --font-primary: {PRIMARY_FONT};
  --font-secondary: {SECONDARY_FONT};
  color-scheme: light;
}}
html, body {{
  background:
    radial-gradient(circle at 12% 16%, color-mix(in srgb, var(--accent) 12%, transparent) 0, transparent 26%),
    linear-gradient(90deg, color-mix(in srgb, var(--accent) 6%, transparent) 1px, transparent 1px),
    linear-gradient(180deg, color-mix(in srgb, var(--accent) 4%, transparent) 1px, transparent 1px),
    var(--bg);
  background-size: 220px 220px, 120px 120px, 120px 120px, auto;
  color: var(--text);
  font-family: var(--font-primary);
}}
.block-container {{ padding-top: 1.1rem; padding-bottom: 2.2rem; max-width: 1200px; }}
h1, h2, h3 {{ letter-spacing: -0.01em; color: var(--text); font-weight: 700; }}
p, .stMarkdown {{ color: var(--text); font-family: var(--font-primary); }}
.stCaption, .st-emotion-cache-1kyxreq, .st-emotion-cache-1n76uvr {{ font-family: var(--font-secondary); color: var(--muted); }}

/* Sidebar */
.stSidebar {{
  background: linear-gradient(180deg, #f1f5fa 0%, #e5edf5 100%);
  color: var(--text);
  border-right: 1px solid color-mix(in srgb, var(--text) 10%, transparent);
}}
.stSidebar .stButton>button, .stSidebar .stDownloadButton>button {{
  border-radius: 12px;
  border: 1px solid color-mix(in srgb, var(--text) 12%, transparent);
  background: white;
  color: var(--text);
  box-shadow: 0 6px 16px color-mix(in srgb, var(--text) 8%, transparent);
}}

/* Hero */
.hero {{
  position: relative;
  overflow: hidden;
  padding: 22px 24px 24px;
  border-radius: 18px;
  background: linear-gradient(135deg, color-mix(in srgb, var(--accent) 12%, white) 0%, white 85%);
  color: var(--text);
  box-shadow: 0 18px 36px rgba(18, 53, 82, 0.12);
  border: 1px solid color-mix(in srgb, var(--text) 10%, transparent);
  }}
.hero__orbit {{
  position: absolute;
  inset: -10% 20% auto -10%;
  height: 220px;
  background: radial-gradient(circle, color-mix(in srgb, var(--accent) 14%, transparent) 0%, transparent 55%);
  filter: blur(20px);
}}
.hero__content {{ position: relative; z-index: 1; max-width: 720px; }}
.hero h1 {{ margin: 0 0 8px; font-size: 2.25rem; }}
.hero .lede {{ color: color-mix(in srgb, var(--text) 70%, var(--muted)); max-width: 640px; }}
.hero__glow {{
  position: absolute;
  right: -8%;
  top: -28%;
  width: 220px;
  height: 220px;
  background: radial-gradient(circle, color-mix(in srgb, var(--accent-orange) 22%, transparent) 0%, transparent 65%);
  filter: blur(16px);
  opacity: 0.65;
}}
.eyebrow {{ text-transform: uppercase; letter-spacing: 0.08em; font-size: 0.74rem; color: var(--muted); margin-bottom: 6px; font-family: var(--font-secondary); }}
.muted {{ color: color-mix(in srgb, var(--text) 55%, transparent); font-family: var(--font-secondary); }}
.hero__pills {{ margin-top: 10px; display: flex; gap: 0.5rem; flex-wrap: wrap; }}

/* Cards */
.card {{
  border: 1px solid color-mix(in srgb, var(--text) 10%, transparent);
  border-radius: 16px;
  padding: 14px 14px 12px;
  background: color-mix(in srgb, white 90%, color-mix(in srgb, var(--accent) 6%, transparent));
  box-shadow: 0 12px 32px rgba(18, 53, 82, 0.08);
  position: relative;
  overflow: hidden;
  }}
.card:before {{
  content: "";
  position: absolute;
  inset: -40% 28% 52% -38%;
  background: radial-gradient(circle, color-mix(in srgb, var(--accent-green) 22%, transparent) 0%, transparent 55%);
  opacity: 0.4;
}}
.card .k {{ font-size: 0.82rem; color: var(--muted); font-family: var(--font-secondary); letter-spacing: 0.02em; text-transform: uppercase; }}
.card .v {{ font-size: 1.45rem; margin-top: 0.3rem; color: var(--text); font-weight: 700; }}

/* Pills */
.pill {{
  display: inline-block;
  border: 1px solid color-mix(in srgb, var(--accent) 25%, transparent);
  border-radius: 999px;
  padding: 0.25rem 0.75rem;
  font-size: 0.85rem;
  color: var(--muted);
  background: color-mix(in srgb, var(--accent) 6%, white);
  margin-right: 0.35rem;
  margin-bottom: 0.35rem;
  font-family: var(--font-secondary);
  backdrop-filter: blur(3px);
  }}
.pill-strong {{ color: var(--text); background: white; border-color: color-mix(in srgb, var(--accent) 30%, white); font-weight: 600; }}
.hr {{ height:1px; background: color-mix(in srgb, var(--text) 9%, transparent); margin: 0.9rem 0; }}

/* Tabs & data */
.stTabs [data-baseweb="tab"] {{
  background: color-mix(in srgb, white 96%, transparent);
  border-radius: 12px 12px 0 0;
  margin-right: 0.25rem;
  padding: 0.75rem 1rem;
  font-weight: 600;
  border: 1px solid color-mix(in srgb, var(--text) 6%, transparent);
  border-bottom: none;
}}
.stTabs [data-baseweb="tab"]:hover {{
  background: color-mix(in srgb, var(--accent) 12%, white);
}}
.stTabs [data-baseweb="tab"]:active {{ transform: translateY(1px); }}
.stTabs [aria-selected="true"] {{
  color: var(--text);
  border-bottom: 2px solid var(--accent);
  background: color-mix(in srgb, var(--accent) 12%, white);
}}
.stDataFrame {{
  background: white;
  border-radius: 18px;
  border: 1px solid color-mix(in srgb, var(--text) 10%, transparent);
  box-shadow: 0 10px 24px rgba(18, 53, 82, 0.08);
  padding: 0.35rem;
}}

/* Empty state */
.empty-state {{
  display: flex;
  gap: 14px;
  align-items: center;
  background: color-mix(in srgb, var(--accent) 8%, white);
  border: 1px dashed color-mix(in srgb, var(--text) 18%, transparent);
  padding: 16px 18px;
  border-radius: 14px;
  box-shadow: 0 8px 18px rgba(18, 53, 82, 0.05);
}}
.empty-state__icon {{
  width: 48px;
  height: 48px;
  display: grid;
  place-items: center;
  background: white;
  border-radius: 12px;
  font-size: 1.4rem;
  box-shadow: inset 0 0 0 1px color-mix(in srgb, var(--accent) 16%, transparent);
}}

/* Buttons */
.stDownloadButton>button, .stButton>button {{
  background: linear-gradient(120deg, color-mix(in srgb, var(--accent) 85%, white) 0%, color-mix(in srgb, var(--accent-amber) 55%, white) 100%);
  color: #0b243b;
  border-radius: 12px;
  border: 1px solid color-mix(in srgb, var(--text) 8%, transparent);
  padding: 0.55rem 1rem;
  font-weight: 650;
  box-shadow: 0 12px 26px rgba(18, 53, 82, 0.16);
}}
.stDownloadButton>button:hover, .stButton>button:hover {{ filter: brightness(1.03); }}

/* Streamlit tweaks */
.st-emotion-cache-1u0u0jh p {{ color: var(--muted); }}
hr {{ border-color: color-mix(in srgb, var(--text) 10%, transparent); }}
</style>
""",
        unsafe_allow_html=True,
    )


def metric_card(label: str, value: str, help_text: Optional[str] = None) -> None:
    ht = f' title="{html.escape(help_text)}"' if help_text else ""
    st.markdown(
        f"""
<div class="card"{ht}>
  <div class="k">{html.escape(label)}</div>
  <div class="v">{html.escape(value)}</div>
</div>
""",
        unsafe_allow_html=True,
    )


def pills(items: List[str]) -> None:
    if not items:
        return
    st.markdown(
        "".join([f'<span class="pill">{html.escape(x)}</span>' for x in items if x]),
        unsafe_allow_html=True,
    )
