from datetime import datetime
from typing import List

from pydantic import BaseModel, condecimal
from sqlalchemy import DECIMAL


# for creating or reading data
#############################################

class DataIConsum(BaseModel):
    data: str
    consum: int

class DataOptimitzacio(BaseModel):
    bombeig: int
    capacitat: int
    hora: int


class InfoPerOptimitzar(BaseModel):
    data_i_consum: List[DataIConsum]
    capacitat: float
    consum: float
    bombeig: float

class ResultatOptimitzacio(BaseModel):
    hora: int
    bombeig : float
    capacitat: float
    consumit: float


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
    horainici: int

# inherit from dades base + additional attrib
class ModelCreate(ModelBase):
    pass


# returning from API
class Model(ModelBase):
    id: int
    dia: datetime
    horainici: int

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
