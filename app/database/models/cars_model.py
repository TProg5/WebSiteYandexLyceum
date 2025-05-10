from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey

from sqlalchemy import (
    Text,
    Integer,
    Float,
    String,
    UniqueConstraint,
    PrimaryKeyConstraint,
)

from flask_login import UserMixin

from sqlalchemy_serializer import SerializerMixin

from database.sync_engine import Base


class Cars(Base, UserMixin, SerializerMixin): 
    __tablename__ = "cars"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    vin_number: Mapped[str] = mapped_column(String, unique=True)
    year: Mapped[int] = mapped_column(Integer)
    mileage: Mapped[int] = mapped_column(Integer)
    transmission: Mapped[str] = mapped_column(String) 
    engine_size: Mapped[float] = mapped_column(Float)
    driver_type: Mapped[str] = mapped_column(String)
    color: Mapped[str] = mapped_column(String)
    seats: Mapped[int] = mapped_column(Integer)
    doors: Mapped[int] = mapped_column(Integer)
 
    model_id: Mapped[int] = mapped_column(ForeignKey("models.id"), nullable=False)
    model = relationship("Models", back_populates='cars')

    

class Brands(Base, UserMixin):
    __tablename__ = "brands"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    models = relationship("Models", back_populates="brand")


class Models(Base, UserMixin):
    __tablename__ = "models"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    brand_id: Mapped[int] = mapped_column(ForeignKey("brands.id"))

    brand = relationship("Brands", back_populates="models")
    cars = relationship("Cars", back_populates="model")