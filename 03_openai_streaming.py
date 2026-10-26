from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI()

print("Generuję odpowiedź w czasie rzeczywistym (streaming):\n")

stream = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": "Jesteś krytykiem filmowym."},
        {
            "role": "user",
            "content": "Napisz krótki, jednoakapitowy esej o filmie 'Interstellar'.",
        },
    ],
    stream=True,
)

for chunk in stream:
    # Wyciągamy wygenerowany kawałek tekstu (delta token)
    content = chunk.choices[0].delta.content or ""
    print(content, end="", flush=True)

print("\n\nStrumieniowanie zakończone.")
