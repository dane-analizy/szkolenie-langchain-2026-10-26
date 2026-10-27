import sqlite3

from fastapi import FastAPI, HTTPException

app = FastAPI(
    title="Kino API Service",
    description="Mikroserwis udostępniający bazę filmów dla Agentów AI",
    version="1.0",
)


def get_db():
    conn = sqlite3.connect("filmy.db")
    conn.row_factory = sqlite3.Row
    return conn


@app.get("/")
def root():
    return {"status": "ok", "service": "Kino API Service", "docs": "/docs"}


@app.get("/api/movies/search")
def search_movies(genre: str | None = None):
    """Wyszukuje filmy według gatunku."""
    conn = get_db()
    cursor = conn.cursor()
    if genre:
        query = """
            SELECT f.tytul, f.data_premiery, f.ocena_filmweb, f.liczba_glosow, g.nazwa_gatunku
            FROM fakt_filmy f
            JOIN wymiar_gatunki g ON f.id_gatunku = g.id_gatunku
            WHERE LOWER(g.nazwa_gatunku) = LOWER(?)
            ORDER BY f.ocena_filmweb DESC NULLS LAST
            LIMIT 10;
        """
        cursor.execute(query, (genre.strip(),))
    else:
        query = """
            SELECT tytul, data_premiery, ocena_filmweb, liczba_glosow
            FROM fakt_filmy
            ORDER BY ocena_filmweb DESC NULLS LAST
            LIMIT 10;
        """
        cursor.execute(query)

    rows = [dict(r) for r in cursor.fetchall()]
    conn.close()
    return {"count": len(rows), "results": rows}


@app.get("/api/movies/{title}")
def get_movie_details(title: str):
    """Pobiera szczegóły filmu i obsadę aktorską."""
    conn = get_db()
    cursor = conn.cursor()
    query = """
        SELECT f.id_filmu, f.tytul, f.data_premiery, f.ocena_filmweb, f.liczba_glosow,
            rez.imie || ' ' || rez.nazwisko AS rezyser,
            scen.imie || ' ' || scen.nazwisko AS scenarzysta
        FROM fakt_filmy f
        LEFT JOIN wymiar_osoby rez ON f.id_rezysera = rez.id_osoby
        LEFT JOIN wymiar_osoby scen ON f.id_scenarzysty = scen.id_osoby
        WHERE LOWER(f.tytul) LIKE LOWER(?);
    """
    cursor.execute(query, (f"%{title.strip()}%",))
    row = cursor.fetchone()
    if not row:
        conn.close()
        raise HTTPException(status_code=404, detail="Film nie został znaleziony")
    film = dict(row)

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
    import uvicorn

    print("Uruchamiam serwer FastAPI na http://127.0.0.1:8000...")
    uvicorn.run(app, host="0.0.0.0", port=8000)
