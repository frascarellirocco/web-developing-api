from fastapi import FastAPI
from .progetto_db import dbinit

dbinit()

app = FastAPI()

from .progetto_prodotti import router as prodotti_router

app.include_router(prodotti_router)

@app.get("/")
def home():
    return {"info":"Server principale attivo!"}



