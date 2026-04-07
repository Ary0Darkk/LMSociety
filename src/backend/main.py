from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from opentelemetry import trace
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor

from sqlalchemy.orm import Session

from backend.db.session import SessionLocal, engine
from backend.db.models import Base, Debate, Agent, Message
from backend.agents.debate_engine import generate_agent_response
from backend.observability.tracing import setup_phoenix, instrument_all

from shared.shared_schemas import DebateCreate

import dspy
from backend.llm.models import LLM_REGISTRY

# observability setup
setup_phoenix()
instrument_all()

Base.metadata.create_all(bind=engine)


# fastapi
app = FastAPI()

FastAPIInstrumentor.instrument_app(app)

tracer = trace.get_tracer("lmsociety")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/debate/start")
def start_debate(data: DebateCreate):
    selected_model = LLM_REGISTRY[data.model]

    dspy.settings.configure(lm=selected_model)

    db: Session = SessionLocal()

    debate = Debate(topic=data.topic)

    db.add(debate)
    db.commit()
    db.refresh(debate)

    for a in data.agents:
        agent = Agent(name=a.name, persona=a.persona, debate_id=debate.id)

        db.add(agent)

    db.commit()

    return {"debate_id": debate.id}


@app.post("/debate/{debate_id}/round")
def run_round(debate_id: int):
    db: Session = SessionLocal()

    debate = db.query(Debate).filter(Debate.id == debate_id).first()

    # Get previous messages for context
    previous_messages = (
        db.query(Message)
        .filter(Message.debate_id == debate_id)
        .order_by(Message.timestamp)
        .all()
    )
    history = [{"agent": m.agent_name, "content": m.content} for m in previous_messages]

    responses = []

    agent_names = [a.name for a in debate.agents]

    for i, agent in enumerate(debate.agents):
        target_agent = agent_names[i + 1] if i + 1 < len(agent_names) else None

        result = generate_agent_response(
            {"name": agent.name, "persona": agent.persona},
            debate.topic,
            history=history,
            target_agent=target_agent,
        )

        message = Message(
            debate_id=debate.id,
            agent_name=agent.name,
            content=result["verbal_response"],
            internal_monologue=result["internal_monologue"],
            withheld_info=result["withheld_info"],
            subtext=result["subtext"],
        )

        db.add(message)

        # Add to history for next agent in same round
        history.append({"agent": agent.name, "content": result["verbal_response"]})

        responses.append(result)

    db.commit()

    return {"messages": responses}


@app.get("/debate/{debate_id}")
def get_messages(debate_id: int):
    db: Session = SessionLocal()

    msgs = db.query(Message).filter(Message.debate_id == debate_id).all()

    return [
        {
            "id": m.id,
            "agent_name": m.agent_name,
            "content": m.content,
            "internal_monologue": m.internal_monologue,
            "withheld_info": m.withheld_info,
            "subtext": m.subtext,
            "timestamp": m.timestamp.isoformat() if m.timestamp else None,
        }
        for m in msgs
    ]


@app.get("/debate/{debate_id}/agents")
def get_debate_agents(debate_id: int):
    db: Session = SessionLocal()

    debate = db.query(Debate).filter(Debate.id == debate_id).first()

    if not debate:
        return []

    return [{"name": a.name, "persona": a.persona} for a in debate.agents]


@app.post("/debate/{debate_id}/speak")
def agent_turn(debate_id: int, data: dict):
    agent_name = data["agent"]
    user_prompt = data.get("prompt")

    db: Session = SessionLocal()

    debate = db.query(Debate).filter(Debate.id == debate_id).first()

    agent = next((a for a in debate.agents if a.name == agent_name), None)

    if not agent:
        return {"error": "Agent not found"}

    if user_prompt:
        user_message = Message(
            debate_id=debate.id, agent_name=f"user:{agent_name}", content=user_prompt
        )
        db.add(user_message)
        db.commit()

    # Get previous messages for context
    previous_messages = (
        db.query(Message)
        .filter(Message.debate_id == debate_id)
        .order_by(Message.timestamp)
        .all()
    )
    history = [{"agent": m.agent_name, "content": m.content} for m in previous_messages]

    result = generate_agent_response(
        {"name": agent.name, "persona": agent.persona},
        debate.topic,
        history=history,
        user_prompt=user_prompt,
    )

    message = Message(
        debate_id=debate.id,
        agent_name=agent.name,
        content=result["verbal_response"],
        internal_monologue=result["internal_monologue"],
        withheld_info=result["withheld_info"],
        subtext=result["subtext"],
    )

    db.add(message)
    db.commit()

    return {
        "message": result["verbal_response"],
        "internal_monologue": result["internal_monologue"],
        "withheld_info": result["withheld_info"],
        "subtext": result["subtext"],
    }
