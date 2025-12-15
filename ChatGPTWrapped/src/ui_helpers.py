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
:root {{
  --bg: {BACKGROUND_COLOR};
  --text: {TEXT_COLOR};
  --muted: {MUTED_TEXT_COLOR};
  --accent: {ACCENT_COLOR};
  --surface: #ffffff;
  --border: #e5e7eb;
  --accent-soft: color-mix(in srgb, var(--accent) 14%, white);
  --font-primary: {PRIMARY_FONT};
  --font-secondary: {SECONDARY_FONT};
  color-scheme: light;
}}
html, body {{
  background: var(--bg);
  color: var(--text);
  font-family: var(--font-primary);
}}
.block-container {{ padding-top: 1.4rem; padding-bottom: 2.4rem; max-width: 1200px; }}
h1, h2, h3 {{ letter-spacing: -0.01em; color: var(--text); font-weight: 700; }}
p, .stMarkdown {{ color: var(--text); font-family: var(--font-primary); line-height: 1.55; }}
.stCaption, .st-emotion-cache-1kyxreq, .st-emotion-cache-1n76uvr {{ font-family: var(--font-secondary); color: var(--muted); }}

/* Sidebar */
.stSidebar {{
  background: var(--surface);
  color: var(--text);
  border-right: 1px solid var(--border);
}}
.stSidebar .stButton>button, .stSidebar .stDownloadButton>button {{
  border-radius: 10px;
  border: 1px solid var(--border);
  background: var(--surface);
  color: var(--text);
  box-shadow: none;
}}

/* Hero */
.hero {{
  position: relative;
  overflow: hidden;
  padding: 0;
  border-radius: 0;
  background: transparent;
  color: var(--text);
  box-shadow: none;
  border: none;
  display: grid;
  grid-template-columns: 1fr;
  gap: 0.5rem;
}}
.hero__orbit {{
  position: absolute;
  inset: 4% auto auto 72%;
  width: 120px;
  height: 120px;
  background: radial-gradient(circle, var(--accent-soft) 0%, transparent 70%);
  filter: blur(6px);
  opacity: 0.75;
}}
.hero__content {{ position: relative; z-index: 1; max-width: 840px; }}
.hero h1 {{ margin: 0 0 8px; font-size: 2.15rem; }}
.hero .lede {{ color: var(--muted); max-width: 640px; }}
.hero__glow {{ display: none; }}
.eyebrow {{ text-transform: uppercase; letter-spacing: 0.08em; font-size: 0.76rem; color: var(--muted); margin-bottom: 6px; font-family: var(--font-secondary); }}
.muted {{ color: var(--muted); font-family: var(--font-secondary); }}
.hero__pills {{ margin-top: 10px; display: flex; gap: 0.5rem; flex-wrap: wrap; }}

/* Cards */
.card {{
  border: 1px solid var(--border);
  border-radius: 14px;
  padding: 14px 14px 12px;
  background: var(--surface);
  box-shadow: 0 12px 30px rgba(17, 24, 39, 0.06);
}}
.card .k {{ font-size: 0.82rem; color: var(--muted); font-family: var(--font-secondary); letter-spacing: 0.04em; text-transform: uppercase; }}
.card .v {{ font-size: 1.42rem; margin-top: 0.3rem; color: var(--text); font-weight: 700; }}

/* Pills */
.pill {{
  display: inline-block;
  border: 1px solid var(--border);
  border-radius: 999px;
  padding: 0.3rem 0.8rem;
  font-size: 0.88rem;
  color: var(--muted);
  background: #f5f7fb;
  margin-right: 0.35rem;
  margin-bottom: 0.35rem;
  font-family: var(--font-secondary);
}}
.pill-strong {{ color: var(--text); background: color-mix(in srgb, var(--accent) 12%, white); border-color: var(--border); font-weight: 600; }}
.hr {{ height:1px; background: var(--border); margin: 0.9rem 0; }}

/* Tabs & data */
.stTabs [data-baseweb="tab"] {{
  background: #f5f7fb;
  border-radius: 12px 12px 0 0;
  margin-right: 0.25rem;
  padding: 0.72rem 0.95rem;
  font-weight: 600;
  border: 1px solid var(--border);
  border-bottom: none;
}}
.stTabs [data-baseweb="tab"]:hover {{
  background: color-mix(in srgb, var(--accent) 10%, white);
}}
.stTabs [data-baseweb="tab"]:active {{ transform: translateY(1px); }}
.stTabs [aria-selected="true"] {{
  color: var(--text);
  border-bottom: 2px solid var(--accent);
  background: color-mix(in srgb, var(--accent) 12%, white);
}}
.stDataFrame {{
  background: var(--surface);
  border-radius: 16px;
  border: 1px solid var(--border);
  box-shadow: 0 8px 22px rgba(17, 24, 39, 0.06);
  padding: 0.25rem;
}}

/* Empty state */
.empty-state {{
  display: flex;
  gap: 14px;
  align-items: center;
  background: color-mix(in srgb, var(--accent) 8%, white);
  border: 1px dashed var(--border);
  padding: 16px 18px;
  border-radius: 14px;
  box-shadow: none;
}}
.empty-state__icon {{
  width: 48px;
  height: 48px;
  display: grid;
  place-items: center;
  background: var(--surface);
  border-radius: 12px;
  font-size: 1.4rem;
  border: 1px solid var(--border);
}}

/* Buttons */
.stDownloadButton>button, .stButton>button {{
  background: var(--accent);
  color: #ffffff;
  border-radius: 10px;
  border: 1px solid color-mix(in srgb, var(--accent) 40%, var(--border));
  padding: 0.55rem 1rem;
  font-weight: 650;
  box-shadow: 0 10px 24px rgba(65, 138, 179, 0.18);
}}
.stDownloadButton>button:hover, .stButton>button:hover {{ filter: brightness(1.05); }}

/* Streamlit tweaks */
.st-emotion-cache-1u0u0jh p {{ color: var(--muted); }}
hr {{ border-color: var(--border); }}
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
