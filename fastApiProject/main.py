from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# @app.get("/api/")
# async def root():
#     return {"message": "Hello World"}

@app.get("/api/")
async def root():
    return "Hello World";

@app.get("/api/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}
