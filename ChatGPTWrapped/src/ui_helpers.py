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
  --font-primary: {PRIMARY_FONT};
  --font-secondary: {SECONDARY_FONT};
}}
html, body {{
  background: var(--bg);
  color: var(--text);
  font-family: var(--font-primary);
}}
.block-container {{ padding-top: 1.1rem; padding-bottom: 2.2rem; max-width: 1200px; }}
h1, h2, h3 {{ letter-spacing: -0.01em; color: var(--text); }}
p, .stMarkdown {{ color: var(--text); font-family: var(--font-primary); }}
.stCaption, .st-emotion-cache-1kyxreq, .st-emotion-cache-1n76uvr {{ font-family: var(--font-secondary); color: var(--muted); }}
.card {{
  border: 1px solid color-mix(in srgb, var(--text) 10%%, transparent);
  border-radius: 16px;
  padding: 14px 14px 12px;
  background: white;
  box-shadow: 0 6px 18px color-mix(in srgb, var(--accent) 12%%, transparent);
}}
.card .k {{ font-size: 0.82rem; color: var(--muted); font-family: var(--font-secondary); letter-spacing: 0.01em; }}
.card .v {{ font-size: 1.35rem; margin-top: 0.25rem; color: var(--text); }}
.pill {{
  display: inline-block;
  border: 1px solid color-mix(in srgb, var(--accent) 35%%, transparent);
  border-radius: 999px;
  padding: 0.2rem 0.55rem;
  font-size: 0.8rem;
  color: var(--muted);
  background: color-mix(in srgb, var(--accent) 8%%, white);
  margin-right: 0.35rem;
  margin-bottom: 0.35rem;
  font-family: var(--font-secondary);
}}
.hr {{ height:1px; background: color-mix(in srgb, var(--text) 9%%, transparent); margin: 0.8rem 0; }}
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
