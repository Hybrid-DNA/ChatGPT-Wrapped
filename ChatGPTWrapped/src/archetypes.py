from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Tuple

import pandas as pd


@dataclass(frozen=True)
class Archetype:
    title: str
    tagline: str
    emoji: str
    traits: Tuple[str, str, str]


ARCHETYPES = {
    "Data engineering and SQL": Archetype(
        title="Technician",
        tagline="You chase correctness, performance, and clean data like it is a sport.",
        emoji="🛠️",
        traits=("Rigorous", "Systems-minded", "Relentless about edge cases"),
    ),
    "Security, privacy and compliance": Archetype(
        title="Guardian",
        tagline="You prioritise trust, governance, and safe adoption over hype.",
        emoji="🛡️",
        traits=("Risk-aware", "Practical", "Trust-first"),
    ),
    "AI and LLMs": Archetype(
        title="Explorer",
        tagline="You test new models and workflows, looking for real leverage.",
        emoji="🧭",
        traits=("Curious", "Fast learner", "Tool-oriented"),
    ),
    "Business strategy, finance and deals": Archetype(
        title="Strategist",
        tagline="You think in trade-offs, incentives, and paths to scale.",
        emoji="♟️",
        traits=("Commercial", "Decisive", "Option-creating"),
    ),
    "Writing, marketing and comms": Archetype(
        title="Storyteller",
        tagline="You turn ideas into language that moves people.",
        emoji="🖋️",
        traits=("Clear", "Persuasive", "Audience-aware"),
    ),
    "App development and code": Archetype(
        title="Builder",
        tagline="You ship tools, prototypes, and platforms that make work easier.",
        emoji="🏗️",
        traits=("Hands-on", "Iterative", "Product-minded"),
    ),
    "Analytics and reporting": Archetype(
        title="Analyst",
        tagline="You make data legible and decision-ready.",
        emoji="📈",
        traits=("Insightful", "Structured", "Outcome-focused"),
    ),
    "Troubleshooting and tooling": Archetype(
        title="Fixer",
        tagline="You keep the machine running, one thorny error at a time.",
        emoji="🔧",
        traits=("Pragmatic", "Persistent", "Detail-oriented"),
    ),
    "Data quality and parsing": Archetype(
        title="Archivist",
        tagline="You care about truth over time, canonical records, and clean history.",
        emoji="📚",
        traits=("Precise", "Audit-friendly", "Consistency-obsessed"),
    ),
    "Personal and lifestyle": Archetype(
        title="Adventurer",
        tagline="You mix the serious with the fun. Work hard, play thoughtfully.",
        emoji="✨",
        traits=("Well-rounded", "Playful", "Human-first"),
    ),
}


def assign_archetype(tokens_by_category: pd.DataFrame) -> Archetype:
    if tokens_by_category.empty:
        return ARCHETYPES["Personal and lifestyle"]
    top_cat = str(tokens_by_category.iloc[0]["category"])
    return ARCHETYPES.get(top_cat, ARCHETYPES["Personal and lifestyle"])


def add_flair(metrics: Dict[str, float]) -> Dict[str, str]:
    tokens = metrics.get("tokens", 0)
    conversations = metrics.get("conversations", 0)
    assistant_share = metrics.get("assistant_token_share", 0.0)

    lines: Dict[str, str] = {}
    if tokens >= 2_000_000:
        lines["intensity"] = "High-volume year: you treated ChatGPT like a second brain."
    elif tokens >= 500_000:
        lines["intensity"] = "Consistent year: you used ChatGPT as a daily work partner."
    else:
        lines["intensity"] = "Light-touch year: you dipped in when it mattered."

    if conversations >= 1000:
        lines["cadence"] = "You work in lots of threads: rapid context switching, fast iteration."
    elif conversations >= 200:
        lines["cadence"] = "You build a healthy number of threads: project-based exploration."
    else:
        lines["cadence"] = "You keep things focused: fewer threads, deeper dives."

    if assistant_share >= 0.85:
        lines["style"] = "You prompt for deep outputs and big syntheses."
    elif assistant_share >= 0.65:
        lines["style"] = "Balanced dialogue: you steer, ChatGPT elaborates."
    else:
        lines["style"] = "You do more of the talking: short replies and quick turns."

    return lines
