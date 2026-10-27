from dotenv import load_dotenv
from langchain.chat_models import init_chat_model

load_dotenv()

# Inicjalizacja modelu w standardzie LangChain 1.0
model = init_chat_model("gpt-4o-mini", temperature=0.2)

prompt = "Wyjaśnij w 3 zwięzłych zdaniach, dlaczego architektura MRKL łączy sieci neuronowe z modułami symbolicznymi."
print(f"User: {prompt}\n")
print("Bot (Streaming):")

# Strumieniowanie tokenów za pomocą generatora model.stream()
for chunk in model.stream(prompt):
    print(chunk.content, end="", flush=True)

print("\n\nStrumieniowanie LangChain zakończone pomyślnie.")
