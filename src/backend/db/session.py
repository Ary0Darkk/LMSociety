from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os
from dotenv import load_dotenv

load_dotenv()

# Using NeonDB for storing data - free tier
NEON_DB_URL = os.getenv("NEON_DB_CONNECTION_STRING")

if NEON_DB_URL:
    engine = create_engine(NEON_DB_URL, pool_pre_ping=True, pool_size=5)
else:
    DATABASE_URL = "sqlite:///./debate.db"
    engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
