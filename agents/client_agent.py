# agents/client_agent.py

"""
ClientAgent
-----------
Simulates the private banking client.
- Sends an initial investment query.
- Receives messages from the AdvisorAgent.
- Decides when the conversation is resolved.
"""

from typing import Dict, Any, List
from .base_agent import BaseAgent, Message


class ClientAgent(BaseAgent):
    def __init__(self, profile: Dict[str, Any]):
        """
        Initialize a simulated client with a financial profile.
        Example:
            profile = {
                "name": "Kavya",
                "age": 40,
                "risk": "moderate",
                "goal": "retirement",
                "investment_amount": 200000
            }
        """
        super().__init__(name="client")
        self.profile = profile
        self.satisfied = False  # tracks if conversation is complete

    def handle(self, message: Message) -> List[Message]:
        """
        React to incoming messages (from Advisor).
        Returns a list of outgoing Message objects.
        """
        # Only Advisor should talk to Client
        if message.sender != "advisor":
            self.log(f"Ignored message from non-advisor: {message.sender}")
            return []

        # Display the advisor's message for clarity
        print(f"\n[Advisor → Client]: {message.content}\n")

        # Check if Advisor gave a recommendation
        lower = message.content.lower()
        if any(word in lower for word in ["recommend", "allocation", "portfolio", "plan"]):
            self.satisfied = True
            self.log("Client satisfied with the recommendation.")

            # Send polite closure response
            reply = Message(
                sender="client",
                receiver="advisor",
                content="Thank you! This plan works for me.",
                metadata={"status": "resolved", "client_profile": self.profile},
            )
            print(f"[Client → Advisor]: {reply.content}")
            return [reply]

        # If unclear, ask for clarification
        self.log("Client seeking clarification on risk/returns.")
        follow_up = Message(
            sender="client",
            receiver="advisor",
            content="Could you please explain the risk and return trade-off?",
            metadata={"status": "needs_more_info", "client_profile": self.profile},
        )
        print(f"[Client → Advisor]: {follow_up.content}")
        return [follow_up]
