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

tools_schema = [{
    "type": "function",
    "function": {
        "name": "zapisz_plik",
        "description": "Zapisuje tekst do pliku na dysku komputera.",
        "parameters": {
            "type": "object",
            "properties": {
                "nazwa_pliku": {"type": "string", "description": "Nazwa pliku z rozszerzeniem txt"},
                "tresc": {"type": "string", "description": "Tekst do zapisania w pliku"}
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

if choice.finish_reason == "tool_calls":
    tool_call = choice.message.tool_calls[0]
    fn_name = tool_call.function.name
    fn_args = json.loads(tool_call.function.arguments)
    print(f"Model wywołał: {fn_name}({fn_args})")
    
    wynik_dzialania = AVAILABLE_TOOLS[fn_name](**fn_args)
    
    messages.append(choice.message)
    messages.append({
        "role": "tool",
        "tool_call_id": tool_call.id,
        "content": wynik_dzialania
    })
    
    final_res = client.chat.completions.create(model="gpt-4o-mini", messages=messages)
    print("\nBot:", final_res.choices[0].message.content)
