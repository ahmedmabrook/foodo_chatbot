"""Pure domain entities. Zero external imports — only stdlib."""
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Optional
from uuid import uuid4


@dataclass
class Message:
    role: str  # "user" | "assistant"
    content: str
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


@dataclass
class Conversation:
    id: str = field(default_factory=lambda: str(uuid4()))
    session_id: str = ""
    messages: list[Message] = field(default_factory=list)
    metadata: dict = field(default_factory=dict)

    def add_message(self, role: str, content: str) -> Message:
        msg = Message(role=role, content=content)
        self.messages.append(msg)
        return msg

    def last_user_message(self) -> Optional[Message]:
        for m in reversed(self.messages):
            if m.role == "user":
                return m
        return None
