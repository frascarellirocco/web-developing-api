from fastapi import FastAPI

# Uso del punto per l'import relativo corretto (Lezione 7, Slide 5)
from .progetto_db import dbinit
from .progetto_prodotti import router as prodotti_router
from .progetto_utente import router as utenti_router
from .progetto_film import router as film_router
from fastapi.middleware.cors import CORSMiddleware

# Inizializzazione database all'avvio
dbinit()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],          # Permette l'accesso da qualsiasi sito (Origin)
    allow_credentials=True,
    allow_methods=["*"],          # Permette tutti i metodi (GET, POST, PUT, DELETE, ecc.)
    allow_headers=["*"],          # Permette tutte le intestazioni (Headers)
)

# Agganciamo entrambi i router all'applicazione principale (Lezione 7, Slide 5)
app.include_router(prodotti_router)
app.include_router(utenti_router)
app.include_router(film_router)

@app.get("/")
def home():
    return {"info": "Server principale attivo!"}