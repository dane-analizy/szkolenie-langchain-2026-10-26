import sqlite3


def szukaj_filmow_gatunku(nazwa_gatunku: str) -> list[dict]:
    """Wyszukuje filmy w bazie na podstawie nazwy gatunku (np. Sci-Fi, Komedia)."""
    conn = sqlite3.connect("filmy.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    query = """
    SELECT f.tytul, f.data_premiery, f.ocena_filmweb, f.liczba_glosow, g.nazwa_gatunku
    FROM fakt_filmy f
    JOIN wymiar_gatunki g ON f.id_gatunku = g.id_gatunku
    WHERE LOWER(g.nazwa_gatunku) = LOWER(?)
    ORDER BY f.ocena_filmweb DESC NULLS LAST
    LIMIT 10;
    """
    cursor.execute(query, (nazwa_gatunku,))
    wyniki = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return wyniki


def pobierz_szczegoly_filmu(tytul: str) -> dict:
    """Zwraca pełne szczegóły filmu: twórców, oceny Filmweb i obsadę aktorską."""
    conn = sqlite3.connect("filmy.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    query_film = """
    SELECT 
        f.id_filmu, f.tytul, f.data_premiery, f.ocena_filmweb, f.liczba_glosow,
        g.nazwa_gatunku,
        rez.imie || ' ' || rez.nazwisko AS rezyser,
        scen.imie || ' ' || scen.nazwisko AS scenarzysta
    FROM fakt_filmy f
    LEFT JOIN wymiar_gatunki g ON f.id_gatunku = g.id_gatunku
    LEFT JOIN wymiar_osoby rez ON f.id_rezysera = rez.id_osoby
    LEFT JOIN wymiar_osoby scen ON f.id_scenarzysty = scen.id_osoby
    WHERE LOWER(f.tytul) LIKE LOWER(?);
    """
    cursor.execute(query_film, (f"%{tytul}%",))
    film_row = cursor.fetchone()

    if not film_row:
        conn.close()
        return {"error": f"Nie znaleziono filmu o tytule pasującym do '{tytul}'"}

    film = dict(film_row)

    # Pobranie obsady
    cursor.execute(
        """
        SELECT o.imie || ' ' || o.nazwisko AS aktor, r.rola
        FROM relacja_obsada r
        JOIN wymiar_osoby o ON r.id_osoby = o.id_osoby
        WHERE r.id_filmu = ?
        LIMIT 10;
    """,
        (film["id_filmu"],),
    )
    film["obsada"] = [dict(r) for r in cursor.fetchall()]
    conn.close()
    return film


if __name__ == "__main__":
    print("Test bezpiecznych narzędzi domenowych SQL:")
    print("\n1. szukaj_filmow_gatunku('Sci-Fi'):")
    print(szukaj_filmow_gatunku("Sci-Fi"))
    print("\n2. pobierz_szczegoly_filmu('Diuna'):")
    print(pobierz_szczegoly_filmu("Diuna"))
