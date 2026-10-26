from openai import OpenAI

# TODO: Skonfiguruj klienta pod lokalną Ollamę:
# - base_url: domyślny port Ollamy ze ścieżką /v1 ("http://localhost:11434/v1")
# - api_key: dowolny string, np. "ollama"
client = OpenAI(
    base_url=  # <-- UZUPEŁNIJ
    api_key=   # <-- UZUPEŁNIJ
)

# TODO: Podmień model na "llama3.2:3b"
try:
    response = client.chat.completions.create(
        model= # <-- UZUPEŁNIJ
        messages=[{"role": "user", "content": "Wymień 2 znane polskie komedie."}],
        temperature=0.1
    )
    print("Odpowiedź z lokalnej Ollamy:")
    print(response.choices[0].message.content)
except Exception as e:
    print(f"Błąd połączenia z Ollamą: {e}")
    print("Upewnij się, że usługa Ollama działa w tle: `ollama run llama3.2:3b`")
