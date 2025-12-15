from __future__ import annotations

import re
from typing import Callable, Tuple

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

def get_token_counter() -> Tuple[Callable[[str], int], bool, str | None]:
    """Return a token counter, a flag for tiktoken usage, and any load error."""
    try:
        import tiktoken  # type: ignore

        enc = tiktoken.get_encoding("cl100k_base")

        def count(text: str) -> int:
            return len(enc.encode(text))

        return count, True, None
    except ModuleNotFoundError:
        return estimate_tokens_heuristic, False, "tiktoken is not installed"
    except Exception as exc:  # pragma: no cover - defensive fallback
        return estimate_tokens_heuristic, False, f"tiktoken failed to load: {exc}"
