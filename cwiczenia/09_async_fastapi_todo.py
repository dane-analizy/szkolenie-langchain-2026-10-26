import asyncio
import httpx
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain.tools import tool
from langchain.agents import create_agent

load_dotenv()

API_URL = "http://localhost:8000"

# TODO 1: Zdefiniuj asynchroniczną funkcję narzędzia z dekoratorem @tool
@ # <-- UZUPEŁNIJ
async def pobierz_film_api(tytul: str) -> dict:
    """Asynchronicznie pobiera szczegóły filmu z serwera FastAPI."""
    async with httpx.AsyncClient() as client:
        # TODO 2: Uzupełnij asynchroniczne wywołanie GET do endpointu {API_URL}/api/movies/{tytul}
        res = # <-- UZUPEŁNIJ
        return res.json() if res.status_code == 200 else {"error": "Film nie znaleziony w API"}

async def main():
    model = init_chat_model("gpt-4o-mini", temperature=0.0)
    agent = create_agent(
        model=model,
        tools=[pobierz_film_api],
        system_prompt="Jesteś asystentem kinowym korzystającym z API."
    )

    pytanie = "Sprawdź w API, kto wyreżyserował film Diuna i jaką ma ocenę na Filmwebie."
    print(f"User: {pytanie}\n")

    # TODO 3: Wywołaj agenta asynchronicznie za pomocą metody ainvoke()
    odp = # <-- UZUPEŁNIJ
    
    print("Bot:", odp["messages"][-1].content)

if __name__ == "__main__":
    asyncio.run(main())
