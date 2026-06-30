from fastapi import APIRouter, HTTPException
import sqlite3

router = APIRouter()

@router.get("/film/cerca")
def cerca_film(keyword: str):
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    
    cursor.execute("SELECT * FROM film WHERE titolo LIKE ?", (f"%{keyword}%",))
    risultato = cursor.fetchall()
    conn.close()
    
    if not risultato:
        raise HTTPException(status_code=404, detail="Film non trovato")
    return risultato

    # ESERCITAZIONE 4: Rotta di dettaglio per il singolo film (Slide 10-11)
@router.get("/film/{id_film}")
def dettaglio_film(id_film: int):
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row  # Fondamentale per leggere i dati come dizionario
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM film WHERE id = ?", (id_film,))
    risultato = cursor.fetchone()  # Recuperiamo un solo risultato (il singolo film)
    conn.close()
    
    if not risultato:
        raise HTTPException(status_code=404, detail="Film non trovato")
    return risultato