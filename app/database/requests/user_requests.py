from sqlalchemy import insert, select
from sqlalchemy.engine import Result

from database.models.users_model import Users

from database.engine import async_session


from flask import Flask
from flask_login import LoginManager

from utils.password_utils import check_password

login_manager = LoginManager()



async def add_user(
    username: str, 
    email: str, 
    hashed_password: str

) -> int:
    """Функция для добавления нового пользователя в Базу Данных"""

    async with async_session() as session:
        async with session.begin():
            result: Result = await session.execute(
                insert(Users)
                .values(
                    username=username,
                    email=email,
                    hashed_password=hashed_password
                )
                .returning(Users.id)
                )
            
            new_id: int = result.scalar_one()

            return new_id
        

async def check_email(
    email: str
) -> bool:
    """Функция для проверки на существование `Email` в Базе данных"""
    async with async_session() as session:
        async with session.begin():
            result: Result = await session.execute(
                select(Users)
                .where(Users.email == email)
            )

            return bool(result.scalar_one_or_none())


async def returning_info_to_login(
        email: str
) -> None:
    
    async with async_session() as session:
        async with session.begin():
            result = await session.execute(
                select(Users)
                .where(Users.email == email)
            )

            user = result.scalar_one_or_none()

            if user:
                detached_user = Users(
                    id=user.id,
                    username=user.username,
                    email=user.email,
                    hashed_password=user.hashed_password,
                    created_date=user.created_date
                )
                return detached_user
            
            return None


async def get_user_data(email: str) -> None:
    pass

@login_manager.user_loader
async def login_user(user_id: int) -> None:
    pass