from openai import OpenAI

client = OpenAI(
    base_url="http://localhost:11434/v1",
    api_key="ollama"
)

try:
    response = client.chat.completions.create(
        model="llama3.2:3b",
        messages=[{"role": "user", "content": "Wymień 2 znane polskie komedie."}],
        temperature=0.1
    )
    print("Odpowiedź z lokalnej Ollamy:")
    print(response.choices[0].message.content)
except Exception as e:
    print(f"Błąd połączenia z Ollamą: {e}")
    print("Upewnij się, że usługa Ollama działa w tle: `ollama run llama3.2:3b`")
