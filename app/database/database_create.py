import asyncio
from sync_engine import engine, Base

from models.users_model import Users
from models.cars_model import Brands, Models, Cars

def create_all_tables():
    with engine.begin() as conn:
        Base.metadata.create_all(bind=engine)


if __name__ == "__main__":
    create_all_tables()