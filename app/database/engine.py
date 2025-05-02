import os

from typing import Optional
from dotenv import load_dotenv

from sqlalchemy.orm import DeclarativeBase

from sqlalchemy.ext.asyncio import (
    create_async_engine, AsyncAttrs,
    async_sessionmaker, AsyncSession,
    AsyncEngine
)
     
load_dotenv()

DATABASE_URL: Optional[str] = os.getenv("DATABASE_URL")
if DATABASE_URL is None:
    raise ValueError("No DATABASE_URL provided in environment variables.")


engine: AsyncEngine = create_async_engine(url=DATABASE_URL)
async_session: async_sessionmaker[AsyncSession] = async_sessionmaker(bind=engine)

class Base(AsyncAttrs, DeclarativeBase):
    pass