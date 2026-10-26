import json

from dotenv import load_dotenv
from openai import OpenAI

from domain_tools import pobierz_szczegoly_filmu, szukaj_filmow_gatunku

load_dotenv()
client = OpenAI()

AVAILABLE_TOOLS = {
    "szukaj_filmow_gatunku": szukaj_filmow_gatunku,
    "pobierz_szczegoly_filmu": pobierz_szczegoly_filmu,
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
                    "nazwa_gatunku": {
                        "type": "string",
                        "description": "Nazwa gatunku filmowego",
                    }
                },
                "required": ["nazwa_gatunku"],
            },
        },
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
                "required": ["tytul"],
            },
        },
    },
]


def run_single_task(user_prompt: str) -> str:
    """Obsługuje JEDNO zapytanie. Po wyjściu z funkcji tablica messages znika (brak stanu)!"""
    messages = [
        {
            "role": "system",
            "content": "Jesteś asystentem kinowym. Korzystaj z narzędzi, aby odpowiadać na pytania.",
        },
        {"role": "user", "content": user_prompt},
    ]

    while True:
        response = client.chat.completions.create(
            model="gpt-4o-mini", messages=messages, tools=tools_schema
        )
        choice = response.choices[0]

        if choice.finish_reason != "tool_calls":
            return choice.message.content

        messages.append(choice.message)
        for tool_call in choice.message.tool_calls:
            fn_name = tool_call.function.name
            fn_args = json.loads(tool_call.function.arguments)
            print(f"[Tool] Wywołuję: {fn_name}({fn_args})")

            result = AVAILABLE_TOOLS[fn_name](**fn_args)
            print(f"[Tool] Wynik: {result}")
            messages.append(
                {
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": json.dumps(result, ensure_ascii=False),
                }
            )


if __name__ == "__main__":
    print("Agent Bezstanowy (Brak Pamięci). Wpisz 'exit' aby wyjść.")
    print("Przetestuj:")
    print("1. Kto wyreżyserował film Diuna?")
    print("2. A kto w nim zagrał? (zobaczysz, że model zapomni o jaki film pytasz!)")

    while True:
        prompt = input("\nTy > ").strip()
        if not prompt or prompt.lower() == "exit":
            break
        odpowiedz = run_single_task(prompt)
        print(f"Bot > {odpowiedz}")
