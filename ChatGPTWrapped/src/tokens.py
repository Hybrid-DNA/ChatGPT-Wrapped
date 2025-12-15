from __future__ import annotations

import re
from typing import Callable

_CODE_HINTS = re.compile(r"(\bSELECT\b|\bCREATE\b|\bFROM\b|\bWHERE\b|def\s+|import\s+|```|\{|\};)", re.I)

def estimate_tokens_heuristic(text: str) -> int:
    """Stable heuristic: codey ~1 token per 3.1 chars, otherwise ~1 per 4 chars."""
    if not text:
        return 0
    t = text.strip()
    if not t:
        return 0
    divisor = 3.1 if _CODE_HINTS.search(t) else 4.0
    return max(1, int(len(t) / divisor))

def get_token_counter() -> Callable[[str], int]:
    """Return a lightweight token estimation function."""

    return estimate_tokens_heuristic
