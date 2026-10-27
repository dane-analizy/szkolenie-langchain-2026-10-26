from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
from langchain_core.tools import create_retriever_tool
from langchain.chat_models import init_chat_model
from langchain.agents import create_agent

load_dotenv()

cytaty = [
    "Mędrca szkiełko i oko silniej mówi do mnie niż czucie i wiara. Miej serce i patrzaj w serce! (Adam Mickiewicz, Romantyczność)",
    "Praca organiczna, nauka i rozwój techniki to jedyna droga ocalenia dla społeczeństwa. (Bolesław Prus, Lalka)",
    "Miałeś, chamie, złoty róg, ostał ci się ino sznur. Naród uśpiony czeka na cud. (Stanisław Wyspiański, Wesele)"
]

embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
vectorstore = Chroma.from_texts(cytaty, embeddings)
retriever = vectorstore.as_retriever(search_kwargs={"k": 1})

narzedzie_rag = create_retriever_tool(
    retriever=retriever,
    name="szukaj_cytatow",
    description="Wyszukuje motywy filozoficzne i cytaty z lektur (Mickiewicz, Prus, Wyspiański)."
)

model = init_chat_model("gpt-4o-mini", temperature=0.1)
agent = create_agent(model=model, tools=[narzedzie_rag])

pytanie = "Co według Wyspiańskiego ostało się z polskiego zrywu narodowego?"
print(f"User: {pytanie}\n")

res = agent.invoke({"messages": [{"role": "user", "content": pytanie}]})
print("Bot:", res["messages"][-1].content)
