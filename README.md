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
   .\.venv\Scripts\activate
   pip install -r requirements.txt
