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


PRIMARY_ARCHETYPES = {
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


SECONDARY_ARCHETYPES: Dict[Tuple[str, str], Archetype] = {
    ("AI and LLMs", "App development and code"): Archetype(
        title="Applied Futurist",
        tagline="You pair models with shipping discipline—ideas leave the lab fast.",
        emoji="🚀",
        traits=("Prototype-hungry", "Tool-builder", "Impact-driven"),
    ),
    ("AI and LLMs", "Writing, marketing and comms"): Archetype(
        title="Narrative Synthesist",
        tagline="You turn model outputs into stories that persuade and teach.",
        emoji="🪄",
        traits=("Translational", "Audience-savvy", "Pattern-spotter"),
    ),
    ("AI and LLMs", "Business strategy, finance and deals"): Archetype(
        title="Venture Scout",
        tagline="You scan emerging tech for leverage, moats, and upside.",
        emoji="🏔️",
        traits=("Opportunity-first", "Model-aware", "Market translator"),
    ),
    ("AI and LLMs", "Data engineering and SQL"): Archetype(
        title="Model Wrangler",
        tagline="You connect clean data to hungry models and keep the pipes flowing.",
        emoji="🧰",
        traits=("Structured", "Integration-minded", "Reliability-focused"),
    ),
    ("App development and code", "Troubleshooting and tooling"): Archetype(
        title="Systems First Responder",
        tagline="You debug, patch, and ship—often in the same afternoon.",
        emoji="🩹",
        traits=("Resilient", "Hands-on", "Latency-sensitive"),
    ),
    ("App development and code", "Security, privacy and compliance"): Archetype(
        title="Secure Builder",
        tagline="You ship features with guardrails baked in from day one.",
        emoji="🧱",
        traits=("Threat-aware", "Practical", "Defense-in-depth"),
    ),
    ("Data engineering and SQL", "Analytics and reporting"): Archetype(
        title="Pipeline Navigator",
        tagline="You architect flows that make analysis trustworthy and fast.",
        emoji="🛰️",
        traits=("End-to-end thinker", "Schema-loyal", "Latency-aware"),
    ),
    ("Data engineering and SQL", "Data quality and parsing"): Archetype(
        title="Data Conservator",
        tagline="You obsess over lineage, versioning, and long-lived truth.",
        emoji="🏺",
        traits=("Steady", "Documentation-forward", "Future-proof"),
    ),
    ("Analytics and reporting", "Writing, marketing and comms"): Archetype(
        title="Insight Narrator",
        tagline="You translate dashboards into decisions with crisp prose.",
        emoji="🗺️",
        traits=("Plain-language", "Audience-aware", "Outcome-anchored"),
    ),
    ("Business strategy, finance and deals", "Analytics and reporting"): Archetype(
        title="Board Whisperer",
        tagline="You distill numbers into moves, risks, and next bets.",
        emoji="🏛️",
        traits=("Executive-ready", "Synthesis-heavy", "Scenario-minded"),
    ),
    ("Business strategy, finance and deals", "AI and LLMs"): Archetype(
        title="Automation Strategist",
        tagline="You map AI experiments to revenue, margin, and durable advantage.",
        emoji="🧮",
        traits=("Commercial", "Experiment-friendly", "Leveraged"),
    ),
    ("Writing, marketing and comms", "Personal and lifestyle"): Archetype(
        title="Voice Crafter",
        tagline="You weave work, hobbies, and story-telling into one fluent feed.",
        emoji="🎙️",
        traits=("Expressive", "Empathetic", "Curator"),
    ),
    ("Security, privacy and compliance", "AI and LLMs"): Archetype(
        title="Safety Pilot",
        tagline="You champion responsible adoption while keeping experimentation alive.",
        emoji="🛰️",
        traits=("Governance-minded", "Pragmatic", "Calm"),
    ),
    ("Security, privacy and compliance", "Data quality and parsing"): Archetype(
        title="Governance Steward",
        tagline="You ensure records, access, and policy all stay in sync.",
        emoji="📜",
        traits=("Custodial", "Checklist-loyal", "Risk-aware"),
    ),
    ("Troubleshooting and tooling", "Data quality and parsing"): Archetype(
        title="Reliability Custodian",
        tagline="You hunt flaky links and tidy logs until everything hums.",
        emoji="🧹",
        traits=("Diagnostic", "Patient", "Observability-driven"),
    ),
}


def assign_archetype(tokens_by_category: pd.DataFrame) -> Archetype:
    if tokens_by_category.empty:
        return PRIMARY_ARCHETYPES["Personal and lifestyle"]

    top_row = tokens_by_category.iloc[0]
    top_cat = str(top_row["category"])

    second_cat = None
    if len(tokens_by_category) > 1:
        second_cat = str(tokens_by_category.iloc[1]["category"])

    if top_cat and second_cat:
        combo_key = (top_cat, second_cat)
        if combo_key in SECONDARY_ARCHETYPES:
            return SECONDARY_ARCHETYPES[combo_key]

    return PRIMARY_ARCHETYPES.get(top_cat, PRIMARY_ARCHETYPES["Personal and lifestyle"])


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
