# services/llm_client.py
"""
LLM Client Service
------------------
Provides a common interface for all agents to interact with
a language model (OpenAI GPT, Anthropic Claude, etc.).
The AdvisorAgent uses this to reason and craft natural-language outputs.
"""

import os
from typing import Optional
from openai import OpenAI


class LLMClient:
    """
    Real LLM wrapper using OpenAI's Python SDK.
    Supports both GPT-4.1 and GPT-3.5 (switchable by model name).
    """

    def __init__(self, model: str = "gpt-4o-mini"):
        # Expect the API key to be set as an environment variable
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("  OPENAI_API_KEY not set in environment.")
        self.client = OpenAI(api_key=api_key)
        self.model = model

    # ---------------------------------------------------------------------
    def chat(self, prompt: str, system_prompt: Optional[str] = None) -> str:
        """
        Sends a chat request to the OpenAI API and returns the model's reply.
        """
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0.3,
                max_tokens=400,
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            print(f"[LLMClient ERROR]: {e}")
            return "[LLM_ERROR] Unable to generate response."


# -------------------------------------------------------------------------
# Mock version for offline testing (still useful in CI or no-internet env)
# -------------------------------------------------------------------------
class DummyLLM:
    def chat(self, prompt: str, system_prompt: Optional[str] = None) -> str:
        return f"[MOCK_LLM_RESPONSE] {prompt[:100]}..."
