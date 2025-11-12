# api/server.py
"""
FastAPI layer for the Agentic Private Bank multi-agent system.
Endpoints:
  - /simulate : run a full client–advisor–analyst conversation.
  - /recommend : run a single query with a custom client profile.
"""

from fastapi import FastAPI
from pydantic import BaseModel
from agents.client_agent import ClientAgent
from agents.advisor_agent import AdvisorAgent
from agents.analyst_agent import AnalystAgent
from models.client_profile import ClientProfile
from models.message import Message
from services.llm_client import DummyLLM

app = FastAPI(title="Agentic Private Bank API", version="1.0")

# ---------- Data Models ----------

class ConversationResult(BaseModel):
    transcript: list[str]
    status: str

class RecommendRequest(BaseModel):
    name: str
    age: int
    risk: str
    goal: str
    investment_amount: float
    query: str

# ---------- Helper ----------

def run_simulation(profile: ClientProfile, query: str = "I want to invest for retirement.") -> ConversationResult:
    llm = DummyLLM()
    advisor = AdvisorAgent(llm=llm)
    analyst = AnalystAgent()
    client = ClientAgent(profile=profile)

    transcript: list[str] = []
    queue = [Message(sender="client", receiver="advisor", content=query, metadata={"client_profile": profile.__dict__})]

    while queue:
        msg = queue.pop(0)
        transcript.append(f"{msg.sender} → {msg.receiver}: {msg.content}")

        if msg.receiver == "advisor":
            new_msgs = advisor.handle(msg)
        elif msg.receiver == "analyst":
            new_msgs = analyst.handle(msg)
        elif msg.receiver == "client":
            new_msgs = client.handle(msg)
        else:
            new_msgs = []

        queue.extend(new_msgs)

        if client.satisfied:
            transcript.append(" Client satisfied. Conversation complete.")
            break

    return ConversationResult(transcript=transcript, status="resolved" if client.satisfied else "pending")

# ---------- Routes ----------

@app.get("/")
def root():
    return {"message": "Agentic Private Bank API is running."}

@app.post("/simulate", response_model=ConversationResult)
def simulate():
    """Run default simulation with preset client profile."""
    profile = ClientProfile(name="Kavya", age=40, risk="moderate", goal="retirement", investment_amount=200000)
    result = run_simulation(profile)
    return result

@app.post("/recommend", response_model=ConversationResult)
def recommend(req: RecommendRequest):
    """Run simulation using custom client profile & query."""
    profile = ClientProfile(
        name=req.name,
        age=req.age,
        risk=req.risk,
        goal=req.goal,
        investment_amount=req.investment_amount,
    )
    result = run_simulation(profile, query=req.query)
    return result
