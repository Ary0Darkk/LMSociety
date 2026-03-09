from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from .session import Base


class Debate(Base):
    __tablename__ = "debates"

    id = Column(Integer, primary_key=True, index=True)
    topic = Column(String)

    agents = relationship("Agent", back_populates="debate")
    messages = relationship("Message", back_populates="debate")


class Agent(Base):
    __tablename__ = "agents"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    persona = Column(Text)

    debate_id = Column(Integer, ForeignKey("debates.id"))

    debate = relationship("Debate", back_populates="agents")


class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True)

    debate_id = Column(Integer, ForeignKey("debates.id"))
    agent_name = Column(String)
    content = Column(Text)

    debate = relationship("Debate", back_populates="messages")
