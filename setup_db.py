from pathlib import Path
import sqlite3
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent
DANE_DIR = BASE_DIR / "dane"
DB_PATH = BASE_DIR / "filmy.db"

def setup_database():
    print(f"🎬 Inicjalizuję bazę danych {DB_PATH.name} wyłącznie na podstawie plików CSV z {DANE_DIR}...")

    # 1. Wymiar Gatunki
    genres_df = pd.read_csv(DANE_DIR / "genre_names.csv").dropna(subset=["id", "name"])
    genres_df = genres_df.rename(columns={"id": "id_gatunku", "name": "nazwa_gatunku"})

    # 2. Wymiar Osoby (aktorzy, reżyserzy, scenarzyści z plików *_names.csv)
    actors = pd.read_csv(DANE_DIR / "actors_names.csv")
    directors = pd.read_csv(DANE_DIR / "directors_names.csv")
    writers = pd.read_csv(DANE_DIR / "writers_names.csv")
    people = (
        pd.concat([actors, directors, writers])
        .dropna(subset=["person_id", "name"])
        .drop_duplicates(subset=["person_id"])
    )

    def split_name(name):
        parts = str(name).strip().rsplit(" ", 1)
        if len(parts) == 2:
            return parts[0], parts[1]
        return "", parts[0]

    splits = people["name"].apply(split_name)
    people["imie"] = [s[0] for s in splits]
    people["nazwisko"] = [s[1] for s in splits]
    osoby_df = people[["person_id", "imie", "nazwisko"]].rename(
        columns={"person_id": "id_osoby"}
    )

    # 3. Filmy z ocenami z filmweb.csv
    movies = pd.read_csv(DANE_DIR / "movies.csv").dropna(subset=["movie_id", "movie_title"])
    filmweb = pd.read_csv(DANE_DIR / "filmweb.csv").dropna(subset=["movie_id"])
    movies = movies.merge(filmweb, on="movie_id", how="left")

    movie_genres = pd.read_csv(DANE_DIR / "movie_genres.csv").dropna(subset=["movie_id", "genre_id"])
    first_genre = movie_genres.drop_duplicates(subset=["movie_id"])
    genre_map = dict(zip(first_genre["movie_id"], first_genre["genre_id"]))

    movie_people = pd.read_csv(DANE_DIR / "movie_people.csv").dropna(subset=["movie_id", "person_id"])
    directors_mp = movie_people[movie_people["role"] == "director"].drop_duplicates(subset=["movie_id"])
    dir_map = dict(zip(directors_mp["movie_id"], directors_mp["person_id"]))

    writers_mp = movie_people[movie_people["role"] == "writer"].drop_duplicates(subset=["movie_id"])
    writer_map = dict(zip(writers_mp["movie_id"], writers_mp["person_id"]))

    filmy_rows = []
    for _, row in movies.iterrows():
        mid = str(row["movie_id"])
        title = str(row["movie_title"])
        date = str(row["premiere_date"])
        rating = round(float(row["filmweb_rating"]), 2) if pd.notna(row["filmweb_rating"]) else None
        rating_count = int(row["filmweb_ratingcount"]) if pd.notna(row["filmweb_ratingcount"]) else None
        gid = genre_map.get(mid)
        did = dir_map.get(mid)
        wid = writer_map.get(mid)
        filmy_rows.append((mid, title, date, rating, rating_count, gid, did, wid))

    # 4. Obsada aktorska
    actors_mp = movie_people[movie_people["role"] == "actor"]
    obsada_rows = [
        (str(r["movie_id"]), str(r["person_id"]), str(r["role"]))
        for _, r in actors_mp.iterrows()
    ]

    # 5. Zapis do SQLite w schemacie gwiazdy
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("DROP TABLE IF EXISTS relacja_obsada;")
    cur.execute("DROP TABLE IF EXISTS fakt_filmy;")
    cur.execute("DROP TABLE IF EXISTS wymiar_osoby;")
    cur.execute("DROP TABLE IF EXISTS wymiar_gatunki;")

    cur.execute("""
    CREATE TABLE wymiar_gatunki (
        id_gatunku TEXT PRIMARY KEY,
        nazwa_gatunku TEXT NOT NULL
    );
    """)

    cur.execute("""
    CREATE TABLE wymiar_osoby (
        id_osoby TEXT PRIMARY KEY,
        imie TEXT NOT NULL,
        nazwisko TEXT NOT NULL
    );
    """)

    cur.execute("""
    CREATE TABLE fakt_filmy (
        id_filmu TEXT PRIMARY KEY,
        tytul TEXT NOT NULL,
        data_premiery TEXT NOT NULL,
        ocena_filmweb REAL,
        liczba_glosow INTEGER,
        id_gatunku TEXT REFERENCES wymiar_gatunki(id_gatunku),
        id_rezysera TEXT REFERENCES wymiar_osoby(id_osoby),
        id_scenarzysty TEXT REFERENCES wymiar_osoby(id_osoby)
    );
    """)

    cur.execute("""
    CREATE TABLE relacja_obsada (
        id_filmu TEXT REFERENCES fakt_filmy(id_filmu),
        id_osoby TEXT REFERENCES wymiar_osoby(id_osoby),
        rola TEXT NOT NULL
    );
    """)

    cur.executemany("INSERT INTO wymiar_gatunki VALUES (?, ?);", genres_df.values)
    cur.executemany("INSERT INTO wymiar_osoby VALUES (?, ?, ?);", osoby_df.values)
    cur.executemany("INSERT INTO fakt_filmy VALUES (?, ?, ?, ?, ?, ?, ?, ?);", filmy_rows)
    cur.executemany("INSERT INTO relacja_obsada VALUES (?, ?, ?);", obsada_rows)

    cur.execute("CREATE INDEX IF NOT EXISTS idx_fakt_filmy_gatunek ON fakt_filmy(id_gatunku);")
    cur.execute("CREATE INDEX IF NOT EXISTS idx_fakt_filmy_rezyser ON fakt_filmy(id_rezysera);")
    cur.execute("CREATE INDEX IF NOT EXISTS idx_obsada_filmu ON relacja_obsada(id_filmu);")
    cur.execute("CREATE INDEX IF NOT EXISTS idx_osoby_nazwisko ON wymiar_osoby(nazwisko);")

    conn.commit()
    conn.close()

    print(
        f"✅ Baza '{DB_PATH.name}' została pomyślnie zasilona wyłącznie danymi z '{DANE_DIR.name}/'!\n"
        f"   - Gatunki: {len(genres_df)}\n"
        f"   - Osoby: {len(osoby_df)}\n"
        f"   - Filmy: {len(filmy_rows)} (w tym z ocenami z Filmweb: {movies['filmweb_rating'].notna().sum()})\n"
        f"   - Obsada: {len(obsada_rows)}"
    )

if __name__ == "__main__":
    setup_database()
