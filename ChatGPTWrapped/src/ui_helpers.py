from __future__ import annotations

import html
from typing import Optional, List

import streamlit as st


def inject_css() -> None:
    st.markdown(
        """
<style>
.block-container { padding-top: 1.1rem; padding-bottom: 2.2rem; max-width: 1200px; }
h1, h2, h3 { letter-spacing: -0.01em; }
.card {
  border: 1px solid rgba(11,18,32,0.10);
  border-radius: 16px;
  padding: 14px 14px 12px;
  background: white;
}
.card .k { font-size: 0.82rem; color: rgba(11,18,32,0.62); }
.card .v { font-size: 1.35rem; margin-top: 0.25rem; }
.pill {
  display: inline-block;
  border: 1px solid rgba(11,18,32,0.10);
  border-radius: 999px;
  padding: 0.2rem 0.55rem;
  font-size: 0.8rem;
  color: rgba(11,18,32,0.70);
  background: rgba(246,247,251,0.9);
  margin-right: 0.35rem;
  margin-bottom: 0.35rem;
}
.hr { height:1px; background: rgba(11,18,32,0.08); margin: 0.8rem 0; }
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
