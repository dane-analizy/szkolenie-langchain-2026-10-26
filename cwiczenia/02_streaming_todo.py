import sys
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI()

prompt = "Napisz krótki, 3-wersowy wiersz o programowaniu w Pythonie."
print(f"User: {prompt}\nBot: ", end="")

# TODO 1: Włącz streaming w wywołaniu metody (stream=True)
stream = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": prompt}],
    stream=  # <-- UZUPEŁNIJ (włącz parametr stream)
)

# TODO 2: W pętli for wyciągnij tekst tokenu z każdego chunka i wypisz go z flush=True
for chunk in stream:
    token =   # <-- UZUPEŁNIJ wyciągnięcie tekstu
    print(token, end="", flush=True)

print("\n\nZakończono.")
