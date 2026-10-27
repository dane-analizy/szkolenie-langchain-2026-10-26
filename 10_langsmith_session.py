import os
import uuid
from datetime import datetime

from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain.chat_models import init_chat_model
from langchain.tools import tool

load_dotenv()

# Sprawdzenie obecności kluczy LangSmith
if not os.getenv("LANGCHAIN_API_KEY"):
    print(
        "Uwaga: Brak klucza LANGCHAIN_API_KEY w .env. Zapytanie zadziała lokalnie, ale nie pojawi się w LangSmith."
    )


# 1. Definicja przykładowego narzędzia biznesowego
@tool
def sprawdz_status_subskrypcji(id_uzytkownika: str) -> dict:
    """Sprawdza ważność abonamentu i limit tokenów dla danego konta klienta."""
    print(f"[TOOL]: Sprawdzanie statusu subskrypcji dla użytkownika: {id_uzytkownika}")
    return {
        "id_uzytkownika": id_uzytkownika,
        "plan": "PRO_VIP",
        "aktywny": True,
        "pozostaly_limit_zapytan": 1420,
        "komentarz": "To są zmyślone dane, nie zastanawiaj się nad tym za wiele!",
        "data_urodzenia": "2023-12-31",
        "extra_info": "Specjalnie na życzie kursanta, aby pokazać jak można zwracać dodatkowe informacje w formacie JSON.",
    }


# 2. Inicjalizacja modelu i agenta w LangChain 1.0
model = init_chat_model("gpt-4o-mini", temperature=0.0)
agent = create_agent(
    model=model,
    tools=[sprawdz_status_subskrypcji],
    system_prompt="Jesteś doradcą obsługi klienta. Korzystaj z narzędzi do weryfikacji konta.",
)

# 3. Dynamiczne generowanie ID sesji użytkownika (login + data/godzina + UUID)
user_login = os.getenv("USERNAME", "kursant_sages")
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
session_id = f"warsztat_{user_login}_{timestamp}_{uuid.uuid4().hex[:6]}"

print(f"Aktywna sesja użytkownika: {session_id}")

# 4. Przekazanie metadanych i tagów w konfiguracji LangSmith
config = {
    "configurable": {"thread_id": session_id},
    "metadata": {
        "session_id": session_id,
        "user": user_login,
        "environment": "workshop_production",
    },
    "tags": ["warsztat", "film-bot", user_login],
}

# 5. Wywołanie agenta z pełnym tracingiem
pytanie = f"Sprawdź czy użytkownik {user_login} ma aktywny abonament i ile zapytań mu zostało, dodaj ewentualne komentarze."
print(f"User: {pytanie}\n")

response = agent.invoke(
    {"messages": [{"role": "user", "content": pytanie}]}, config=config
)

print("Bot:")
print(response["messages"][-1].content)
print(
    "\nZapytanie wysłane! Jeśli masz skonfigurowany serwer EU, sprawdź ślad na: https://eu.smith.langchain.com"
)
