from dotenv import load_dotenv
from ddgs import DDGS
from langchain.chat_models import init_chat_model
from langchain.tools import tool
from langchain.agents import create_agent

load_dotenv()

# TODO 1: Oznacz funkcję dekoratorem i upewnij się, że docstring jest czytelny dla LLM
@ # <-- UZUPEŁNIJ
def szukaj_w_internecie(query: str) -> str:
    """""" # <-- UZUPEŁNIJ
    with DDGS(timeout=15) as ddgs:
        wyniki = list(ddgs.text(query, max_results=2))
        if not wyniki:
            return "Brak wyników."
        return "\n\n".join([f"{r.get('title')}: {r.get('body')}" for r in wyniki])

model = init_chat_model("gpt-4o-mini", temperature=0.0)

# TODO 2: Przekaż zdefiniowane narzędzie do listy 'tools' w agencie
agent = create_agent(
    model=model,
    tools=   # <-- UZUPEŁNIJ
    system_prompt="Jesteś pomocnym asystentem. Korzystaj z wyszukiwarki do odpowiadania na pytania o świeże fakty."
)

pytanie = "Kto wygrał Oscara za najlepszy film w 2026 roku?"
print(f"User: {pytanie}\n")

res = agent.invoke({"messages": [{"role": "user", "content": pytanie}]})
print("Bot:", res["messages"][-1].content)
