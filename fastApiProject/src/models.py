from datetime import datetime

from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DECIMAL, DateTime
from sqlalchemy.orm import relationship

from .database import Base


class Dades(Base):
    __tablename__ = "dades"

    id = Column(Integer, primary_key=True)
    prediccio = Column(DECIMAL)

    # items = relationship("Item", back_populates="owner")

class Model(Base):
    __tablename__ = "model"

    id = Column(Integer, primary_key=True, autoincrement=True)
    dia = Column(DateTime, default=datetime.utcnow)

# class Item(Base):
#     __tablename__ = "items"
#
#     id = Column(Integer, primary_key=True)
#     title = Column(String, index=True)
#     description = Column(String, index=True)
#     owner_id = Column(Integer, ForeignKey("users.id"))
#
#     owner = relationship("Dades", back_populates="items")