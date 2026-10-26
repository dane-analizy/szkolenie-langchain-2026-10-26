import sys
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI()

prompt = "Napisz krótki, 3-wersowy wiersz o programowaniu w Pythonie."
print(f"User: {prompt}\nBot: ", end="")

stream = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": prompt}],
    stream=True
)

for chunk in stream:
    token = chunk.choices[0].delta.content or ""
    print(token, end="", flush=True)

print("\n\nZakończono.")
