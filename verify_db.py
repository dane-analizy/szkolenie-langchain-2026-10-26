import sqlite3

conn = sqlite3.connect("filmy.db")
cursor = conn.cursor()

# Zapytanie 1: Filmy z nazwami gatunków i reżyserami (przykładowe 5 wyników)
query_1 = """
SELECT f.tytul, g.nazwa_gatunku, o.imie || ' ' || o.nazwisko AS rezyser
FROM fakt_filmy f
JOIN wymiar_gatunki g ON f.id_gatunku = g.id_gatunku
JOIN wymiar_osoby o ON f.id_rezysera = o.id_osoby
LIMIT 5;
"""
print("--- Zapytanie 1: Filmy i Reżyserzy (pierwsze 5 wyników) ---")
for row in cursor.execute(query_1):
    print(row)

# Zapytanie 2: Kto zagrał w filmie Diuna?
query_2 = """
SELECT f.tytul, o.imie || ' ' || o.nazwisko AS aktor, r.rola
FROM relacja_obsada r
JOIN fakt_filmy f ON r.id_filmu = f.id_filmu
JOIN wymiar_osoby o ON r.id_osoby = o.id_osoby
WHERE f.tytul = 'Diuna'
LIMIT 5;
"""
print("\n--- Zapytanie 2: Obsada filmu Diuna (pierwsze 5 wyników) ---")
for row in cursor.execute(query_2):
    print(row)

conn.close()
