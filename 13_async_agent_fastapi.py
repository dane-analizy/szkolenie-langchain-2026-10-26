import asyncio
import os
import uuid
from datetime import datetime

import httpx
from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain.chat_models import init_chat_model
from langchain.messages import HumanMessage, SystemMessage
from langchain.tools import tool

load_dotenv()

API_URL = "http://localhost:8000"


# 1 zobacz jak zbudowany jest serwer API - kino_api.py
# 2 uruchom go


# Definicja narzędzi asynchronicznych z httpx
@tool
async def api_szukaj_filmow(gatunek: str) -> dict:
    """Wyszukuje filmy w API kina na podstawie gatunku (np. Sci-Fi, Komedia)."""
    async with httpx.AsyncClient() as client:
        try:
            res = await client.get(
                f"{API_URL}/api/movies/search", params={"genre": gatunek}
            )
            return (
                res.json()
                if res.status_code == 200
                else {"error": f"Błąd API: status {res.status_code}"}
            )
        except httpx.ConnectError:
            return {
                "error": "Nie można połączyć się z serwerem API. Upewnij się, że 'kino_api.py' jest uruchomiony na porcie 8000."
            }


@tool
async def api_pobierz_szczegoly(tytul: str) -> dict:
    """Pobiera z API kina szczegółowe dane filmu (twórcy, obsada) po tytule."""
    async with httpx.AsyncClient() as client:
        try:
            res = await client.get(f"{API_URL}/api/movies/{tytul}")
            return (
                res.json()
                if res.status_code == 200
                else {"error": "Film nie znaleziony w API"}
            )
        except httpx.ConnectError:
            return {"error": "Nie można połączyć się z serwerem API na porcie 8000."}


async def main():
    # Konfiguracja sesji z trackingiem w LangSmith
    user_login = os.getenv("USER", "kursant_sages")
    session_id = f"warsztat_{user_login}_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{uuid.uuid4().hex[:6]}"
    config = {
        "configurable": {"thread_id": session_id},
        "metadata": {"session_id": session_id, "user": user_login},
        "tags": ["warsztat", "langchain-agent"],
    }
    model = init_chat_model("gpt-4o-mini", temperature=0.0)
    agent = create_agent(
        model=model,
        tools=[api_szukaj_filmow, api_pobierz_szczegoly],
    )

    pytanie = (
        "Wyszukaj w API filmy z gatunku Sci-Fi i sprawdź, kto zagrał w filmie Diuna."
    )
    print(f"User: {pytanie}\n")

    # Wywołanie asynchroniczne bez blokowania pętli zdarzeń asyncio
    print("Wywołuję asynchronicznego agenta (ainvoke)...")
    # odpowiedz = await agent.ainvoke(
    #     {"messages": [{"role": "user", "content": pytanie}]}, config=config
    # )

    odpowiedz = await agent.ainvoke(
        {
            "messages": [
                SystemMessage(
                    content="Jesteś doradcą filmowym. Korzystaj z narzędzi asynchronicznego API kina."
                ),
                HumanMessage(content=pytanie),
            ]
        },
        config=config,
    )

    print("Odpowiedź agenta otrzymana, wyświetlam wynik...")
    print(odpowiedz)

    print("\nAgent:")
    print(odpowiedz["messages"][-1].content)


if __name__ == "__main__":
    asyncio.run(main())
