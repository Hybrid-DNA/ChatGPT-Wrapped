from __future__ import annotations

import re
from dataclasses import dataclass
from typing import List, Pattern

@dataclass(frozen=True)
class CategoryRule:
    name: str
    pattern: Pattern[str]

# Keep patterns broad but not too noisy. Up to 10 buckets.
RULES: List[CategoryRule] = [
    CategoryRule("Data engineering and SQL", re.compile(r"\b(SELECT|INSERT|UPDATE|DELETE|CREATE|ALTER|DROP|PL/pgSQL|postgres|psql|uuid|index|join|window function)\b", re.I)),
    CategoryRule("App development and code", re.compile(r"\b(streamlit|stripe|frontend|backend|api|oauth|auth|typescript|javascript|react|tauri|rust|docker|cloud run|gcp|mysql)\b", re.I)),
    CategoryRule("Troubleshooting and tooling", re.compile(r"\b(error|stack trace|traceback|npm|vite|cargo|compile|dependency|cannot be resolved|failed to run|port\s+\d+\s+is\s+in\s+use)\b", re.I)),
    CategoryRule("Data quality and parsing", re.compile(r"\b(price_parser|parse_price|canonical|normalise|normalize|dedupe|edge case|test summary|false events|lineage)\b", re.I)),
    CategoryRule("AI and LLMs", re.compile(r"\b(chatgpt|claude|gemini|copilot|llm|prompt|hallucination|arena|model)\b", re.I)),
    CategoryRule("Security, privacy and compliance", re.compile(r"\b(gdpr|soc2|pii|privacy|leak|redact|compliance|governance|risk perception|data loss)\b", re.I)),
    CategoryRule("Analytics and reporting", re.compile(r"\b(power bi|dax|dashboard|oracle api|metrics|kpi|reporting|visuali[sz]ation)\b", re.I)),
    CategoryRule("Business strategy, finance and deals", re.compile(r"\b(jv|joint venture|acquisition|sell|search fund|private equity|due diligence|valuation|irr|wacc)\b", re.I)),
    CategoryRule("Writing, marketing and comms", re.compile(r"\b(linkedin|carousel|blog|seo|press|pr|media release|copywriting)\b", re.I)),
]

DEFAULT_CATEGORY = "Personal and lifestyle"

def categorise(text: str) -> str:
    if not text:
        return DEFAULT_CATEGORY
    for r in RULES:
        if r.pattern.search(text):
            return r.name
    return DEFAULT_CATEGORY
