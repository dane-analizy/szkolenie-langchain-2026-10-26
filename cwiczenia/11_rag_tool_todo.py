from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain.chat_models import init_chat_model
from langchain_chroma import Chroma
from langchain_core.tools import create_retriever_tool
from langchain_openai import OpenAIEmbeddings

load_dotenv()

# Baza wiedzy o literaturze z Wolnych Lektur
cytaty = [
    "Mędrca szkiełko i oko silniej mówi do mnie niż czucie i wiara. Miej serce i patrzaj w serce! (Adam Mickiewicz, Romantyczność)",
    "Praca organiczna, nauka i rozwój techniki to jedyna droga ocalenia dla społeczeństwa. (Bolesław Prus, Lalka)",
    "Miałeś, chamie, złoty róg, ostał ci się ino sznur. Naród uśpiony czeka na cud. (Stanisław Wyspiański, Wesele)"
]

# Indeksacja w FAISS
embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
vectorstore = Chroma.from_texts(cytaty, embeddings)
retriever = vectorstore.as_retriever(search_kwargs={"k": 1})

# TODO: Skonfiguruj narzędzie za pomocą create_retriever_tool:
# - retriever: nasz obiekt retriever
# - name: "szukaj_cytatow"
# - description: "Wyszukuje motywy filozoficzne i cytaty z lektur (Mickiewicz, Prus, Wyspiański)."
narzedzie_rag = create_retriever_tool() # <-- UZUPEŁNIJ

model = init_chat_model("gpt-4o-mini", temperature=0.1)
agent = create_agent(model=model, tools=[narzedzie_rag])

pytanie = "Co według Wyspiańskiego ostało się z polskiego zrywu narodowego?"
print(f"User: {pytanie}\n")

res = agent.invoke({"messages": [{"role": "user", "content": pytanie}]})
print("Bot:", res["messages"][-1].content)
