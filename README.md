# Agentic Private Bank — Multi-Agent AI System

## Overview
An AI-powered Private Banking simulation where a **Client**, **Advisor**, and **Analyst** agent collaborate to provide personalized investment recommendations.  
Built with **FastAPI**, **Streamlit**, **FAISS**, and **LLMs (OpenAI/HuggingFace)**.

## Architecture
- **agents/** → Core AI agents (client, advisor, analyst)
- **services/** → Vector search, LLM clients, utilities
- **models/** → Typed data models (ClientProfile, Message)
- **knowledge/** → Domain corpus for RAG retrieval
- **api/** → FastAPI REST backend
- **ui/** → Streamlit chat interface
- **main.py** → Local orchestration entry point

## Tech Stack
- Python 3.12  
- FastAPI + Uvicorn  
- Streamlit  
- HuggingFace Sentence Transformers + FAISS  
- OpenAI API (optional LLM)  
- Modular, Testable, and Extensible Architecture

## How to Run
1. Create virtual environment
```bash
   python -m venv .venv
   source .venv/bin/activate    # (or `.venv\Scripts\activate` on Windows)
 ```
2. Install dependencies:
 
```bash
pip install -r requirements.txt
```

3. Set required environment variables (OPENAI_API_KEY).
Create a .env file
 ```
OPENAI_API_KEY=your-api-key-here
 ```
4. Run the backend API:
 ```
uvicorn api.main:app --reload
 ```
5. Launch the UI:
 ```
streamlit run ui/app.py    # (or whichever file under `ui/`)
 ```

### **Usage / Example Flow** 

1. The Client agent (simulated user) provides a profile: age, risk appetite, investment horizon, preference for “green” / ESG investments etc.

2. The Advisor agent uses the client profile and retrieval from knowledge/ + embeddings to suggest a portfolio strategy (asset classes, allocation, reasoning).

3. The Analyst agent drills down to specific investment recommendations (e.g., ETFs, stocks, bonds) with supporting rationale, referencing retrieved knowledge.

4. The system returns a structured recommendation that the Client can review, ask follow-up questions, get refinements.


### **Directory Structure**
Multi-agent-system/
├── agents/
│   ├── client_agent.py
│   ├── advisor_agent.py
│   └── analyst_agent.py
├── services/
│   ├── vector_service.py
│   ├── llm_service.py
│   ├── prompt_utils.py
│   └── ...
├── models/
│   ├── client_profile.py
│   ├── message.py
│   └── recommendation.py
├── knowledge/
│   └── private_bank_corpus/
│       ├── doc1.txt
│       └── doc2.txt
├── api/
│   ├── main.py
│   ├── routes.py
│   └── schemas.py
├── ui/
│   └── app.py
├── main.py
├── requirements.txt
├── README.md   ← (this file)
└── .gitignore
