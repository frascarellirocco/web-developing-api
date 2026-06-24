from fastapi import FastAPI

# Uso del punto per l'import relativo corretto (Lezione 7, Slide 5)
from .progetto_db import dbinit
from .progetto_prodotti import router as prodotti_router
from .progetto_utente import router as utenti_router
from .progetto_film import router as film_router

# Inizializzazione database all'avvio
dbinit()

app = FastAPI()

# Agganciamo entrambi i router all'applicazione principale (Lezione 7, Slide 5)
app.include_router(prodotti_router)
app.include_router(utenti_router)
app.include_router(film_router)

@app.get("/")
def home():
    return {"info": "Server principale attivo!"}