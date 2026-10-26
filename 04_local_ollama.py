# 1. Zainstaluj Ollama -> https://ollama.com/
# 2. Pobierz model LLaMA 3.2:3b -> `ollama pull llama3.2:3b`
# 3. Uruchom lokalny serwer Ollama -> `ollama run llama3.2:3b`

import os

from openai import OpenAI

# Wskazujemy adres lokalnego serwera Ollama
base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434/v1")

client = OpenAI(
    base_url=base_url,
    api_key="ollama",  # Ollama nie waliduje klucza, ale biblioteka wymaga niepustego stringa
)

print(f"Wysyłam zapytanie do lokalnego modelu (Ollama pod adresem {base_url}):\n")

try:
    response = client.chat.completions.create(
        model="llama3.2:3b",
        messages=[
            {"role": "system", "content": "Odpowiadaj krótko i po polsku."},
            {
                "role": "user",
                "content": "Kto wyreżyserował polską komedię 'Seksmisja' i w którym roku?",
            },
        ],
        temperature=0.1,
    )
    print("Odpowiedź z lokalnej maszyny:")
    print(response.choices[0].message.content)
except Exception as e:
    print(f"Nie udało się połączyć z lokalną Ollamą: {e}")
    print("Upewnij się, że usługa Ollama działa w tle: `ollama run llama3.2:3b`")
