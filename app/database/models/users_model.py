from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import (
    Text,
    Integer,
    String,
    UniqueConstraint,
    PrimaryKeyConstraint,
)

from flask_login import UserMixin

from database.engine import Base


class Users(Base, UserMixin): 
    __tablename__ = "users"
    __table_args__ = (
        PrimaryKeyConstraint(
            "id",
            name='primary_id_const'
        ),
        UniqueConstraint(
            'email', 
            name='unique_email_const'
        )
    )

    id: Mapped[int] = mapped_column(Integer)
    username: Mapped[str] = mapped_column(String, nullable=True)
    email: Mapped[str] = mapped_column(String(33), nullable=True)
    hashed_password: Mapped[str] = mapped_column(Text, nullable=True)
    created_date: Mapped[datetime] = mapped_column(default=datetime.utcnow)


