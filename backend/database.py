"""
database.py

Database connection and session management for NeonDB (Postgres).

Set DATABASE_URL in a .env file at the project root, e.g.:

    DATABASE_URL=postgresql+psycopg2://user:password@ep-xxxx.neon.tech/neondb?sslmode=require

Author: Raman Tiwari
Project: SAP AI Test Agent
"""

import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

load_dotenv()

DATABASE_URL = os.environ.get("DATABASE_URL")

if not DATABASE_URL:
    raise RuntimeError(
        "DATABASE_URL is not set. Create a .env file with your "
        "NeonDB connection string (see database.py docstring)."
    )

engine = create_engine(DATABASE_URL, pool_pre_ping=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    pass


def get_db():
    """
    FastAPI dependency — yields a DB session per request.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
