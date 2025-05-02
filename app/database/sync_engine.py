import os
from typing import Optional

from dotenv import load_dotenv

from sqlalchemy.orm import DeclarativeBase

from sqlalchemy import create_engine, Engine
from sqlalchemy.orm import sessionmaker, Session


load_dotenv()


SYNC_DATABASE_URL: Optional[str] = os.getenv("SYNC_DATABASE_URL")
if SYNC_DATABASE_URL is None:
    raise ValueError("No DATABASE_URL provided in environment variables.")


engine: Engine = create_engine(url=SYNC_DATABASE_URL)
session: sessionmaker[Session] = sessionmaker(bind=engine)

class Base(DeclarativeBase):
    pass