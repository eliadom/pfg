from datetime import datetime

from pydantic import BaseModel, condecimal
from sqlalchemy import DECIMAL


# for creating or reading data
#############################################

class DataIConsum(BaseModel):
    data : datetime
    consum : int

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
        from_attributes = True


#############################################
class ModelBase(BaseModel):
    id: int
    dia: datetime


# inherit from dades base + additional attrib
class ModelCreate(ModelBase):
    pass


# returning from API
class Model(ModelBase):
    id: int
    dia: datetime

    class Config:
        from_attributes = True

#############################################
class SeleccionatBase(BaseModel):
    id: int


# inherit from dades base + additional attrib
class SeleccionatCreate(SeleccionatBase):
    pass


# returning from API
class Seleccionat(SeleccionatBase):
    id: int

    class Config:
        from_attributes = True