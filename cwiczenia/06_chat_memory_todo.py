from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI()

SYSTEM_MSG = {"role": "system", "content": "Jesteś zwięzłym doradcą filmowym. Pamiętasz wcześniejsze wypowiedzi."}
conversation = [SYSTEM_MSG]

print("Start czatu. Wpisz '/new' aby zresetować pamięć, 'exit' aby wyjść.\n")

while True:
    tekst = input("Ty > ").strip()
    if not tekst or tekst.lower() == "exit":
        break
        
    # TODO 1: Obsłuż komendę '/new' - zresetuj listę 'conversation' tak, by zawierała TYLKO SYSTEM_MSG
    if tekst.lower() == "/new":
        conversation = # <-- UZUPEŁNIJ
        print("Pamięć wyczyszczona!\n")
        continue

    # TODO 2: Dodaj zapytanie użytkownika do historii rozmowy
    conversation.append()  # <-- UZUPEŁNIJ
    
    res = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=conversation
    )
    odpowiedz = res.choices[0].message
    print(f"Bot > {odpowiedz.content}\n")
    
    # TODO 3: Zapisz odpowiedź modelu w historii rozmowy, aby pamiętał ją w kolejnym kroku!
    conversation.append()  # <-- UZUPEŁNIJ
