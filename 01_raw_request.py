import os
from pprint import pprint

import requests
from dotenv import load_dotenv

# Wczytanie zmiennych z pliku .env
load_dotenv()

API_KEY = os.getenv("OPENAI_API_KEY")
if not API_KEY:
    raise ValueError("Brak klucza OPENAI_API_KEY w pliku .env!")

URL = "https://api.openai.com/v1/chat/completions"

headers = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}

payload = {
    "model": "gpt-4o-mini",
    "messages": [
        {
            "role": "system",
            "content": "Jesteś cynicznym krytykiem filmowym. Odpowiadaj zwięźle.",
        },
        {"role": "user", "content": "Jaki jest najlepszy film 2023 roku?"},
    ],
    "temperature": 0.2,
}

print("Wysyłam surowe zapytanie HTTP POST przez bibliotekę requests...")
response = requests.post(URL, headers=headers, json=payload)

pprint("\n--- Surowa odpowiedź HTTP ---")
pprint(response)

if response.status_code == 200:
    data = response.json()
    print("\n--- Odpowiedź API ---")
    pprint(data)
    print("\n--- Odpowiedź modelu ---")
    print(data["choices"][0]["message"]["content"])
    print("\n--- Koszt ---")
    print(
        f"\nZużyto tokenów: {data['usage']['total_tokens']} "
        f"(prompt: {data['usage']['prompt_tokens']}, completion: {data['usage']['completion_tokens']})"
    )
else:
    print(f"\nBłąd HTTP {response.status_code}: {response.text}")
