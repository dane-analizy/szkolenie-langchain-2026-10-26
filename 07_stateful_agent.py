import json
import os
from dotenv import load_dotenv
from openai import OpenAI
from domain_tools import szukaj_filmow_gatunku, pobierz_szczegoly_filmu

# 1 przygotuj bazę danych - użyj setup_db.py
# 2 zobacz do domain_tools.py


load_dotenv()
client = OpenAI()

AVAILABLE_TOOLS = {
    "szukaj_filmow_gatunku": szukaj_filmow_gatunku,
    "pobierz_szczegoly_filmu": pobierz_szczegoly_filmu
}

tools_schema = [
    {
        "type": "function",
        "function": {
            "name": "szukaj_filmow_gatunku",
            "description": "Wyszukuje filmy w bazie kina według nazwy gatunku (np. Sci-Fi, Dramat, Komedia).",
            "parameters": {
                "type": "object",
                "properties": {
                    "nazwa_gatunku": {"type": "string", "description": "Nazwa gatunku filmowego"}
                },
                "required": ["nazwa_gatunku"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "pobierz_szczegoly_filmu",
            "description": "Pobiera szczegóły filmu: reżyser, scenarzysta, ocena i obsada aktorska.",
            "parameters": {
                "type": "object",
                "properties": {
                    "tytul": {"type": "string", "description": "Tytuł filmu"}
                },
                "required": ["tytul"]
            }
        }
    }
]

SYSTEM_PROMPT = {
    "role": "system",
    "content": "Jesteś asystentem kinowym. Pamiętasz wcześniejsze wątki rozmowy i korzystasz z narzędzi bazy SQLite."
}

def start_chat():
    conversation_history = [SYSTEM_PROMPT]
    print("Rozpoczynamy rozmowę z agentem (Pamięć Włączona)!")
    print("Wpisz '/new' aby wyczyścić pamięć, lub 'exit' aby zakończyć.\n")
    
    while True:
        user_input = input("Ty > ").strip()
        if not user_input or user_input.lower() == "exit":
            break
            
        if user_input.lower() == "/new":
            conversation_history = [SYSTEM_PROMPT]
            print(f"[Pamięć wyczyszczona! Rozpoczynamy nowy wątek.]\n")
            continue
            
        conversation_history.append({"role": "user", "content": user_input})
        
        while True:
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=conversation_history,
                tools=tools_schema
            )
            choice = response.choices[0]
            
            if choice.finish_reason != "tool_calls":
                conversation_history.append(choice.message)
                print(f"Bot > {choice.message.content}\n")
                break
                
            conversation_history.append(choice.message)
            for tool_call in choice.message.tool_calls:
                fn_name = tool_call.function.name
                fn_args = json.loads(tool_call.function.arguments)
                print(f"[Tool] Wywołuję: {fn_name}({fn_args})")
                
                result = AVAILABLE_TOOLS[fn_name](**fn_args)
                print(f"[Tool] Wynik: {result}")
                conversation_history.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": json.dumps(result, ensure_ascii=False)
                })

if __name__ == "__main__":
    start_chat()
