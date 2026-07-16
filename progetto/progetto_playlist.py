import sqlite3
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from .progetto_classi_validazione import PlaylistIn

# Inizializziamo il router delle playlist
router = APIRouter()

@router.post("/playlist")
def crea_playlist(dati: PlaylistIn, token: str):
    # 1. Apriamo la connessione al database
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    
    # 2. Verifichiamo a quale utente appartiene il token inviato
    cursor.execute("SELECT id FROM utenti WHERE token = ?", (token,))
    utente = cursor.fetchone()
    
    # 3. Se il token non esiste o è errato, blocchiamo l'azione
    if utente is None:
        conn.close()
        raise HTTPException(status_code=401, detail="Devi fare il login!")
    
    id_creatore = utente[0] # Ecco l'ID dell'utente loggato recuperato in sicurezza
    
    try:
        # 4. Inseriamo la nuova playlist nel database
        cursor.execute("""
            INSERT INTO playlist_video (titolo_playlist, utente_id) 
            VALUES (?, ?)
        """, (dati.titolo_playlist, id_creatore))
        
        conn.commit()
        conn.close()
        return {"status": "Playlist creata con successo!", "titolo": dati.titolo_playlist}
        
    except Exception as e:
        conn.close()
        raise HTTPException(status_code=500, detail=f"Errore durante la creazione: {str(e)}")
    
@router.get("/playlist")
def dammi_mie_playlist(token: str):
    # 1. Apriamo la connessione al database
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row  # Conversione attiva in dizionari
    cursor = conn.cursor()
    
    # 2. Verifichiamo il token
    cursor.execute("SELECT id FROM utenti WHERE token = ?", (token,))
    utente = cursor.fetchone()
    
    # 3. Blocco di sicurezza se il token non esiste
    if utente is None:
        conn.close()
        raise HTTPException(status_code=401, detail="Token non valido o scaduto!")
        
    id_utente_trovato = utente[0]
    
    # 4. Recuperiamo le sole playlist dell'utente
    cursor.execute("""
        SELECT id, titolo_playlist 
        FROM playlist_video 
        WHERE utente_id = ? AND film_id IS NULL
    """, (id_utente_trovato,))
    
    mie_liste = cursor.fetchall()
    conn.close()
    
    return mie_liste

@router.post("/playlist/aggiungi-film")
def aggiungi_film_a_lista(titolo_p: str, id_f: int, token: str):
    # 1. Convalida del token di sicurezza
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM utenti WHERE token = ?", (token,))
    utente = cursor.fetchone()
    
    if utente is None:
        conn.close()
        raise HTTPException(status_code=401, detail="Token non valido o scaduto!")
        
    id_utente_reale = utente[0]
    
    try:
        # 2. Se valido, eseguiamo l'inserimento agganciando il film alla playlist
        cursor.execute("""
            INSERT INTO playlist_video (titolo_playlist, utente_id, film_id) 
            VALUES (?, ?, ?)
        """, (titolo_p, id_utente_reale, id_f))
        
        conn.commit()
        conn.close()
        return {"status": "Film aggiunto alla playlist!", "playlist": titolo_p, "film_id": id_f}
        
    except Exception as e:
        conn.close()
        raise HTTPException(status_code=500, detail=f"Errore durante l'inserimento: {str(e)}")


@router.get("/playlist/dettaglio")
def dettaglio_playlist(titolo_p: str, token: str):
    # 1. Convalida del token
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM utenti WHERE token = ?", (token,))
    utente = cursor.fetchone()
    
    if utente is None:
        conn.close()
        raise HTTPException(status_code=401, detail="Token non valido!")
        
    id_utente_reale = utente[0]
    
    # 2. Query con JOIN per estrarre i dettagli di tutti i film di questa playlist
    cursor.execute("""
        SELECT film.id, film.titolo, film.url_locandina 
        FROM playlist_video 
        JOIN film ON playlist_video.film_id = film.id 
        WHERE playlist_video.titolo_playlist = ? AND playlist_video.utente_id = ?
    """, (titolo_p, id_utente_reale))
    
    film_in_lista = cursor.fetchall()
    conn.close()
    
    return film_in_lista