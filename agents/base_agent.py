# agents/base_agent.py

"""
BaseAgent module
----------------
This file defines:
1. The Message dataclass (standard communication format)
2. The BaseAgent abstract class (interface every agent must follow)
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Dict, Any, Literal, List


# Step 1️ — Define allowed agent roles
Role = Literal["client", "advisor", "analyst"]


# Step 2️ — Message dataclass
@dataclass
class Message:
    """
    Represents a message passed between agents.
    Acts like a standardized envelope so that every agent
    understands the same structure.
    """
    sender: Role
    receiver: Role
    content: str
    metadata: Dict[str, Any] | None = None

    def __repr__(self):
        return f"Message(from={self.sender}, to={self.receiver}, content={self.content[:40]}...)"

# Step 3️ — Abstract base agent
class BaseAgent(ABC):
    """
    Parent class that defines a common interface for all agents.
    All agents (ClientAgent, AdvisorAgent, AnalystAgent) inherit this.
    """

    def __init__(self, name: str):
        self.name = name  # Each agent will have a unique identifier

    @abstractmethod
    def handle(self, message: Message) -> List[Message]:
        """
        Process an incoming message and return a list of outgoing messages.
        Every agent MUST override this method.
        """
        pass

    # Optional: a helper function for logging or debugging
    def log(self, text: str):
        print(f"[{self.name.upper()} LOG]: {text}")
