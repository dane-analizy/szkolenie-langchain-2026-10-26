import os
import uuid
from datetime import datetime

from ddgs import DDGS
from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain.chat_models import init_chat_model
from langchain.tools import tool
from langgraph.checkpoint.memory import InMemorySaver

from agent_tools import pobierz_szczegoly_filmu, szukaj_filmow_gatunku

load_dotenv()


# 1. Definicja narzędzia wyszukiwania w sieci DuckDuckGo
@tool
def szukaj_w_internecie(zapytanie: str) -> str:
    """Wyszukuje aktualne informacje, premiery kinowe i wiadomości w Internecie (DuckDuckGo)."""
    print(f"[Web Search] Szukam w sieci: '{zapytanie}'")
    try:
        with DDGS(timeout=15) as ddgs:
            wyniki = list(ddgs.text(zapytanie, max_results=10))
            if not wyniki:
                return "Brak wyników w sieci."

            raport = []
            for r in wyniki:
                raport.append(
                    f"Tytuł: {r.get('title')}\nTreść: {r.get('body')}\nLink: {r.get('href')}"
                )
            return "\n\n".join(raport)
    except Exception as e:
        return f"Błąd wyszukiwania internetowego: {e}"


# 2. Inicjalizacja modelu i agenta z 3 narzędziami (baza + sieć)
model = init_chat_model("gpt-4o-mini", temperature=0.0)
checkpointer = InMemorySaver()

agent = create_agent(
    model=model,
    tools=[szukaj_filmow_gatunku, pobierz_szczegoly_filmu, szukaj_w_internecie],
    system_prompt=(
        "Jesteś wszechstronnym doradcą filmowym. "
        "W przypadku pytań o filmy z naszej biblioteki (np. Incepcja, Diuna, Dzień świra) sprawdzaj naszą bazę SQLite. "
        "W przypadku pytań o filmy sprzed 2020 roku korzystaj z narzędzia szukaj_w_internecie. "
        "W przypadku pytań o bieżący repertuar, aktualne premiery kinowe lub newsy ze świata kina, zawsze korzystaj "
        "z narzędzia szukaj_w_internecie."
    ),
    checkpointer=checkpointer,
)

# 3. Konfiguracja sesji z trackingiem w LangSmith
user_login = os.getenv("USER", "kursant_sages")
session_id = f"warsztat_{user_login}_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{uuid.uuid4().hex[:6]}"
config = {
    "configurable": {"thread_id": session_id},
    "metadata": {"session_id": session_id, "user": user_login},
    "tags": ["warsztat", "langchain-agent"],
}

# 4. Test 1: Pytanie wewnętrzne (Model powinien wybrać bazę SQLite
pyt1 = "Kto wyreżyserował film Diuna z naszej bazy?"
pyt2 = "Jakie filmy science-fiction miały premierę kinową przed rokiem 2000?"

print(f"Pytanie 1 (Dotyczy bazy wewnętrznej SQLite): {pyt1}")
odp1 = agent.invoke({"messages": [{"role": "user", "content": pyt1}]}, config=config)
print("Bot:", odp1["messages"][-1].content)

# 5. Test 2: Pytanie zewnętrzne (Model powinien wybrać Internet!)
print(f"\nPytanie 2 (Wymaga wyjścia do sieci internetowej): {pyt2}")
odp2 = agent.invoke({"messages": [{"role": "user", "content": pyt2}]}, config=config)
print("Bot:", odp2["messages"][-1].content)
