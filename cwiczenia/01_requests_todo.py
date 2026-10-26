import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("OPENAI_API_KEY")
URL = "https://api.openai.com/v1/chat/completions"

gatunek = "Sci-Fi"

# TODO 1: Uzupełnij nagłówek autoryzacyjny Bearer token
headers = {
    "Authorization": # <-- UZUPEŁNIJ TU
    "Content-Type": "application/json"
}

# TODO 2: Zbuduj ciało zapytania (messages):
# - dodaj rolę 'system' z instrukcją: "Jesteś cynicznym krytykiem filmowym. Odpowiadaj w 2 zdaniach."
# - dodaj rolę 'user' z pytaniem o film z gatunku {gatunek}
payload = {
    "model": "gpt-4o-mini",
    "messages": [
        # --- UZUPEŁNIJ TUTAJ (2 linijki) ---
        # -----------------------------------
    ],
    "temperature": 0.2
}

response = requests.post(URL, headers=headers, json=payload)

if response.status_code == 200:
    data = response.json()
    odpowiedz = data["choices"][0]["message"]["content"]
    
    # TODO 3: Wyciągnij liczbę tokenów z obiektu usage
    prompt_tokens = # <-- UZUPEŁNIJ
    completion_tokens = # <-- UZUPEŁNIJ
    
    print("Recenzja:", odpowiedz)
    print(f"Zużyto tokenów: wejście={prompt_tokens}, wyjście={completion_tokens}")
else:
    print(f"Błąd HTTP {response.status_code}: {response.text}")
