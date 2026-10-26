import json
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI()

def zapisz_plik(nazwa_pliku: str, tresc: str) -> str:
    with open(nazwa_pliku, "w", encoding="utf-8") as f:
        f.write(tresc)
    return f"Sukces: zapisano plik {nazwa_pliku}."

AVAILABLE_TOOLS = {"zapisz_plik": zapisz_plik}

# TODO 1: Uzupełnij opis (description) i parametry w JSON Schema
tools_schema = [{
    "type": "function",
    "function": {
        "name": "zapisz_plik",
        "description":   # <-- UZUPEŁNIJ OPIS
        "parameters": {
            "type": "object",
            "properties": {
                "nazwa_pliku":  # <--- UZUPEŁNIJ
                "tresc":        # <--- UZUPEŁNIJ
            },
            "required": ["nazwa_pliku", "tresc"]
        }
    }
}]

messages = [
    {"role": "system", "content": "Jesteś asystentem posiadającym narzędzia plikowe."},
    {"role": "user", "content": "Zapisz w pliku 'notatka_testowa.txt' tekst: 'Cześć z warsztatów AI!'"}
]

res = client.chat.completions.create(model="gpt-4o-mini", messages=messages, tools=tools_schema)
choice = res.choices[0]

# Obsługa wywołania narzędzia
if choice.finish_reason == "tool_calls":
    tool_call = choice.message.tool_calls[0]
    fn_name = tool_call.function.name
    fn_args = json.loads(tool_call.function.arguments)
    print(f"Model wywołał: {fn_name}({fn_args})")
    
    # Wykonanie funkcji w Pythonie
    wynik_dzialania = AVAILABLE_TOOLS[fn_name](**fn_args)
    
    # TODO 2: Dołącz do listy messages informację o wywołaniu narzędzia:
    # 1. Dołącz najpierw choice.message (odpowiedź asystenta z id narzędzia)
    # 2. Dołącz słownik roli 'tool' z parametrami: role, tool_call_id, content
    messages.append()           # <-- UZUPEŁNIJ
    messages.append({
        "role":                 # <-- UZUPEŁNIJ
        "tool_call_id":         # <-- UZUPEŁNIJ
        "content":              # <-- UZUPEŁNIJ
    })
    
    # Finałowe zapytanie z wynikiem
    final_res = client.chat.completions.create(model="gpt-4o-mini", messages=messages)
    print("\nBot:", final_res.choices[0].message.content)
