# main.py

"""
Main Orchestrator
-----------------
Controls the entire conversation flow between:
ClientAgent ↔ AdvisorAgent ↔ AnalystAgent
"""

from agents.base_agent import Message
from agents.client_agent import ClientAgent
from agents.advisor_agent import AdvisorAgent
from agents.analyst_agent import AnalystAgent
from services.llm_client import DummyLLM


def run_conversation():
    """
    Simulates a full interaction between client, advisor, and analyst agents.
    The process ends once the client is satisfied.
    """

    # -------------------------------------------------------------------------
    # Step 1️ — Initialize all dependencies
    # -------------------------------------------------------------------------
    llm = DummyLLM()                        # Mock LLM for reasoning
    advisor = AdvisorAgent(llm=llm)         # Orchestrator
    analyst = AnalystAgent()                # Data/research agent

    # Create client profile
    profile = {
        "name": "Kavya",
        "age": 40,
        "risk": "moderate",
        "goal": "retirement",
        "investment_amount": 200000
    }
    client = ClientAgent(profile=profile)   # Simulated user

    # -------------------------------------------------------------------------
    # Step 2️ — Initialize conversation queue
    # -------------------------------------------------------------------------
    queue: list[Message] = []

    # First message originates from Client
    first_msg = Message(
        sender="client",
        receiver="advisor",
        content="I want to invest for retirement.",
        metadata={"client_profile": profile}
    )

    queue.append(first_msg)
    print("\n Conversation started!\n")

    # -------------------------------------------------------------------------
    # Step 3️ — Conversation loop
    # -------------------------------------------------------------------------
    while queue:
        msg = queue.pop(0)  # FIFO queue
        next_messages = []

        # Routing logic based on receiver
        if msg.receiver == "advisor":
            next_messages = advisor.handle(msg)
        elif msg.receiver == "analyst":
            next_messages = analyst.handle(msg)
        elif msg.receiver == "client":
            next_messages = client.handle(msg)
        else:
            print(f" Unknown receiver: {msg.receiver}")

        # Add new messages to the queue
        queue.extend(next_messages)

        # End loop if client is satisfied
        if client.satisfied:
            print("\nConversation resolved. Client is satisfied.\n")
            break


# -------------------------------------------------------------------------
# Step 4️ — Entry point
# -------------------------------------------------------------------------
if __name__ == "__main__":
    run_conversation()
