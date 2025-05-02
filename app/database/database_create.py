import asyncio
from sync_engine import engine, Base  # Импортируешь свой engine и Base

from models.users_model import Users

def create_all_tables():
    with engine.begin() as conn:
        # Важно: run_sync позволяет использовать синхронные методы внутри асинхронного контекста
        conn.run_sync(Base.metadata.create_all)


if __name__ == "__main__":
    create_all_tables()