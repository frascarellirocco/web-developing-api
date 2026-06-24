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