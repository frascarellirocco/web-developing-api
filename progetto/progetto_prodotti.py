from fastapi import APIRouter, HTTPException
import sqlite3

# Punto inserito per l'import relativo
from .progetto_classi_validazione import ProdottoIn

router = APIRouter()

# Espongo la chiamata per listare uno specifico prodotto (Lezione 6, Slide 6)
@router.get("/prodotti/{id_prodotto}")
def lista_prodotto_singolo(id_prodotto: int):
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM prodotti WHERE id = ?", (id_prodotto,))
    risultato = cursor.fetchone() 
    conn.close()
    
    if risultato is None:
        raise HTTPException(status_code=404, detail="Prodotto non trovato")
    return risultato

# Espongo la chiamata per recuperare tutti i prodotti (Lezione 5, Slide 12)
@router.get("/prodotti")
def lista_prodotti():
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM prodotti")
    risultato = cursor.fetchall()
    conn.close()
    return risultato

# Espongo la chiamata per inserire un nuovo prodotto (Lezione 6, Slide 5)
@router.post("/prodotti", status_code=201)
def crea_prodotto(dati: ProdottoIn):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO prodotti (nome, prezzo) VALUES (?, ?)", (dati.nome, dati.prezzo))
    conn.commit()
    conn.close()
    return {"status": "Prodotto registrato con successo"}

# Espongo la chiamata per modificare un prodotto (Lezione 6, Slide 6)
@router.put("/prodotti/{id_prodotto}") 
def aggiorna_prodotto(id_prodotto: int, dati: ProdottoIn):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    # Verifico se il prodotto richiesto esiste (Lezione 6, Slide 10)
    cursor.execute("SELECT * FROM prodotti WHERE id = ?", (id_prodotto,))
    risultato = cursor.fetchone()
    if risultato is None:
        conn.close()
        raise HTTPException(status_code=404, detail="Prodotto non trovato")
    
    cursor.execute("UPDATE prodotti SET nome = ?, prezzo = ? WHERE id = ?", (dati.nome, dati.prezzo, id_prodotto))
    conn.commit()
    conn.close()
    return {"status": "Modifica salvata"}

# Espongo la chiamata per cancellare un prodotto (Lezione 6, Slide 7 e Slide 10)
@router.delete("/prodotti/{id_prodotto}")
def elimina(id_prodotto: int):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    
    cursor.execute("DELETE FROM prodotti WHERE id = ?", (id_prodotto,))
    
    # Controllo di robustezza rowcount (Lezione 6, Slide 10)
    if cursor.rowcount == 0:
        conn.close()
        raise HTTPException(status_code=404, detail="Prodotto non trovato nel database")
        
    conn.commit()
    conn.close()
    return {"status": "Cancellato"}