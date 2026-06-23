import sqlite3

def dbinit():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    
    # Creazione tabella prodotti (Lezione 5, Slide 6)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS prodotti (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        prezzo REAL
    )
    """)
    
    # Creazione tabella utenti (Lezione 9, Slide 3)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS utenti (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL,
        token TEXT
    )
    """)

    conn.commit()

    # Controllo se è vuoto (Lezione 5, Slide 12)
    cursor.execute("SELECT * FROM prodotti")
    risultato = cursor.fetchall()

    # Se vuoto lo popolo con dei dati di esempio (Lezione 5, Slide 9)
    if not risultato:
        lista_prodotti = [
            ("Mouse Wireless", 25.50),
            ("Tastiera Meccanica", 89.90),
            ("Monitor 24 Pollici", 149.00),
            ("Cuffie Gaming", 45.00),
            ("Tappetino XL", 15.00)
        ]
        cursor.executemany("INSERT INTO prodotti (nome, prezzo) VALUES (?, ?)", lista_prodotti)
        conn.commit()

    # Chiudiamo la connessione iniziale globale
    conn.close()
    print("Eseguita inizializzazione database")