import os

from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain.chat_models import init_chat_model
from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_core.tools import create_retriever_tool
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

load_dotenv()

# 1. Przygotowanie reprezentatywnych tekstów literackich z Wolnych Lektur
DOKUMENTY = {
    "mickiewicz_romantycznosc.txt": (
        "Mędrca szkiełko i oko silniej mówi do mnie niż czucie i wiara. "
        "Dziewczyna krzyczy: 'Umarł! Ach, zginął na wieki!'. Martwe znasz prawdy, nieznane dla ludu, "
        "Widzisz świat w proszku, nie znasz żywych cudów. Miej serce i patrzaj w serce!"
    ),
    "prus_lalka_paryz.txt": (
        "Wokulski spacerował po bulwarach Paryża. Widział miasto jak potężną machinę cywilizacji. "
        "Zrozumiał, że praca organiczna, nauka i technika to jedyna droga rozwoju społeczeństwa, "
        "podczas gdy polska arystokracja marnuje siły na puste bale i pozory."
    ),
    "wyspianski_wesele.txt": (
        "Miałeś, chamie, złoty róg, ostał ci się ino sznur. "
        "Chochoł gra, a wszyscy tańczą w lunatycznym uśpieniu. Społeczeństwo niezdolne do czynu "
        "czeka na cud, gubiąc swoje szanse na wolność."
    ),
}

os.makedirs("lektury", exist_ok=True)
for nazwa, tresc in DOKUMENTY.items():
    sciezka = os.path.join("lektury", nazwa)
    with open(sciezka, "w", encoding="utf-8") as f:
        f.write(tresc)

print("Zapisano teksty literackie do katalogu lektury/.")

# 2. Załadowanie i podział na fragmenty (Chunking)
docs = []
for nazwa in DOKUMENTY:
    sciezka = os.path.join("lektury", nazwa)
    with open(sciezka, "r", encoding="utf-8") as f:
        text = f.read()
    docs.append(Document(page_content=text, metadata={"source": sciezka}))

splitter = RecursiveCharacterTextSplitter(chunk_size=180, chunk_overlap=30)
chunks = splitter.split_documents(docs)
print(f"Podzielono teksty na {len(chunks)} fragmentów (chunks).")
print(f"Przykładowy chunk 0: '{chunks[0].page_content}'")
print(f"Metadata chunk 0: {chunks[0].metadata}")
print(f"Przykładowy chunk 1: '{chunks[1].page_content}'")
print(f"Metadata chunk 1: {chunks[1].metadata}")

# 3. Wektoryzacja w lokalnej bazie FAISS
print("Generuję embeddingi i indeksuję w lokalnej bazie wektorowej Chroma...")
embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
vectorstore = Chroma.from_documents(chunks, embeddings)
retriever = vectorstore.as_retriever(search_kwargs={"k": 2})

# 4. Przekształcenie bazy wektorowej w narzędzie dla agenta (create_retriever_tool)
tool_literacki = create_retriever_tool(
    retriever=retriever,
    name="szukaj_w_literaturze",
    description="Wyszukuje motywy filozoficzne, cytaty i fragmenty dzieł literackich (Mickiewicz, Prus, Wyspiański).",
)

# 5. Agent łączący RAG z modelem LLM
model = init_chat_model("gpt-4o-mini", temperature=0.1)
agent = create_agent(
    model=model,
    tools=[tool_literacki],
    system_prompt="Jesteś kulturoznawcą i analitykiem literatury. W swoich odpowiedziach zawsze powołuj się na cytaty z literatury i używaj narzędzia szukaj_w_literaturze.",
)

pytanie = "Czym różni się romantyczne spojrzenie na świat u Mickiewicza od pozytywistycznego podejścia Wokulskiego?"
print(f"\nUser: {pytanie}\n")

res = agent.invoke({"messages": [{"role": "user", "content": pytanie}]})
print("Bot (RAG):")
print(res["messages"][-1].content)
