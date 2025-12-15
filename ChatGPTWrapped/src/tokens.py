from __future__ import annotations

import re
from typing import Callable, Optional, Tuple

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

def get_token_counter() -> Tuple[Callable[[str], int], bool, Optional[Exception]]:
    """Return a lightweight token estimation function and availability info.

    Tries to import ``tiktoken`` for more realistic counts and falls back to the
    heuristic estimator when the dependency is missing.
    """

    try:
        import tiktoken

        enc = tiktoken.get_encoding("cl100k_base")

        def counter(text: str) -> int:
            if not text:
                return 0
            return len(enc.encode(text))

        return counter, True, None
    except Exception as e:  # pragma: no cover - optional dependency
        return estimate_tokens_heuristic, False, e
