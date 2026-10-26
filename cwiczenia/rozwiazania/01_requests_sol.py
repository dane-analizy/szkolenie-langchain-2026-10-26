import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("OPENAI_API_KEY")
URL = "https://api.openai.com/v1/chat/completions"

gatunek = "Sci-Fi"

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

payload = {
    "model": "gpt-4o-mini",
    "messages": [
        {"role": "system", "content": "Jesteś cynicznym krytykiem filmowym. Odpowiadaj w 2 zdaniach."},
        {"role": "user", "content": f"Poleć mi jeden niszowy film z gatunku: {gatunek}"}
    ],
    "temperature": 0.2
}

response = requests.post(URL, headers=headers, json=payload)

if response.status_code == 200:
    data = response.json()
    odpowiedz = data["choices"][0]["message"]["content"]
    
    prompt_tokens = data["usage"]["prompt_tokens"]
    completion_tokens = data["usage"]["completion_tokens"]
    
    print("Recenzja:", odpowiedz)
    print(f"Zużyto tokenów: wejście={prompt_tokens}, wyjście={completion_tokens}")
else:
    print(f"Błąd HTTP {response.status_code}: {response.text}")
