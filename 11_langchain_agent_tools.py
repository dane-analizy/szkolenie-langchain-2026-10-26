import os
import uuid
from datetime import datetime

import sqlite3

from dotenv import load_dotenv

from langchain.agents import create_agent
from langchain.chat_models import init_chat_model
from langchain.tools import tool

from langgraph.checkpoint.memory import InMemorySaver


load_dotenv()


# 1. Narzędzia domenowe opakowane w dekorator @tool
@tool
def szukaj_filmow_gatunku(nazwa_gatunku: str) -> list[dict]:
    """Wyszukuje filmy w bazie SQLite na podstawie podanego gatunku (np. Sci-Fi, Komedia, Dramat)."""
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


@tool
def pobierz_szczegoly_filmu(tytul: str) -> dict:
    """Pobiera z bazy SQLite szczegóły filmu: reżysera, scenarzystę, ocenę Filmweb i obsadę aktorską."""
    conn = sqlite3.connect("filmy.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    query = """
        SELECT f.id_filmu, f.tytul, f.data_premiery, f.ocena_filmweb, f.liczba_glosow,
            rez.imie || ' ' || rez.nazwisko AS rezyser,
            scen.imie || ' ' || scen.nazwisko AS scenarzysta
        FROM fakt_filmy f
        LEFT JOIN wymiar_gatunki g ON f.id_gatunku = g.id_gatunku
        LEFT JOIN wymiar_osoby rez ON f.id_rezysera = rez.id_osoby
        LEFT JOIN wymiar_osoby scen ON f.id_scenarzysty = scen.id_osoby
        WHERE LOWER(f.tytul) LIKE LOWER(?);
    """
    cursor.execute(query, (f"%{tytul}%",))
    row = cursor.fetchone()
    if not row:
        conn.close()
        return {"error": f"Nie znaleziono filmu '{tytul}'"}
    film = dict(row)

    # Obsada
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


# 2. Inicjalizacja modelu, checkpointera pamięci i agenta
model = init_chat_model("gpt-4o-mini", temperature=0.0)
checkpointer = InMemorySaver()

agent = create_agent(
    model=model,
    tools=[szukaj_filmow_gatunku, pobierz_szczegoly_filmu],
    system_prompt="Jesteś doradcą filmowym. Korzystaj z narzędzi, aby sprawdzać dane w bazie.",
    checkpointer=checkpointer,
)

# 3. Konfiguracja sesji użytkownika
user_login = os.getenv("USER", "kursant_sages")
session_id = f"warsztat_{user_login}_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{uuid.uuid4().hex[:6]}"
config = {
    "configurable": {"thread_id": session_id},
    "metadata": {"session_id": session_id, "user": user_login},
    "tags": ["warsztat", "langchain-agent"],
}

# 4. Pytanie 1 w ramach sesji
pyt1 = "Kto wyreżyserował film Diuna i kto w nim zagrał?"
pyt2 = "A jakie inne filmy tego reżysera mamy w bazie?"

print(f"Pytanie 1: {pyt1}")
odp1 = agent.invoke({"messages": [{"role": "user", "content": pyt1}]}, config=config)
print("Bot:", odp1["messages"][-1].content)

# 5. Pytanie 2 (Test pamięci kontekstu bez powtarzania tytułu ani nazwiska!)
print(f"\nPytanie 2: {pyt2}")
odp2 = agent.invoke({"messages": [{"role": "user", "content": pyt2}]}, config=config)
print("Bot:", odp2["messages"][-1].content)
