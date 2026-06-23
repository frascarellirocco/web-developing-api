from fastapi import HTTPException, APIRouter
import sqlite3
import hashlib
import secrets

# Punto inserito per l'import relativo
from .progetto_classi_validazione import UtenteAuth

router = APIRouter()

# Definizione corretta della funzione di supporto (Lezione 9, Slide 5 e Slide 6)
def calcolaHash(passwordChiaro: str) -> str:
    hash_risultato = hashlib.sha256(passwordChiaro.encode('utf-8')).hexdigest()
    return hash_risultato

# Rotta di registrazione (Lezione 9, Slide 7 e Slide 8)
@router.post("/register")
def registra_utente(dati: UtenteAuth):
    password_sicura = calcolaHash(dati.password)

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    try:
        cursor.execute(
            "INSERT INTO utenti (username, password_hash) VALUES (?, ?)",
            (dati.username, password_sicura)
        )
        conn.commit()
        conn.close()
    except sqlite3.IntegrityError:
        conn.close()
        raise HTTPException(status_code=400, detail="Questo username e' gia' occupato. Scegline un altro")
        
    return {"status": "Utente registrato con successo"}

# ESERCITAZIONE 4: Implementazione della POST /login (Lezione 9, Slide 10 e Slide 11)
@router.post("/login")
def login(dati: UtenteAuth):
    # 1. Calcoliamo l'hash della password inviata
    hash_inviato = calcolaHash(dati.password)
    
    # 2. Cerchiamo lo username nel database
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    
    cursor.execute("SELECT id, password_hash FROM utenti WHERE username = ?", (dati.username,))
    utente = cursor.fetchone()
    
    # 3. Controllo di Sicurezza (Slide 11)
    if utente is None or utente[1] != hash_inviato:
        conn.close()
        raise HTTPException(status_code=401, detail="Credenziali errate")
        
    # 4. Generazione token e salvataggio tramite UPDATE (Slide 10)
    token_sessione = secrets.token_hex(16)
    
    cursor.execute("UPDATE utenti SET token = ? WHERE id = ?", (token_sessione, utente[0]))
    conn.commit()
    conn.close()
    
    # Restituisce il token al client
    return {"token": token_sessione}


@router.get("/profilo")
def mostra_profilo(token: str):
    # 1. Interroga il DB cercando il proprietario del pass (Slide 12, Mattoncino di controllo)
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    
    cursor.execute("SELECT id FROM utenti WHERE token = ?", (token,))
    utente = cursor.fetchone()
    conn.close()
    
    # 2. Se il token non esiste, lancia un errore 401 (Slide 12)
    if utente is None:
        raise HTTPException(status_code=401, detail="Pass non valido!")
        
    # 3. Se il token esiste, risponde con un JSON contenente l'ID dell'utente trovato (Slide 13)
    id_utente_reale = utente[0]
    return {"id_utente": id_utente_reale}

