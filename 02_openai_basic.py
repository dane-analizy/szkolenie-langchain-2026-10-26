import os
from dotenv import load_dotenv
from openai import OpenAI
from pprint import pprint

load_dotenv()

# Domyślnie klient OpenAI czyta OPENAI_API_KEY ze środowiska
client = OpenAI()

print("Wysyłam zapytanie do API OpenAI przez oficjalne SDK...")

response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": "Jesteś analitykiem rynku filmowego. Odpowiadaj zwięźle i profesjonalnie."},
        {"role": "user", "content": "Wymień 3 reżyserów, którzy zdefiniowali współczesne kino science-fiction."}
    ],
    temperature=0.8,
    n=3
)

print("\n--- Odpowiedź frameforku ---")
pprint(response.to_dict())

print("\n--- Odpowiedź modelu ---")
print(response.choices[0].message.content)

# Analiza tokenów
usage = response.usage
print(f"\nStatystyki tokenów: prompt={usage.prompt_tokens}, "
      f"completion={usage.completion_tokens}, razem={usage.total_tokens}")


print("\n--- Wszystkie odpowiedzi modelu ---")
for choice in response.choices:
    print(choice.message.content)
    print("---")

