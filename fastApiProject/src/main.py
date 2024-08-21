import base64
import io
import os
import shutil
import subprocess
from datetime import datetime
from typing import Annotated, List

from posixpath import join

import openpyxl
import pandas as pd
from fastapi import Depends, FastAPI, HTTPException, UploadFile, File, Request, Form
from fastapi.middleware.cors import CORSMiddleware
from rich import status
from sqlalchemy.orm import Session
from sqlalchemy.sql.functions import current_date
from starlette.responses import JSONResponse

from . import crud, models, schemas, training
from .database import SessionLocal, engine
from fastapi.responses import StreamingResponse
from .models import Seleccionat

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

import requests
from fastapi.responses import FileResponse

import pulp


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


origins = ["*"]


@app.get('/api/getPreus')
def get_preus():
    api_url = "https://api.preciodelaluz.org/v1/prices/all?zone=PCB"
    preus = requests.get(api_url).json()
    return preus


@app.post("/api/optimitzacio")
def optimitza(data_model: schemas.InfoPerOptimitzar, response_model=list[any]):
    # Calcular el máximo de litros que se pueden bombear por hora

    # Crear el problema de optimización
    problema = pulp.LpProblem("Minimizar_Costo_Electricidad", pulp.LpMinimize)

    # El preu ens ve donat en euros/MWh
    preuElectricitat = get_preus()
    prepara = list(preuElectricitat.items())

    # Passem el consum entrat a MWh
    data_model.consum = data_model.consum / 1000;
    data_model.bombeig = data_model.bombeig * 60;

    # Variables de decisión
    B = pulp.LpVariable.dicts("Bombeo", range(24), lowBound=0, upBound=data_model.bombeig, cat='Continuous')
    S = pulp.LpVariable.dicts("Almacenamiento", range(24), lowBound=0, upBound=data_model.capacitat, cat='Continuous')

    # Volumen inicial
    S[-1] = 50  # Partirem de 50L inicials

    # Función objetivo
    problema += pulp.lpSum(prepara[t][1]['price'] * B[t] * data_model.consum for t in range(24))

    # Restricciones
    for t in range(24):
        if t == 0:
            problema += S[t] == S[-1] + B[t] - data_model.data_i_consum[t].consum
        else:
            problema += S[t] == S[t - 1] + B[t] - data_model.data_i_consum[t].consum
        problema += S[t] <= data_model.capacitat
        problema += S[t] >= data_model.data_i_consum[t].consum
        problema += B[t] <= data_model.bombeig  # Restricción de bombeo máximo por hora

    # Resolver el problema
    problema.solve()

    # for t in range(24):

    # Resultados
    print("Estado de optimización:", pulp.LpStatus[problema.status])
    print("Costo total de electricidad: $", pulp.value(problema.objective))
    novaLlista = []
    for t in range(24):
        print(f"Hora {t}: Bombeo = {B[t].varValue:.2f} litros, Almacenamiento = {S[t].varValue:.2f} litros")
        entrada = {
            'hora': t,
            'bombeig': B[t].varValue,
            'capacitat': S[t].varValue
        }
        novaLlista.append(entrada)
    return JSONResponse(content={"llista" : novaLlista, "total":round(pulp.value(problema.objective),2)})





@app.post("/api/excel")
async def create_excel(data_model: List[schemas.DataIConsum]):
    # conversio a dataframe de pandas
    data = [item.dict() for item in data_model]
    df = pd.DataFrame(data)

    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Sheet1')

    # Preparem buffer a l'inici del document
    output.seek(0)

    # Retornem l'arxiu gravat sense haver-lo guardat al servidor
    return StreamingResponse(output, media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                             headers={"Content-Disposition": "attachment; filename=data.xlsx"})


@app.get("/api/models/", response_model=list[schemas.Model])
def read_models(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    models = crud.get_models(db, skip=skip, limit=limit)
    return models


@app.get("/api/prediccio/{dies}")
def genera_nova(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), dies=1):
    seleccionat = crud.get_seleccionat(db, skip=skip, limit=limit)
    selec = None
    if len(seleccionat) != 0:
        selec = seleccionat[0]

    horaInicial = 0
    resultat, plt = training.genera_prediccio(str(selec.id), int(dies), horaInicial)

    fig, ax = plt.subplots()
    ax.plot(resultat, marker='o')
    ax.set_title('Consum dels propers ' + dies + ' dies')
    ax.set_xlabel('Temps (h)')
    ax.set_ylabel('Consum (L)')

    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    plt.close(fig)

    plt.show()
    img_str = base64.b64encode(buf.getvalue()).decode('utf-8')

    return JSONResponse(content={"resul": resultat, "plot": f"data:image/png;base64,{img_str}"})


@app.get("/api/seleccionat", response_model=schemas.Seleccionat)
def read_models(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    seleccionat = crud.get_seleccionat(db, skip=skip, limit=limit)
    selec = None
    if len(seleccionat) != 0:
        selec = seleccionat[0]
    return selec


def save_model(db: Session):
    current_date = datetime.now()
    db_model = models.Model(dia=current_date)
    db.add(db_model)
    db.commit()
    db.refresh(db_model)
    return db_model


def save_seleccionat(db: Session, number: int):
    listselec = crud.get_seleccionat(db)
    if (len(listselec) > 0):
        selec = listselec[0]
        db.delete(selec)
        db.commit()
    db_model = models.Seleccionat(id=number)
    db.add(db_model)
    db.commit()
    db.refresh(db_model)
    return db_model


@app.post("/api/seleccionat/{id}")
def selecciona_nou(db: Session = Depends(get_db), id=0, response_model=[schemas.Seleccionat]):
    nouModel = save_seleccionat(db, id)
    return nouModel


@app.post("/api/models/")
def create_model(file: UploadFile = File(...), db: Session = Depends(get_db)):
    if file.filename.endswith('.xlsx'):
        nouModel = save_model(db)
        novaId = nouModel.id
        nouArxiu = guardaArxiu(file, novaId)

        horainici = training.processa_dades(nouArxiu)
        nouModel = db.query(models.Model).filter_by(id=nouModel.id).first()
        nouModel.horainici = horainici
        db.commit()
        db.refresh(nouModel)

    else:
        raise HTTPException(status_code=status.HTTP_405_METHOD_NOT_ALLOWED)


@app.post("/api/files/")
def create_file(file: UploadFile = File(...)):
    print(file)
    return {"file_size": "OK"}


# @app.post("/users/", response_model=schemas.User)
# def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
#     db_user = crud.get_user_by_email(db, email=user.email)
#     if db_user:
#         raise HTTPException(status_code=400, detail="Email already registered")
#     return crud.create_user(db=db, user=user)

# @app.get("/users/{user_id}", response_model=schemas.User)
# def read_user(user_id: int, db: Session = Depends(get_db)):
#     db_user = crud.get_user(db, user_id=user_id)
#     if db_user is None:
#         raise HTTPException(status_code=404, detail="User not found")
#     return db_user
#
#
# @app.post("/users/{user_id}/items/", response_model=schemas.Item)
# def create_item_for_user(
#     user_id: int, item: schemas.ItemCreate, db: Session = Depends(get_db)
# ):
#     return crud.create_user_item(db=db, item=item, user_id=user_id)
#
#
# @app.get("/items/", response_model=list[schemas.Item])
# def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
#     items = crud.get_items(db, skip=skip, limit=limit)
#     return items


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/")
async def root():
    return {"message": "Hello World"}


def guardaArxiu(file, id):
    directoriActual = os.path.dirname(os.path.abspath(__file__))
    idName = str(id)
    save_path = (os.path.join('model', idName + ".xlsx"))
    novaRuta = os.path.join(directoriActual, save_path)

    with open(novaRuta, "wb") as file_object:
        file_object.write(file.file.read())

    # with open(novaRuta, 'wb') as newFile:
    #     for chunk in iter(lambda: file.read(4096), b''):
    #         newFile.write(chunk)
    # shutil.move(file,save_path)
    return idName

    # file.write()


def root():
    return "Hello World";

# @app.get("/api/{name}")
# async def say_hello(name: str):
#     return {"message": f"Hello {name}"}
