import asyncio

import httpx
from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain.chat_models import init_chat_model
from langchain.tools import tool

load_dotenv()

API_URL = "http://localhost:8000"


@tool
async def pobierz_film_api(tytul: str) -> dict:
    """Asynchronicznie pobiera szczegóły filmu z serwera FastAPI."""
    async with httpx.AsyncClient() as client:
        res = await client.get(f"{API_URL}/api/movies/{tytul}")
        return res.json() if res.status_code == 200 else {"error": "Film nie znaleziony w API"}


async def main():
    model = init_chat_model("gpt-4o-mini", temperature=0.0)
    agent = create_agent(model=model, tools=[pobierz_film_api], system_prompt="Jesteś asystentem kinowym korzystającym z API.")

    pytanie = "Sprawdź w API, kto wyreżyserował film Diuna i jaką ma ocenę na Filmwebie."
    print(f"User: {pytanie}\n")

    odp = await agent.ainvoke({"messages": [{"role": "user", "content": pytanie}]})
    print("Bot:", odp["messages"][-1].content)


if __name__ == "__main__":
    asyncio.run(main())
