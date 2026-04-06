from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from .session import Base


class Debate(Base):
    """Table for debates"""

    __tablename__ = "debates"

    id = Column(Integer, primary_key=True, index=True)
    topic = Column(String)

    agents = relationship("Agent", back_populates="debate")
    messages = relationship("Message", back_populates="debate")


class Agent(Base):
    """Table for Agent with persona"""

    __tablename__ = "agents"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    persona = Column(Text)

    debate_id = Column(Integer, ForeignKey("debates.id"))

    debate = relationship("Debate", back_populates="agents")


class Message(Base):
    """Table for storing messages during rounds"""

    __tablename__ = "messages"

    id = Column(Integer, primary_key=True)

    debate_id = Column(Integer, ForeignKey("debates.id"))
    agent_name = Column(String)
    content = Column(Text)  # topic to discuss
    internal_monologue = Column(Text, nullable=True)  # what agent does not want to say
    withheld_info = Column(Text, nullable=True)  # info does not want to share
    subtext = Column(Text, nullable=True)  # agents intent
    timestamp = Column(DateTime, default=lambda: datetime.now())

    debate = relationship("Debate", back_populates="messages")
