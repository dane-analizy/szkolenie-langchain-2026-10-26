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
        
    if tekst.lower() == "/new":
        conversation = [SYSTEM_MSG]
        print("Pamięć wyczyszczona!\n")
        continue

    conversation.append({"role": "user", "content": tekst})
    
    res = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=conversation
    )
    odpowiedz = res.choices[0].message
    print(f"Bot > {odpowiedz.content}\n")
    
    conversation.append(odpowiedz)
