# models/client_profile.py

from dataclasses import dataclass


@dataclass
class ClientProfile:
    """
    Structured representation of a client's financial profile.
    """
    name: str
    age: int
    risk: str            # e.g. "low", "moderate", "high"
    goal: str            # e.g. "retirement", "education"
    investment_amount: float
