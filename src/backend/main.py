from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from sqlalchemy.orm import Session

from backend.db.session import SessionLocal, engine
from backend.db.models import Base, Debate, Agent, Message
from backend.agents.debate_engine import generate_agent_response

from shared.shared_schemas import DebateCreate

import dspy
from backend.llm.models import LLM_REGISTRY

Base.metadata.create_all(bind=engine)

app = FastAPI()
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

    responses = []

    for agent in debate.agents:
        msg = generate_agent_response({"name": agent.name}, debate.topic)

        message = Message(debate_id=debate.id, agent_name=agent.name, content=msg)

        db.add(message)

        responses.append(msg)

    db.commit()

    return {"messages": responses}


@app.get("/debate/{debate_id}")
def get_messages(debate_id: int):
    db: Session = SessionLocal()

    msgs = db.query(Message).filter(Message.debate_id == debate_id).all()

    return msgs


@app.post("/debate/{debate_id}/speak")
def agent_turn(debate_id: int, data: dict):
    agent_name = data["agent"]

    db: Session = SessionLocal()

    debate = db.query(Debate).filter(Debate.id == debate_id).first()

    agent = next(a for a in debate.agents if a.name == agent_name)

    msg = generate_agent_response(
        {"name": agent.name, "persona": agent.persona}, debate.topic
    )

    message = Message(debate_id=debate.id, agent_name=agent.name, content=msg)

    db.add(message)
    db.commit()

    return {"message": msg}
