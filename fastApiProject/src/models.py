from datetime import datetime

from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DECIMAL, DateTime
from sqlalchemy.orm import relationship

from .database import Base


class Model(Base):
    __tablename__ = "model"

    id = Column(Integer, primary_key=True, autoincrement=True)
    dia = Column(DateTime, default=datetime.utcnow)
    horainici = Column(Integer, default=0)

class Seleccionat(Base):
    __tablename__ = "seleccionat"

    id = Column(Integer, primary_key=True)

# class Item(Base):
#     __tablename__ = "items"
#
#     id = Column(Integer, primary_key=True)
#     title = Column(String, index=True)
#     description = Column(String, index=True)
#     owner_id = Column(Integer, ForeignKey("users.id"))
#
#     owner = relationship("Dades", back_populates="items")