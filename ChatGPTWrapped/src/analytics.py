from __future__ import annotations

from typing import Dict, List

import numpy as np
import pandas as pd


def build_message_dataframe(rows: List[Dict]) -> pd.DataFrame:
    df = pd.DataFrame(rows)
    if df.empty:
        return df

    df["created_at"] = pd.to_datetime(df["created_at"], utc=False, errors="coerce")
    df = df.dropna(subset=["created_at"])
    df["date"] = df["created_at"].dt.date
    df["year"] = df["created_at"].dt.year
    df["month"] = df["created_at"].dt.to_period("M").astype(str)
    df["dow"] = df["created_at"].dt.day_name()
    df["hour"] = df["created_at"].dt.hour
    df["is_user"] = df["role"].eq("user")
    df["is_assistant"] = df["role"].eq("assistant")
    df["words"] = df["text"].fillna("").astype(str).str.split().map(len)

    return df


def conversation_level(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty:
        return df

    g = df.groupby(["conversation_id", "conversation_title"], dropna=False)
    out = g.agg(
        first_at=("created_at", "min"),
        last_at=("created_at", "max"),
        messages=("message_id", "count"),
        tokens=("tokens", "sum"),
        words=("words", "sum"),
        user_tokens=("tokens", lambda s: s[df.loc[s.index, "is_user"]].sum()),
        assistant_tokens=("tokens", lambda s: s[df.loc[s.index, "is_assistant"]].sum()),
    ).reset_index()

    out["duration_minutes"] = (out["last_at"] - out["first_at"]).dt.total_seconds() / 60.0
    out["assistant_share"] = np.where(out["tokens"] > 0, out["assistant_tokens"] / out["tokens"], np.nan)
    return out.sort_values("tokens", ascending=False)


def totals(df: pd.DataFrame) -> Dict[str, float]:
    if df.empty:
        return {}

    total_tokens = float(df["tokens"].sum())
    user_tokens = float(df.loc[df["is_user"], "tokens"].sum())
    assistant_tokens = float(df.loc[df["is_assistant"], "tokens"].sum())

    return {
        "messages": int(df.shape[0]),
        "conversations": int(df["conversation_id"].nunique()),
        "tokens": int(total_tokens),
        "user_tokens": int(user_tokens),
        "assistant_tokens": int(assistant_tokens),
        "assistant_token_share": (assistant_tokens / total_tokens) if total_tokens else 0.0,
        "words": int(df["words"].sum()),
    }


def tokens_by_category(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty:
        return df
    return (df.groupby("category", dropna=False)["tokens"]
            .sum()
            .sort_values(ascending=False)
            .reset_index())


def tokens_by_category_and_role(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty:
        return df
    return (df.groupby(["category", "role"], dropna=False)["tokens"]
            .sum()
            .reset_index())


def tokens_over_time(df: pd.DataFrame, freq: str = "D") -> pd.DataFrame:
    if df.empty:
        return df
    ts = df.set_index("created_at").groupby("role")["tokens"].resample(freq).sum().reset_index()
    ts.rename(columns={"created_at": "time"}, inplace=True)
    return ts


def activity_heatmap(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty:
        return df

    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    df2 = df.copy()
    df2["dow"] = pd.Categorical(df2["dow"], categories=days, ordered=True)
    piv = pd.pivot_table(df2, values="tokens", index="dow", columns="hour", aggfunc="sum", fill_value=0)
    return piv.reindex(index=days)


def top_keywords(df: pd.DataFrame, n: int = 25) -> pd.DataFrame:
    if df.empty:
        return pd.DataFrame(columns=["keyword", "count"])

    stop = {
        "the","a","an","and","or","to","of","in","for","on","with","is","it","this","that","be","as","are",
        "i","you","we","they","he","she","them","us","my","your","our","me","at","from","by","not","but",
        "can","could","would","should","do","does","did","so","if","then","than","just","like",
        "select","def","join","null","class","function","return","while","break","continue","import","export",
    }

    text = " ".join(df["text"].astype(str).tolist()).lower()
    import re
    words = re.findall(r"[a-z0-9_']{3,}", text)
    words = [w for w in words if w not in stop and not w.isdigit() and "_" not in w]
    if not words:
        return pd.DataFrame(columns=["keyword", "count"])

    s = pd.Series(words).value_counts().head(n).reset_index()
    s.columns = ["keyword", "count"]
    return s


def highlights(df: pd.DataFrame, conv_df: pd.DataFrame) -> Dict[str, object]:
    if df.empty:
        return {}

    day = df.groupby("date")["tokens"].sum().sort_values(ascending=False)
    peak_day = day.index[0] if len(day) else None
    peak_day_tokens = int(day.iloc[0]) if len(day) else 0

    hr = df.groupby("hour")["tokens"].sum().sort_values(ascending=False)
    busiest_hour = int(hr.index[0]) if len(hr) else None

    top_conv = None
    if not conv_df.empty:
        top = conv_df.sort_values("tokens", ascending=False).iloc[0]
        top_conv = {
            "title": str(top["conversation_title"]),
            "tokens": int(top["tokens"]),
            "messages": int(top["messages"]),
            "first_at": top["first_at"],
        }

    a = df[df["is_assistant"]].sort_values("tokens", ascending=False)
    longest_assistant = None
    if not a.empty:
        row = a.iloc[0]
        longest_assistant = {
            "conversation_title": row["conversation_title"],
            "tokens": int(row["tokens"]),
            "created_at": row["created_at"],
        }

    return {
        "peak_day": peak_day,
        "peak_day_tokens": peak_day_tokens,
        "busiest_hour": busiest_hour,
        "top_conversation": top_conv,
        "longest_assistant": longest_assistant,
    }
