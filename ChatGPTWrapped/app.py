from __future__ import annotations

import json
import zipfile
from io import BytesIO
from datetime import date
from typing import Dict, List, Optional

import pandas as pd
import plotly.express as px
import streamlit as st

from src.analytics import (
    activity_heatmap,
    build_message_dataframe,
    conversation_level,
    highlights,
    top_keywords,
    tokens_by_category,
    tokens_by_category_and_role,
    tokens_over_time,
    totals,
)
from src.archetypes import add_flair, assign_archetype
from src.categorise import categorise
from src.parse_export import ParsedMessage, parse_conversations
from src.report_export import build_wrapped_html, build_wrapped_jpg
from src.tokens import get_token_counter
from src.ui_helpers import inject_css, metric_card, pills
from src.theme import HEATMAP_BLUE_SCALE, apply_plotly_theme, DATA_COLORS

APP_TITLE = "ChatGPT Wrapped"
DEFAULT_TZ = "Australia/Melbourne"


def _format_int(n: int) -> str:
    return f"{n:,}"


@st.cache_data(show_spinner=False)
def _load_messages_from_upload(raw: bytes, name: str, timezone: str) -> List[ParsedMessage]:
    """Parse an uploaded ChatGPT export into a list of messages.

    Caching prevents reparsing large exports on every rerun when users adjust filters
    or switch tabs, which keeps the app responsive.
    """

    if name.lower().endswith(".zip"):
        with zipfile.ZipFile(BytesIO(raw)) as zf:
            conv_path = None
            for c in ("conversations.json", "data/conversations.json", "chatgpt/conversations.json"):
                if c in zf.namelist():
                    conv_path = c
                    break
            if conv_path is None:
                for n in zf.namelist():
                    if n.lower().endswith("conversations.json"):
                        conv_path = n
                        break
            if conv_path is None:
                raise ValueError("Could not find conversations.json inside the ZIP export.")
            conv_data = json.loads(zf.read(conv_path).decode("utf-8"))
    else:
        conv_data = json.loads(raw.decode("utf-8"))

    return parse_conversations(conv_data, timezone=timezone)


@st.cache_data(show_spinner=False)
def _build_df(messages: List[ParsedMessage]) -> pd.DataFrame:
    counter = get_token_counter()

    rows: List[Dict] = []
    for m in messages:
        tok = counter(m.text)
        rows.append(
            {
                "conversation_id": m.conversation_id,
                "conversation_title": m.conversation_title,
                "message_id": m.message_id,
                "role": m.role,
                "created_at": m.created_at,
                "text": m.text,
                "tokens": int(tok),
                "category": categorise(m.text),
            }
        )
    return build_message_dataframe(rows)


def _year_options(df: pd.DataFrame) -> List[str]:
    years = sorted(df["year"].dropna().unique().tolist()) if not df.empty else []
    years = [str(int(y)) for y in years]
    return ["All time"] + years


def _filter_df(df: pd.DataFrame, year_choice: str, start: Optional[date], end: Optional[date]) -> pd.DataFrame:
    out = df
    if year_choice != "All time":
        try:
            y = int(year_choice)
            out = out[out["year"] == y]
        except Exception:
            pass

    if start:
        out = out[out["created_at"].dt.date >= start]
    if end:
        out = out[out["created_at"].dt.date <= end]

    return out


def _render_upload_sidebar() -> tuple[Optional[st.runtime.uploaded_file_manager.UploadedFile], str]:  # type: ignore[name-defined]
    """Render upload controls and return the chosen file and timezone."""

    with st.sidebar:
        st.subheader("Upload")
        uploaded = st.file_uploader("ChatGPT export (.zip) or conversations.json", type=["zip", "json"], key="export_upload")
        timezone = st.text_input("Timezone", value=DEFAULT_TZ, help="Used for grouping by day/hour.", key="timezone")

        st.divider()
        st.subheader("Token counting")
        st.caption("Token counts are estimated from message text; exports do not include official usage.")

    return uploaded, timezone


def _render_filter_sidebar(years: List[str]) -> tuple[str, bool, Optional[date], Optional[date]]:
    """Render filter inputs separately so they can be shown after data loads."""

    default_year = str(date.today().year)
    default_index = years.index(default_year) if default_year in years else 0
    default_start = st.session_state.get("start_date") or date.today()
    default_end = st.session_state.get("end_date") or date.today()

    with st.sidebar:
        st.divider()
        st.subheader("Filters")
        year_choice = st.selectbox("Year", options=years, index=default_index, key="year_choice")
        ignore_dates = st.checkbox("Ignore date range", value=st.session_state.get("ignore_dates", True), key="ignore_dates")
        start_date = st.date_input("Start date", value=default_start, disabled=ignore_dates, key="start_date")
        end_date = st.date_input("End date", value=default_end, disabled=ignore_dates, key="end_date")

    return year_choice, ignore_dates, start_date, end_date


def _render_archetype_summary(archetype, flair, metrics, token_label: str) -> None:
    left, right = st.columns([1.25, 1.0], gap="large")
    with left:
        st.markdown(f"## {archetype.emoji} **{archetype.title}**")
        st.markdown(archetype.tagline)
        pills(list(archetype.traits))
        st.markdown('<div class="hr"></div>', unsafe_allow_html=True)
        pills([flair.get("intensity", ""), flair.get("cadence", ""), flair.get("style", "")])

    with right:
        c1, c2, c3 = st.columns(3, gap="small")
        with c1:
            metric_card(token_label, _format_int(int(metrics.get("tokens", 0))), "Calculated from message text.")
        with c2:
            metric_card("Messages", _format_int(int(metrics.get("messages", 0))))
        with c3:
            metric_card("Conversations", _format_int(int(metrics.get("conversations", 0))))

        c4, c5, c6 = st.columns(3, gap="small")
        with c4:
            metric_card("You (tokens)", _format_int(int(metrics.get("user_tokens", 0))))
        with c5:
            metric_card("Assistant (tokens)", _format_int(int(metrics.get("assistant_tokens", 0))))
        with c6:
            metric_card("Assistant share", f"{metrics.get('assistant_token_share', 0) * 100:.1f}%")


def _render_wrapped_tab(cat_df, hi, kw):
    a, b = st.columns([1.05, 0.95], gap="large")
    with a:
        st.subheader("What you used ChatGPT for")
        fig = px.pie(cat_df, values="tokens", names="category", hole=0.55, color_discrete_sequence=DATA_COLORS)
        fig.update_layout(margin=dict(l=10, r=10, t=10, b=10), height=420, legend_title_text="")
        st.plotly_chart(fig, use_container_width=True)

    with b:
        st.subheader("Your highlights")
        items: List[str] = []
        if hi.get("peak_day"):
            items.append(f"Peak day: {hi['peak_day']} ({_format_int(int(hi.get('peak_day_tokens', 0)))} tokens)")
        if hi.get("busiest_hour") is not None:
            items.append(f"Busiest hour: {int(hi['busiest_hour'])}:00")
        top_conv = hi.get("top_conversation") or {}
        if top_conv:
            items.append(f"Biggest thread: {top_conv.get('title')} ({_format_int(int(top_conv.get('tokens', 0)))} tokens)")
        longest = hi.get("longest_assistant") or {}
        if longest:
            items.append(f"Longest assistant reply: {_format_int(int(longest.get('tokens', 0)))} tokens")

        for s in items:
            st.markdown(f"- {s}")

        st.markdown("")
        st.subheader("Top keywords")
        if kw.empty:
            st.caption("Not enough text to extract keywords.")
        else:
            st.dataframe(kw, use_container_width=True, height=330)


def _render_deep_dive_tab(ts_df, by_cat_role, hm):
    st.subheader("Activity over time")
    if not ts_df.empty:
        fig_ts = px.area(ts_df, x="time", y="tokens", color="role", color_discrete_sequence=DATA_COLORS)
        fig_ts.update_layout(margin=dict(l=10, r=10, t=10, b=10), height=360, legend_title_text="")
        st.plotly_chart(fig_ts, use_container_width=True)
    else:
        st.caption("Not enough timestamped data to build a timeline.")

    st.markdown("")
    c1, c2 = st.columns([1.0, 1.0], gap="large")
    with c1:
        st.subheader("Tokens by category and role")
        if not by_cat_role.empty:
            fig_bar = px.bar(by_cat_role, x="tokens", y="category", color="role", orientation="h", color_discrete_sequence=DATA_COLORS)
            fig_bar.update_layout(margin=dict(l=10, r=10, t=10, b=10), height=420, legend_title_text="")
            st.plotly_chart(fig_bar, use_container_width=True)

    with c2:
        st.subheader("When you use ChatGPT")
        if not hm.empty:
            hm2 = hm.copy()
            hm2.index.name = "Day"
            hm2.columns = [str(int(c)) for c in hm2.columns]
            fig_hm = px.imshow(hm2, aspect="auto", color_continuous_scale=HEATMAP_BLUE_SCALE)
            fig_hm.update_layout(margin=dict(l=10, r=10, t=10, b=10), height=420, coloraxis_showscale=False)
            st.plotly_chart(fig_hm, use_container_width=True)


def _render_conversation_tab(conv_df):
    st.subheader("Top conversations (by token count)")
    if conv_df.empty:
        st.caption("No conversations available under the current filters.")
    else:
        show = conv_df.head(50).copy()
        show["first_at"] = show["first_at"].dt.strftime("%Y-%m-%d")
        show["assistant_share"] = (show["assistant_share"] * 100).round(1)
        show = show.rename(
            columns={
                "conversation_title": "Title",
                "first_at": "First message",
                "messages": "Messages",
                "tokens": "Tokens",
                "assistant_share": "Assistant share (%)",
            }
        )
        st.dataframe(
            show[["Title", "First message", "Messages", "Tokens", "Assistant share (%)"]],
            use_container_width=True,
            height=520,
        )


def _render_downloads(year_choice, timezone, archetype, metrics, cat_df, ts_df, hi, df_f, conv_df):
    st.subheader("Download your results")
    year_label = year_choice if year_choice != "All time" else "All time"

    summary = {
        "year": year_label,
        "timezone": timezone,
        "archetype": {
            "title": archetype.title,
            "emoji": archetype.emoji,
            "tagline": archetype.tagline,
            "traits": list(archetype.traits),
        },
        "metrics": metrics,
        "highlights": {
            "peak_day": str(hi.get("peak_day")),
            "peak_day_tokens": int(hi.get("peak_day_tokens", 0)),
            "busiest_hour": hi.get("busiest_hour"),
            "top_conversation": hi.get("top_conversation"),
            "longest_assistant": hi.get("longest_assistant"),
        },
        "top_categories": cat_df.head(10).to_dict(orient="records"),
    }

    st.download_button(
        "Download summary (JSON)",
        data=json.dumps(summary, default=str, indent=2).encode("utf-8"),
        file_name=f"chatgpt_wrapped_{year_label.replace(' ', '_').lower()}.json",
        mime="application/json",
    )

    st.download_button(
        "Download per-message data (CSV)",
        data=df_f.to_csv(index=False).encode("utf-8"),
        file_name=f"chatgpt_messages_{year_label.replace(' ', '_').lower()}.csv",
        mime="text/csv",
    )

    st.download_button(
        "Download per-conversation data (CSV)",
        data=conv_df.to_csv(index=False).encode("utf-8"),
        file_name=f"chatgpt_conversations_{year_label.replace(' ', '_').lower()}.csv",
        mime="text/csv",
    )

    html = build_wrapped_html(
        title=archetype.title,
        tagline=archetype.tagline,
        emoji=archetype.emoji,
        metrics=metrics,
        tokens_cat=cat_df,
        tokens_time=ts_df,
        highlights=hi,
        year_label=year_label,
    )

    st.download_button(
        "Download shareable HTML report",
        data=html.encode("utf-8"),
        file_name=f"chatgpt_wrapped_{year_label.replace(' ', '_').lower()}.html",
        mime="text/html",
        help="A single HTML file you can open in a browser and share.",
    )

    jpg_bytes = None
    jpg_error: Optional[str] = None
    try:
        jpg_bytes = build_wrapped_jpg(
            title=archetype.title,
            tagline=archetype.tagline,
            emoji=archetype.emoji,
            metrics=metrics,
            tokens_cat=cat_df,
            tokens_time=ts_df,
            highlights=hi,
            year_label=year_label,
        )
    except Exception as e:
        jpg_error = str(e)

    if jpg_bytes:
        st.image(jpg_bytes, caption="Shareable JPG preview", use_column_width=True)
        st.download_button(
            "Download shareable JPG",
            data=jpg_bytes,
            file_name=f"chatgpt_wrapped_{year_label.replace(' ', '_').lower()}.jpg",
            mime="image/jpeg",
        )
    else:
        st.info(
            "Install optional image dependencies (kaleido) to generate a JPG preview." if not jpg_error else f"Could not generate JPG preview: {jpg_error}"
        )

    st.caption("Token counts are estimated from the export text. ChatGPT exports do not include official token usage.")


def main() -> None:
    st.set_page_config(page_title=APP_TITLE, page_icon="✨", layout="wide")
    apply_plotly_theme()
    inject_css()

    st.title("✨ ChatGPT Wrapped")
    st.caption("Upload your ChatGPT export and get a clean, shareable year-in-review.")

    uploaded, timezone = _render_upload_sidebar()

    if not uploaded:
        st.info("Upload a ChatGPT export ZIP or a conversations.json file to begin.")
        st.stop()

    upload_name = getattr(uploaded, "name", "") or ""
    upload_bytes = uploaded.getvalue()

    try:
        with st.spinner("Parsing export..."):
            messages = _load_messages_from_upload(upload_bytes, upload_name, timezone=timezone)
    except Exception as e:
        st.error(f"Could not parse the uploaded file: {e}")
        st.stop()

    df = _build_df(messages)
    if df.empty:
        st.warning("No messages found in this export (or messages had no text).")
        st.stop()

    # Re-render Year selector with real options after load
    years = _year_options(df)
    year_choice, ignore_dates, start_date, end_date = _render_filter_sidebar(years)

    df_f = _filter_df(df, year_choice, None if ignore_dates else start_date, None if ignore_dates else end_date)

    conv_df = conversation_level(df_f)
    metrics = totals(df_f)
    cat_df = tokens_by_category(df_f)
    by_cat_role = tokens_by_category_and_role(df_f)
    ts_df = tokens_over_time(df_f, freq="D")
    hm = activity_heatmap(df_f)
    kw = top_keywords(df_f, n=25)
    hi = highlights(df_f, conv_df)

    archetype = assign_archetype(cat_df)
    flair = add_flair(metrics)

    token_label = "Tokens (estimated)"
    _render_archetype_summary(archetype, flair, metrics, token_label)

    tab_wrapped, tab_dive, tab_convos, tab_download = st.tabs(["Wrapped", "Deep dive", "Conversations", "Download"])

    with tab_wrapped:
        _render_wrapped_tab(cat_df, hi, kw)

    with tab_dive:
        _render_deep_dive_tab(ts_df, by_cat_role, hm)

    with tab_convos:
        _render_conversation_tab(conv_df)

    with tab_download:
        _render_downloads(year_choice, timezone, archetype, metrics, cat_df, ts_df, hi, df_f, conv_df)


if __name__ == "__main__":
    main()
