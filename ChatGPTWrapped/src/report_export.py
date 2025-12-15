from __future__ import annotations

from typing import Dict, Optional

import pandas as pd
import plotly.express as px
import plotly.io as pio
from plotly.subplots import make_subplots
import plotly.graph_objects as go

from .theme import ACCENT_COLOR, DATA_COLORS, MUTED_TEXT_COLOR, PRIMARY_FONT, SECONDARY_FONT, TEXT_COLOR


def _fmt_int(n: int) -> str:
    return f"{n:,}"


def build_wrapped_html(title: str,
                       tagline: str,
                       emoji: str,
                       metrics: Dict[str, float],
                       tokens_cat: pd.DataFrame,
                       tokens_time: pd.DataFrame,
                       highlights: Dict[str, object],
                       year_label: str) -> str:
    """Generate a single-file HTML report with embedded Plotly charts."""

    fig_cat = px.pie(tokens_cat, values="tokens", names="category", hole=0.55, color_discrete_sequence=DATA_COLORS)
    fig_cat.update_layout(margin=dict(l=20, r=20, t=20, b=20), height=360, showlegend=True)

    if not tokens_time.empty and "time" in tokens_time.columns:
        fig_time = px.area(tokens_time, x="time", y="tokens", color="role", color_discrete_sequence=DATA_COLORS)
        fig_time.update_layout(margin=dict(l=20, r=20, t=20, b=20), height=320, legend_title_text="")
        time_html = pio.to_html(fig_time, include_plotlyjs=False, full_html=False)
    else:
        time_html = ""

    cat_html = pio.to_html(fig_cat, include_plotlyjs="cdn", full_html=False)

    peak_day = highlights.get("peak_day")
    peak_day_tokens = int(highlights.get("peak_day_tokens", 0) or 0)
    busiest_hour = highlights.get("busiest_hour")

    css = f"""
    :root {{ --bg:#ffffff; --panel:#f6f7fb; --text:{TEXT_COLOR}; --muted:{MUTED_TEXT_COLOR}; --border:#d7dce7; --accent:{ACCENT_COLOR}; }}
    html, body {{ margin:0; padding:0; background:var(--bg); color:var(--text); font-family:{PRIMARY_FONT}; }}
    .wrap {{ max-width: 980px; margin: 0 auto; padding: 28px 18px 54px; }}
    .hero {{ border:1px solid var(--border); background:linear-gradient(135deg, #ffffff 0%, color-mix(in srgb, {ACCENT_COLOR} 10%, #f7fbff) 100%); border-radius: 16px; padding: 18px 18px 14px; }}
    .hero h1 {{ margin: 0; font-size: 28px; letter-spacing: -0.02em; }}
    .hero .tag {{ margin-top: 6px; color: var(--muted); font-size: 14px; font-family:{SECONDARY_FONT}; }}
    .grid {{ display:grid; grid-template-columns: repeat(3, 1fr); gap: 12px; margin-top: 12px; }}
    .card {{ border:1px solid var(--border); border-radius: 14px; padding: 12px; background: #fff; box-shadow: 0 10px 30px color-mix(in srgb, {ACCENT_COLOR} 10%, transparent); }}
    .k {{ font-size: 12px; color: var(--muted); font-family:{SECONDARY_FONT}; letter-spacing: 0.01em; }}
    .v {{ font-size: 20px; margin-top: 4px; color: var(--text); }}
    .section {{ margin-top: 18px; }}
    .section h2 {{ font-size: 16px; margin: 0 0 10px; letter-spacing: -0.01em; }}
    .small {{ color: var(--muted); font-size: 12px; margin-top: 6px; font-family:{SECONDARY_FONT}; }}
    .pill {{ display:inline-block; font-size: 12px; padding: 6px 10px; border:1px solid color-mix(in srgb, {ACCENT_COLOR} 35%, transparent); border-radius: 999px; background:color-mix(in srgb, {ACCENT_COLOR} 8%, #fff); margin-right: 8px; font-family:{SECONDARY_FONT}; }}
    @media (max-width: 780px) {{ .grid {{ grid-template-columns: 1fr; }} }}
    """

    return f"""<!doctype html>
<html>
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>ChatGPT Wrapped {year_label}</title>
  <style>{css}</style>
</head>
<body>
  <div class="wrap">
    <div class="hero">
      <h1>{emoji} {title} <span style="color:var(--muted); font-weight:500">· ChatGPT Wrapped {year_label}</span></h1>
      <div class="tag">{tagline}</div>
      <div class="grid">
        <div class="card"><div class="k">Estimated tokens</div><div class="v">{_fmt_int(int(metrics.get("tokens",0)))}</div></div>
        <div class="card"><div class="k">Messages</div><div class="v">{_fmt_int(int(metrics.get("messages",0)))}</div></div>
        <div class="card"><div class="k">Conversations</div><div class="v">{_fmt_int(int(metrics.get("conversations",0)))}</div></div>
      </div>
      <div class="small">
        <span class="pill">Peak day: {peak_day} ({_fmt_int(peak_day_tokens)} tokens)</span>
        <span class="pill">Busiest hour: {busiest_hour}:00</span>
        <span class="pill">Assistant share: {metrics.get("assistant_token_share",0)*100:.1f}%</span>
      </div>
    </div>

    <div class="section">
      <h2>What you used ChatGPT for</h2>
      {cat_html}
    </div>

    <div class="section">
      <h2>Your activity over time</h2>
      {time_html if time_html else '<div class="small">Not enough timestamped data to build a timeline.</div>'}
    </div>

    <div class="section">
      <h2>Notes</h2>
      <div class="small">Generated from your ChatGPT export. Token counts are estimated from message text.</div>
    </div>
  </div>
</body>
</html>
"""


def build_wrapped_jpg(title: str,
                      tagline: str,
                      emoji: str,
                      metrics: Dict[str, float],
                      tokens_cat: pd.DataFrame,
                      tokens_time: pd.DataFrame,
                      highlights: Dict[str, object],
                      year_label: str) -> Optional[bytes]:
    """Create a colour-rich JPG snapshot of the wrapped results."""

    fig = make_subplots(
        rows=2,
        cols=2,
        specs=[[{"type": "domain"}, {"type": "xy"}], [{"colspan": 2, "type": "xy"}, None]],
        vertical_spacing=0.16,
        horizontal_spacing=0.12,
        subplot_titles=("What you used ChatGPT for", "Tokens over time", "Top categories"),
    )

    if not tokens_cat.empty:
        fig.add_trace(
            go.Pie(
                labels=tokens_cat["category"],
                values=tokens_cat["tokens"],
                hole=0.55,
                marker=dict(colors=DATA_COLORS),
                textfont=dict(color=TEXT_COLOR, family=SECONDARY_FONT),
            ),
            row=1,
            col=1,
        )

    if not tokens_time.empty and "time" in tokens_time.columns:
        fig.add_trace(
            go.Scatter(
                x=tokens_time["time"],
                y=tokens_time["tokens"],
                mode="lines",
                name="Tokens",
                line=dict(color=DATA_COLORS[0], width=3),
                fill="tozeroy",
                fillcolor="rgba(65,138,179,0.18)",
            ),
            row=1,
            col=2,
        )

    top_cat = tokens_cat.head(6)
    if not top_cat.empty:
        fig.add_trace(
            go.Bar(
                x=top_cat["tokens"],
                y=top_cat["category"],
                orientation="h",
                marker=dict(color=DATA_COLORS),
                text=top_cat["tokens"].apply(_fmt_int),
                textposition="auto",
                name="Tokens",
            ),
            row=2,
            col=1,
        )

    title_block = f"{emoji} {title} · ChatGPT Wrapped {year_label}"
    fig.update_layout(
        title=dict(text=title_block, x=0.02, font=dict(size=26, family=PRIMARY_FONT, color=TEXT_COLOR)),
        annotations=[
            go.layout.Annotation(
                text=tagline,
                x=0.02,
                xref="paper",
                y=1.08,
                yref="paper",
                showarrow=False,
                font=dict(color=MUTED_TEXT_COLOR, family=SECONDARY_FONT, size=14),
            ),
            go.layout.Annotation(
                text=f"Tokens: {_fmt_int(int(metrics.get('tokens', 0)))} · Messages: {_fmt_int(int(metrics.get('messages', 0)))} · Conversations: {_fmt_int(int(metrics.get('conversations', 0)))}",
                x=0.02,
                xref="paper",
                y=-0.12,
                yref="paper",
                showarrow=False,
                font=dict(color=MUTED_TEXT_COLOR, family=SECONDARY_FONT),
            ),
        ],
        legend=dict(orientation="h", y=-0.1, x=0.4, font=dict(family=SECONDARY_FONT)),
        margin=dict(l=40, r=30, t=90, b=110),
        paper_bgcolor="#ffffff",
        plot_bgcolor="#ffffff",
        font=dict(family=PRIMARY_FONT, color=TEXT_COLOR),
        colorway=DATA_COLORS,
    )

    fig.update_xaxes(showgrid=True, gridcolor="rgba(12,18,32,0.08)")
    fig.update_yaxes(showgrid=True, gridcolor="rgba(12,18,32,0.08)")

    try:
        return pio.to_image(fig, format="jpg", width=1200, height=800, scale=2)
    except Exception:
        return None
