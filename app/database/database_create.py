import asyncio
from engine import engine, Base  # Импортируешь свой engine и Base

from models.users_model import Users

async def create_all_tables():
    async with engine.begin() as conn:
        # Важно: run_sync позволяет использовать синхронные методы внутри асинхронного контекста
        await conn.run_sync(Base.metadata.create_all)


if __name__ == "__main__":
    asyncio.run(create_all_tables())