from pydantic import BaseModel
from typing import List


class AgentSchema(BaseModel):
    name: str
    persona: str


class DebateCreate(BaseModel):
    topic: str
    agents: List[AgentSchema]
    model: str
