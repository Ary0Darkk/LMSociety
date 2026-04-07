# LMSociety — Society of LLMs

A multi-agent LLM debate simulation platform where AI personas with distinct perspectives deliberate on real-world topics — like a parliament of language models.

LMSociety orchestrates multiple LLM agents (Philosopher, Engineer, Government, Citizen) across heterogeneous models (Gemini, DeepSeek, GPT-OSS, MiniMax), enabling structured multi-round debates with persistent memory via ChromaDB vector storage. Each agent reasons through DSPy's `ChainOfThought` prompting within its own model context, producing a sequential pipeline of ethical analysis → technical planning → regulatory review → citizen feedback.

## Architecture

```
┌─────────────┐         REST API          ┌──────────────────┐
│   React 19  │  ◄──────────────────────►  │  FastAPI Server  │
│   (Vite)    │                            │                  │
└─────────────┘                            │  ┌────────────┐  │
                                           │  │ DSPy Agent │  │
┌─────────────┐                            │  │  Pipeline   │  │
│  Streamlit  │  ◄──────────────────────►  │  └─────┬──────┘  │
│     App     │                            │        │         │
└─────────────┘                            │  ┌─────▼──────┐  │
                                           │  │  ChromaDB   │  │
┌─────────────┐                            │  │  (Memory)   │  │
│  Click CLI  │  ◄──────────────────────►  │  └─────┬──────┘  │
└─────────────┘                            │  ┌─────▼──────┐  │
                                           │  │  SQLAlchemy │  │
                                           │  │  (SQLite)   │  │
                                           │  └────────────┘  │
                                           └──────────────────┘
```

### Agent Pipeline

```
Proposal
   │
   ▼
┌──────────────┐    ┌──────────────┐    ┌──────────────┐    ┌──────────────┐
│  Philosopher │ ─► │   Engineer   │ ─► │  Government  │ ─► │   Citizen    │
│  (DeepSeek)  │    │  (Gemini)    │    │  (GPT-OSS)   │    │  (MiniMax)   │
│              │    │              │    │              │    │              │
│ Ethics       │    │ Technical    │    │ Regulatory   │    │ Public       │
│ Framework    │    │ Plan         │    │ Verdict      │    │ Feedback     │
└──────────────┘    └──────────────┘    └──────────────┘    └──────────────┘
```

## Tech Stack

| Layer | Technology |
|-------|------------|
| LLM Orchestration | **DSPy** (ChainOfThought, Signatures, Modules) |
| Backend | **FastAPI** + **Uvicorn** |
| Database | **SQLAlchemy** + **SQLite** |
| Vector Store | **ChromaDB** (debate memory & context retrieval) |
| Frontend | **React 19** + **Vite** / **Streamlit** |
| CLI | **Click-Shell** + **Rich** + **Typer** |
| LLM Providers | Google Gemini, DeepSeek, GPT-OSS, MiniMax (via HuggingFace Router) |
| Package Manager | **uv** (Python 3.13+) |

## Project Structure

```
LMSociety/
├── src/
│   ├── backend/
│   │   ├── agents/
│   │   │   ├── debate_engine.py    # Orchestrates agent responses per round
│   │   │   ├── dspy_agents.py      # DSPy DebateAgent module & signature
│   │   │   └── llm_call.py         # Legacy LangChain-based calls
│   │   ├── db/
│   │   │   ├── models.py           # SQLAlchemy models (Debate, Agent, Message)
│   │   │   └── session.py          # Database session factory
│   │   ├── llm/
│   │   │   └── models.py           # LLM registry (Gemini, DeepSeek, GPT-OSS, MiniMax)
│   │   ├── society/
│   │   │   └── lmsociety.py        # Core 4-agent pipeline (SocietyOfFour)
│   │   ├── vector_store/
│   │   │   └── chroma_store.py     # ChromaDB store & retrieval
│   │   └── main.py                 # FastAPI app with debate endpoints
│   ├── frontend/
│   │   ├── react/                  # React 19 + Vite frontend
│   │   └── streamlit/              # Streamlit alternative frontend
│   └── shared/
│       └── shared_schemas.py       # Pydantic schemas (DebateCreate, AgentSchema)
├── cli/                            # Click-shell CLI interface
├── pyproject.toml
└── knowledge.md
```

## Getting Started

### Prerequisites

- Python 3.13+
- [uv](https://docs.astral.sh/uv/) package manager
- Node.js 18+ (for React frontend)

### Installation

```bash
# Clone the repository
git clone https://github.com/your-username/LMSociety.git
cd LMSociety

# Install Python dependencies
uv sync

# Install frontend dependencies
cd src/frontend/react
npm install
cd ../../..
```

### Environment Variables

Create a `.env` file in the project root:

```env
GOOGLE_API_KEY=your_google_api_key     # For Gemini models
HF_TOKEN=your_huggingface_token         # For HuggingFace-hosted models (DeepSeek, GPT-OSS, MiniMax)
```

### Running the App

```bash
# Start the backend server
uvicorn main:app --reload

# Start the React frontend (in a separate terminal)
cd src/frontend/react
npm run dev
```

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/debate/start` | Create a new debate with a topic, agents, and model selection |
| `POST` | `/debate/{id}/round` | Run a full round — all agents respond sequentially |
| `POST` | `/debate/{id}/speak` | Trigger a single agent's response |
| `GET`  | `/debate/{id}` | Retrieve all messages for a debate |

### Example: Start a Debate

```bash
curl -X POST http://localhost:8000/debate/start \
  -H "Content-Type: application/json" \
  -d '{
    "topic": "Should AI control city traffic lights?",
    "agents": [
      {"name": "Philosopher", "persona": "A deep thinker focused on ethics and social dynamics"},
      {"name": "Engineer", "persona": "A pragmatic builder focused on technical feasibility"},
      {"name": "Government", "persona": "A regulator focused on public safety and policy"},
      {"name": "Citizen", "persona": "An everyday person concerned with practical impact"}
    ],
    "model": "Gemini"
  }'
```