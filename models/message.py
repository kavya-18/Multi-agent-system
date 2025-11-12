# models/message.py

from dataclasses import dataclass
from typing import Dict, Any, Literal

Role = Literal["client", "advisor", "analyst"]


@dataclass
class Message:
    """
    Standard envelope passed between agents.
    """
    sender: Role
    receiver: Role
    content: str
    metadata: Dict[str, Any] | None = None

    def __repr__(self) -> str:
        preview = (self.content[:37] + "...") if len(self.content) > 40 else self.content
        return f"Message(from={self.sender}, to={self.receiver}, content={preview})"
