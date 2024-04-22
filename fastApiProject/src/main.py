import io
from typing import Annotated

import openpyxl
from fastapi import Depends, FastAPI, HTTPException, UploadFile, File, Request, Form
from fastapi.middleware.cors import CORSMiddleware
from rich import status
from sqlalchemy.orm import Session


from . import crud, models, schemas, training
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


origins = ["*"]


@app.get("/api/dades/", response_model=list[schemas.Dades])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    dades = crud.get_dades(db, skip=skip, limit=limit)
    return dades


@app.post("/api/models/")
def create_model(file: UploadFile = File(...)):
    print(file)
    if file.filename.endswith('.xlsx'):
        training.processa_dades(file)
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
allow_origins = origins,
allow_credentials = True,
allow_methods = ["*"],
allow_headers = ["*"],
)

@app.get("/api/")
async def root():
    return {"message": "Hello World"}



def root():
    return "Hello World";

# @app.get("/api/{name}")
# async def say_hello(name: str):
#     return {"message": f"Hello {name}"}
