# agents/analyst_agent.py

"""
AnalystAgent (RAG-enabled)
--------------------------
Acts as the research arm of the Private Bank.
Uses VectorStore (FAISS + SentenceTransformer) for semantic retrieval.
- Receives research tasks from AdvisorAgent.
- Searches semantic index for relevant investment instruments.
- Returns factual results in structured format.
"""

from typing import List
from agents.base_agent import BaseAgent
from models.message import Message
from services.vector_store import VectorStore
from services.tools import log_event, timeit


class AnalystAgent(BaseAgent):
    def __init__(self, knowledge_path: str = "knowledge/corpus.json"):
        super().__init__(name="analyst")
        log_event("AnalystAgent", "Initializing RAG-based analyst agent...")
        self.vector_store = VectorStore(knowledge_path)

    # ----------------------------------------------------------
    @timeit
    def handle(self, message: Message) -> List[Message]:
        """
        Process incoming messages from AdvisorAgent.
        Search VectorStore for relevant results and return them.
        """
        if message.sender != "advisor":
            log_event("AnalystAgent", f"Ignored message from non-advisor: {message.sender}")
            return []

        client_profile = message.metadata.get("client_profile", {})
        risk = client_profile.get("risk", "moderate")
        goal = client_profile.get("goal", "general")
        query_text = message.content.lower()

        log_event("AnalystAgent", f"Received research query: '{query_text}' for goal={goal}, risk={risk}")

        # Step 1️ - Semantic search
        results = self.vector_store.search(
            f"{risk} risk investment options for {goal}",
            top_k=3
        )

        # Step 2️ - Handle empty result fallback
        if not results:
            log_event("AnalystAgent", "⚠️ No relevant results found. Returning fallback instruments.")
            results = self.vector_store.corpus[:2]

        # Step 3️ - Create human-readable summary
        summary = ", ".join([r["name"] for r in results])
        response_text = f"I found suitable instruments for {risk} investors aiming for {goal}: {summary}."

        # Step 4️ - Build response message
        msg_back = Message(
            sender="analyst",
            receiver="advisor",
            content=response_text,
            metadata={"results": results, "status": "analysis_done"},
        )

        log_event("AnalystAgent", f"Returning analysis results: {summary}")
        return [msg_back]
