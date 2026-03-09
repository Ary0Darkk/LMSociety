# LMSociety — Project Knowledge

## What This Is
A simulation of an LLM "society" where multiple LLM agents (with different personas) debate and interact like humans. Built with a Python backend (FastAPI + DSPy) and a React frontend.

## Architecture
- **`main.py`** — FastAPI WebSocket server (currently uses mock data, not connected to real DSPy pipeline)
- **`backend/src/society/lmsociety.py`** — Core DSPy society logic: linear pipeline of 4 agents (Philosopher → Engineer → Government → Citizen)
- **`backend/src/agents/models.py`** — DSPy agent/signature definitions
- **`backend/src/agents/llm_call.py`** — Legacy LangChain-based LLM calls (superseded by DSPy)
- **`frontend/`** — React + Vite + TypeScript + Tailwind CSS + shadcn/ui — shows agent cards and messages via WebSocket
- **`cli/`** — Click-shell CLI (placeholder, not yet functional)

## Commands

### Backend
```bash
# Install dependencies (uses uv)
uv sync

# Run FastAPI server
uvicorn main:app --reload
```

### Frontend
```bash
cd frontend
npm install
npm run dev      # Dev server (Vite)
npm run build    # Typecheck + build
npm run lint     # ESLint
```

## Key Tech Stack
- **Python 3.13+**, managed with **uv**
- **DSPy** for LLM orchestration (primary)
- **FastAPI** + **uvicorn** for WebSocket server
- **React 19** + **Vite 7** + **TypeScript** + **Tailwind CSS 3.4** + **shadcn/ui** (Radix primitives)
- **LangChain** (legacy, in `llm_call.py`)

## Environment Variables
- `GOOGLE_API_KEY` — for Gemini models
- `HF_TOKEN` — for HuggingFace models

## Conventions & Gotchas
- `pyproject.toml` project name is still `"rizzler"` — should be updated to `"lmsociety"`
- The FastAPI WebSocket server (`main.py`) and the DSPy society (`lmsociety.py`) are **not yet connected** — the server sends mock/placeholder messages
- Agent names differ between server (Philosopher, Scientist, Economist) and DSPy pipeline (Philosopher, Engineer, Government, Citizen)
- CLI entry point in `pyproject.toml` is commented out
- Frontend connects to WebSocket at `ws://localhost:8000/ws/society`
