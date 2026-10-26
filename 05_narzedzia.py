import json

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI()


# 1. Fizyczne funkcje w Pythonie (Narzędzia)
def read_file(filepath: str) -> str:
    """Odczytuje treść wskazanego pliku z dysku."""
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        return f"Błąd odczytu pliku: {e}"


def write_file(filepath: str, content: str) -> str:
    """Zapisuje treść do wskazanego pliku na dysku."""
    try:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        return f"Pomyślnie zapisano {len(content)} znaków do pliku '{filepath}'."
    except Exception as e:
        return f"Błąd zapisu pliku: {e}"


def dodaj_liczby(liczba_a: float, liczba_b: float) -> float:
    """Dodaje dwie liczby zmiennoprzecinkowe do siebie."""
    return liczba_a + liczba_b


AVAILABLE_TOOLS = {
    "czytaj_plik": read_file,
    "write_file": write_file,
    "dodaj_liczby": dodaj_liczby,
}

# 2. Definicja schematu narzędzi (JSON Schema)
tools_schema = [
    {
        "type": "function",  # Narzędzie jest udostępniane modelowi jako funkcja.
        "function": {
            "name": "czytaj_plik",  # Nazwa, której model użyje, aby zażądać wywołania narzędzia.
            "description": "Odczytuje zawartość wskazanego pliku tekstowego z dysku.",  # Podpowiada modelowi, do czego służy narzędzie.
            "parameters": {  # Opis argumentów, które model ma przekazać do funkcji.
                "type": "object",  # Argumenty są przekazywane jako obiekt.
                "properties": {
                    "filepath": {"type": "string", "description": "Ścieżka do pliku"}
                },  # filepath to tekstowa ścieżka do odczytywanego pliku.
                "required": [
                    "filepath"
                ],  # Wymaga podania ścieżki przy każdym wywołaniu.
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "write_file",
            "description": "Zapisuje wskazaną treść do pliku na dysku.",
            "parameters": {
                "type": "object",
                "properties": {
                    "filepath": {
                        "type": "string",
                        "description": "Ścieżka docelowa pliku",
                    },
                    "content": {"type": "string", "description": "Treść do zapisania"},
                },
                "required": ["filepath", "content"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "dodaj_liczby",
            "description": "Dodaje do siebie dwie liczby.",
            "parameters": {
                "type": "object",  # Argumenty funkcji są przekazywane jako obiekt.
                "properties": {
                    "liczba_a": {
                        "type": "number",
                        "description": "Pierwsza liczba",
                    },  # Pierwszy składnik dodawania.
                    "liczba_b": {
                        "type": "number",
                        "description": "Druga liczba",
                    },  # Drugi składnik dodawania.
                },
                "required": [
                    "liczba_a",
                    "liczba_b",
                ],  # Model musi przekazać oba składniki.
            },
        },
    },
]

# 3. Pierwsze wywołanie modelu z promptem i narzędziami
messages = [
    {
        "role": "system",
        "content": "Jesteś asystentem systemowym z dostępem do narzędzi.",
    },
    {
        "role": "user",
        "content": (
            # "Stwórz plik 'repertuar.txt' i wpisz do niego listę 3 seansów kinowych na dziś. "
            "Użyj też narzędzia dodaj_liczby, aby obliczyć sumę liczb 12.5 oraz -7.5."
            "Przeczytaj jakie seanse zostały zapisane w pliku 'repertuar.txt' i podaj mi ich listę."
        ),
    },
]

print("Wysyłam zapytanie do modelu z deklaracją narzędzi plikowych...")
response = client.chat.completions.create(
    model="gpt-4o-mini", messages=messages, tools=tools_schema
)

choice = response.choices[0]
print(f"Status finish_reason: {choice.finish_reason}")
print(f"Tokeny: {response.usage.total_tokens}")

# 4. Sprawdzenie, czy model zażądał wywołania narzędzia
if choice.finish_reason == "tool_calls":
    # Odpowiadamy na każde wywołanie, jeśli model poprosi o kilka narzędzi naraz.
    messages.append(choice.message)  # Asystent deklaruje wywołania narzędzi
    for tool_call in choice.message.tool_calls:
        func_name = tool_call.function.name
        func_args = json.loads(tool_call.function.arguments)

        print(f"\nModel zażądał uruchomienia: {func_name}({func_args})")

        # Fizyczne uruchomienie funkcji w środowisku Pythona
        if func_name in AVAILABLE_TOOLS:
            result = AVAILABLE_TOOLS[func_name](**func_args)
        else:
            result = f"Błąd: Nieznane narzędzie {func_name}"

        print(f"Wynik wykonania narzędzia w Pythonie: {result}")

        # Wynik narzędzia musi zostać odesłany jako tekst.
        messages.append(
            {"role": "tool", "tool_call_id": tool_call.id, "content": str(result)}
        )

    # Drugie wywołanie – model formułuje końcową odpowiedź dla użytkownika
    print("\nOdsyłam wynik do modelu, aby sformułował odpowiedź końcową...")
    final_response = client.chat.completions.create(
        model="gpt-4o-mini", messages=messages
    )

    print("\n--- Ostateczna odpowiedź modelu ---")
    print(final_response.choices[0].message.content)
    print(f"Tokeny: {final_response.usage.total_tokens}")
