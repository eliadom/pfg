from pydantic import BaseModel, condecimal
from sqlalchemy import DECIMAL


# for creating or reading data
class DadesBase(BaseModel):
    id: int
    prediccio: condecimal(decimal_places=4)


# inherit from dades base + additional attrib
class DadesCreate(DadesBase):
    pass


# returning from API
class Dades(DadesBase):
    id: int
    prediccio: condecimal(decimal_places=4)

    class Config:
        orm_mode = True