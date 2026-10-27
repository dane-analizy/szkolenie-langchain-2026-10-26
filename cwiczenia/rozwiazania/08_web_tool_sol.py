from ddgs import DDGS
from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain.chat_models import init_chat_model
from langchain.tools import tool

load_dotenv()


@tool
def szukaj_w_internecie(query: str) -> str:
    """Wyszukuje bieżące informacje i aktualności w wyszukiwarce DuckDuckGo."""
    with DDGS() as ddgs:
        wyniki = list(ddgs.text(query, max_results=2))
        if not wyniki:
            return "Brak wyników."
        return "\n\n".join([f"{r.get('title')}: {r.get('body')}" for r in wyniki])


model = init_chat_model("gpt-4o-mini", temperature=0.0)

agent = create_agent(
    model=model,
    tools=[szukaj_w_internecie],
    system_prompt="Jesteś pomocnym asystentem. Korzystaj z wyszukiwarki do odpowiadania na pytania o świeże fakty.",
)

pytanie = "Kto wygrał Oscara za najlepszy film w 2026 roku?"
print(f"User: {pytanie}\n")

res = agent.invoke({"messages": [{"role": "user", "content": pytanie}]})
print("Bot:", res["messages"][-1].content)
