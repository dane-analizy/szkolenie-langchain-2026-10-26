import os
import sqlite3
import json
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY", "dummy_key_dla_testow_bazy")
client = OpenAI(api_key=api_key)

def podsumuj_rezysera(nazwisko: str) -> dict:
    """Zwraca statystyki reżysera z bazy SQLite."""
    conn = sqlite3.connect("filmy.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    query = """
        SELECT 
            o.imie || ' ' || o.nazwisko AS rezyser,
            COUNT(f.id_filmu) AS liczba_filmow,
            ROUND(AVG(f.ocena_filmweb), 2) AS srednia_ocena,
            SUM(f.liczba_glosow) AS suma_glosow
        FROM fakt_filmy f
        JOIN wymiar_osoby o ON f.id_rezysera = o.id_osoby
        WHERE LOWER(o.nazwisko) = LOWER(?)
        GROUP BY o.id_osoby;
    """
    cursor.execute(query, (nazwisko,))
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else {"komunikat": "Nie znaleziono reżysera"}

if __name__ == "__main__":
    wynik = podsumuj_rezysera("Nolan")
    print("Wynik z bazy:", wynik)
    assert wynik.get("srednia_ocena") is not None, "Błąd: zapytanie nie zwróciło średniej oceny!"
    print("Zapytanie SQL z bezpiecznym parametrem '?' działa bezbłędnie!")
