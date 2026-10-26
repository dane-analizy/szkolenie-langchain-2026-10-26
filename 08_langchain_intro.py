from dotenv import load_dotenv
from langchain.chat_models import init_chat_model

load_dotenv()

# Inicjalizacja uniwersalnego modelu w LangChain 1.0
model = init_chat_model("gpt-4o-mini", temperature=0.1)

print("Most do Dnia 2: Pierwsze wywołanie modelu w LangChain 1.0\n")

prompt = "W jednym zwięzłym zdaniu: czym różni się prosty łańcuch (Chain) od Agenta AI?"
print(f"Pytanie: {prompt}\n")

response = model.invoke(prompt)

print("Odpowiedź LangChain:")
print(response.content)
