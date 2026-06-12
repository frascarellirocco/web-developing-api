from fastapi import FastAPI, HTTPException
import sqlite3
from pydantic import BaseModel
class ProdottoIn(BaseModel):
    nome: str
    prezzo: float


app=FastAPI()

@app.get("/")
def root():
    return{"messaggio": "funziona"}



@app.get("/prodotti")
def ottieni_prodotti():
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row # Conversione attiva!
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM prodotti")
    risultato = cursor.fetchall()
    conn.close()
    return risultato

@app.get("/prodotti/ricerca")
def cerca_prodotto(keyword: str):
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM prodotti WHERE nome LIKE ?",
        (f"%{keyword}%",)
    )
    risultati = cursor.fetchall()
    conn.close()
    return risultati

@app.post("/prodotti", status_code=201)
def crea_prodotto(dati: ProdottoIn):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO prodotti (nome, prezzo) VALUES (?, ?)", (dati.nome, dati.prezzo))
    conn.commit()
    conn.close()
    return {"status": "Prodotto registrato con successo"}

@app.delete("/prodotti/{id_prodotto}")
def elimina(id_prodotto: int):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM prodotti WHERE id=?", (id_prodotto,))
    if cursor.rowcount == 0:
        conn.close()
        raise HTTPException(status_code=404, detail="Prodotto non trovato nel database")
    conn.commit()
    conn.close()
    return {"status": "Cancellato"}

@app.put("/prodotti/{id_prodotto}")
def aggiorna_prodotto(id_prodotto: int, dati: ProdottoIn):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("UPDATE prodotti SET nome = ?, prezzo = ? WHERE id = ?", (dati.nome, dati.prezzo, id_prodotto))
    if cursor.rowcount == 0:
        conn.close()
        raise HTTPException(status_code=404, detail="Prodotto non trovato nel database")
    conn.commit()
    conn.close()
    return {"status": "Modifica salvata"}




