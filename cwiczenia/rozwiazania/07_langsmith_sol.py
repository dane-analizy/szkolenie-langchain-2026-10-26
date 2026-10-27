import os
import uuid
from datetime import datetime
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model

load_dotenv()

user_login = os.getenv("USERNAME", "kursant")
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
session_id = f"{user_login}_{timestamp}_{uuid.uuid4().hex[:4]}"

model = init_chat_model("gpt-4o-mini", temperature=0.1)

config = {
    "metadata": {
        "session_id": session_id,
        "user": user_login
    },
    "tags": ["cwiczenie-2-1", user_login]
}

prompt = "Czym różni się podejście heurystyczne od agenta opartego na LLM? Odpowiedz w 2 zdaniach."
print(f"Wysyłam zapytanie dla sesji: {session_id} ...")

odpowiedz = model.invoke(prompt, config=config)

print("\nBot:", odpowiedz.content)
print(f"\nGotowe! Wejdź na https://eu.smith.langchain.com i sprawdź projekt 'bol-chat-bot'.")
