from sqlalchemy import insert, select
from sqlalchemy.engine import Result

from app.database.models.users_model import Users

from app.database.sync_engine import sync_session


from flask import Flask
from flask_login import LoginManager

login_manager = LoginManager()


def add_user(
    username: str, 
    email: str, 
    hashed_password: str

) -> int:
    """Функция для добавления нового пользователя в Базу Данных"""

    with sync_session() as session:
        with session.begin():
            result: Result = session.execute(
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
        

def check_email(
    email: str
) -> bool:
    """Функция для проверки на существование `Email` в Базе данных"""
    with sync_session() as session:
        with session.begin():
            result: Result = session.execute(
                select(Users)
                .where(Users.email == email)
            )

            return bool(result.scalar_one_or_none())


def returning_info_to_login(
        email: str
) -> None:
    
    with sync_session() as session:
        with session.begin():
            result = session.execute(
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


def get_user_data(email: str) -> None:
    pass

@login_manager.user_loader
def load_user(user_id):
    with sync_session() as session:
        return session.query(Users).get(user_id)