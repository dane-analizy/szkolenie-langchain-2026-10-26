import uuid
from datetime import datetime
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model

load_dotenv()

# TODO 1: Wpisz swój login/imię bez spacji
user_login =  # <-- UZUPEŁNIJ

timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
session_id = f"{user_login}_{timestamp}_{uuid.uuid4().hex[:4]}"

# Inicjalizacja modelu w standardzie LangChain 1.0
model = init_chat_model("gpt-4o-mini", temperature=0.1)

# TODO 2: Uzupełnij słownik konfiguracyjny przekazywany do LangChain:
# - w 'metadata' przekaż 'session_id' oraz 'user'
# - w 'tags' przekaż listę stringów: ["cwiczenie-2-1", user_login]
config = {
    "metadata": {
        "session_id": # <-- UZUPEŁNIJ
        "user":       # <-- UZUPEŁNIJ
    },
    "tags":           # <-- UZUPEŁNIJ
}

prompt = "Czym różni się podejście heurystyczne od agenta opartego na LLM? Odpowiedz w 2 zdaniach."
print(f"Wysyłam zapytanie dla sesji: {session_id} ...")

# Wywołanie z przekazaniem konfiguracji
odpowiedz = model.invoke(prompt, ) # <-- UZUPEŁNIJ przekazanie konfiguracji

print("\nBot:", odpowiedz.content)
print(f"\nGotowe! Wejdź na https://eu.smith.langchain.com i sprawdź projekt 'bol-chat-bot'.")
