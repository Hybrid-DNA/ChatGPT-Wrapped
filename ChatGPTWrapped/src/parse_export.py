from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict, Iterable, List, Union

from dateutil import tz


@dataclass(frozen=True)
class ParsedMessage:
    conversation_id: str
    conversation_title: str
    message_id: str
    role: str
    created_at: datetime
    text: str


def _safe_text_from_message(message: Dict[str, Any]) -> str:
    """Extract message text from a ChatGPT export node (handles common variants)."""
    content = message.get("content") or {}
    parts = content.get("parts")

    if isinstance(parts, list):
        out: List[str] = []
        for p in parts:
            if isinstance(p, str):
                out.append(p)
            elif isinstance(p, dict):
                txt = p.get("text") if isinstance(p.get("text"), str) else ""
                if txt:
                    out.append(txt)
        return "\n".join([s for s in out if s]).strip()

    if isinstance(content, dict):
        for key in ("text", "value"):
            v = content.get(key)
            if isinstance(v, str) and v.strip():
                return v.strip()

    return ""


def _iter_messages_from_conversation(conv: Dict[str, Any], timezone: str) -> Iterable[ParsedMessage]:
    conv_id = str(conv.get("id") or "")
    title = str(conv.get("title") or "(untitled)")
    mapping = conv.get("mapping") or {}

    tzinfo = tz.gettz(timezone)

    for node in mapping.values():
        msg = node.get("message")
        if not msg:
            continue

        author = msg.get("author") or {}
        role = str(author.get("role") or "unknown")

        text = _safe_text_from_message(msg)
        if not text:
            continue

        ct = msg.get("create_time")
        if not isinstance(ct, (int, float)):
            continue

        created_at = datetime.fromtimestamp(ct, tz=tzinfo)
        msg_id = str(msg.get("id") or "")

        yield ParsedMessage(
            conversation_id=conv_id,
            conversation_title=title,
            message_id=msg_id,
            role=role,
            created_at=created_at,
            text=text,
        )


def parse_conversations(conversations_json: Union[List[Dict[str, Any]], Dict[str, Any]],
                        timezone: str = "Australia/Melbourne") -> List[ParsedMessage]:
    """Parse conversations.json content into a list of ParsedMessage."""
    if isinstance(conversations_json, dict) and "conversations" in conversations_json:
        conversations = conversations_json["conversations"]
    else:
        conversations = conversations_json

    if not isinstance(conversations, list):
        raise ValueError("Unexpected conversations.json format: expected a list of conversations.")

    out: List[ParsedMessage] = []
    for conv in conversations:
        if isinstance(conv, dict):
            out.extend(list(_iter_messages_from_conversation(conv, timezone=timezone)))
    return out
