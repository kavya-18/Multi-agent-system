# agents/advisor_agent.py

import json
from typing import List
from .base_agent import BaseAgent, Message
from services.llm_client import LLMClient
from prompts.advisor_prompts import (
    ADVISOR_SYSTEM_PROMPT,
    CLIENT_TO_ADVISOR_PROMPT,
    ANALYST_TO_ADVISOR_PROMPT,
)


class AdvisorAgent(BaseAgent):
    def __init__(self, llm: LLMClient):
        super().__init__(name="advisor")
        self.llm = llm
        self.waiting_for_analysis = False
        self.last_client_profile = {}

    # ---------------------------------------------------------------
    def handle(self, message: Message) -> List[Message]:
        if message.sender == "client":
            return self._handle_client_message(message)
        elif message.sender == "analyst":
            return self._handle_analyst_message(message)
        else:
            self.log(f"Unknown sender: {message.sender}")
            return []

    # ---------------------------------------------------------------
    def _handle_client_message(self, message: Message) -> List[Message]:
        profile = message.metadata.get("client_profile", {})
        self.last_client_profile = profile
        risk = profile.get("risk", "moderate")
        goal = profile.get("goal", "general")

        # Build user prompt for LLM
        user_prompt = CLIENT_TO_ADVISOR_PROMPT.format(
            goal=goal, risk=risk, message=message.content
        )

        # Call LLM
        raw_output = self.llm.chat(user_prompt, system_prompt=ADVISOR_SYSTEM_PROMPT)
        self.log(f"LLM raw output: {raw_output}")

        # Parse JSON safely
        try:
            parsed = json.loads(raw_output)
        except json.JSONDecodeError:
            self.log(" JSON parsing failed — returning fallback message.")
            parsed = {"tasks_for_analyst": ["Find moderate risk ETFs"], "recommendation": "pending"}

        tasks = parsed.get("tasks_for_analyst", [])
        msg_to_analyst = Message(
            sender="advisor",
            receiver="analyst",
            content="; ".join(tasks),
            metadata={"client_profile": profile},
        )

        print(f"[Advisor → Analyst]: {msg_to_analyst.content}")
        return [msg_to_analyst]

    # ---------------------------------------------------------------
    def _handle_analyst_message(self, message: Message) -> List[Message]:
        results = message.metadata.get("results", [])
        analyst_json = json.dumps(results, indent=2)

        risk = self.last_client_profile.get("risk", "moderate")
        goal = self.last_client_profile.get("goal", "general")

        user_prompt = ANALYST_TO_ADVISOR_PROMPT.format(
            analyst_data=analyst_json, goal=goal, risk=risk
        )

        raw_output = self.llm.chat(user_prompt, system_prompt=ADVISOR_SYSTEM_PROMPT)
        self.log(f"LLM raw output: {raw_output}")

        try:
            parsed = json.loads(raw_output)
        except json.JSONDecodeError:
            self.log(" JSON parse error — using fallback recommendation.")
            parsed = {"recommendation": "VTI and AGG", "summary": "Balanced portfolio suggestion."}

        msg_to_client = Message(
            sender="advisor",
            receiver="client",
            content=f"Recommendation: {parsed['recommendation']}\nSummary: {parsed['summary']}",
            metadata={"status": "recommendation"},
        )

        print(f"[Advisor → Client]: {msg_to_client.content}")
        return [msg_to_client]
