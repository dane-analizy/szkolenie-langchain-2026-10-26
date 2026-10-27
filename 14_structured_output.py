import os
import uuid
from datetime import datetime
from typing import Literal

from dotenv import load_dotenv
from langchain.chat_models import init_chat_model

from pydantic import BaseModel, Field

from agent_tools import szukaj_filmow_gatunku

load_dotenv()


# 1. Definicja ustrukturyzowanego schematu Pydantic
class FilmRekomendacja(BaseModel):
    tytul: str = Field(description="Tytuł rekomendowanego filmu")
    rezyser: str = Field(description="Reżyser rekomendowanego filmu")
    premiera: str = Field(description="Rok premiery rekomendowanego filmu")
    gatunek: str = Field(description="Gatunek filmu")
    ocena: float = Field(
        description="Ocena filmu w skali 1-10",
        ge=1,
        le=10,
    )
    uzasadnienie: str = Field(description="Dlaczego ten film warto obejrzeć", max_length=80)
    kategoria: Literal["Klasyk", "Blockbuster", "Ambitne"] = Field(
        description="Kategoria filmu"
    )
    


class RaportKinowy(BaseModel):
    profil_widza: str = Field(description="Profil odbiorcy rekomendacji")
    propozycje: list[FilmRekomendacja] = Field(
        description="Lista rekomendowanych filmów"
    )
    podsumowanie: str = Field(description="Krótkie podsumowanie trendu")


# 2. Inicjalizacja modelu z wymuszeniem struktury wyjścia Pydantic
model = init_chat_model("gpt-4o-mini", temperature=0.1)
structured_model = model.with_structured_output(RaportKinowy)


# Konfiguracja sesji z trackingiem w LangSmith
user_login = os.getenv("USER", "kursant_sages")
session_id = f"warsztat_{user_login}_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{uuid.uuid4().hex[:6]}"
config = {
    "configurable": {"thread_id": session_id},
    "metadata": {"session_id": session_id, "user": user_login},
    "tags": ["warsztat", "langchain-agent"],
}


# 3. Pobranie danych z bazy filmów
filmy_scifi = szukaj_filmow_gatunku.invoke({"nazwa_gatunku": "Sci-Fi"})

print("Wyjście z toola szukaj_filmow_gatunku (przykładowe dane):")
print(filmy_scifi)

prompt = (
    f"Oto lista filmów z naszej bazy: {filmy_scifi}. "
    f"Przygotuj profesjonalny raport rekomendacyjny dla miłośnika ambitnych widowisk science-fiction."
)

print("Wysyłam zapytanie do modelu ze schematem Pydantic (with_structured_output)...\n")

raport: RaportKinowy = structured_model.invoke(prompt, config=config)

# 4. Odbiór w 100% zwalidowanego obiektu Pydantic!
print("--- Wynik jako zwalidowany obiekt Pydantic ---")
print(f"Profil widza: {raport.profil_widza}")
print(f"Liczba propozycji: {len(raport.propozycje)}")


for f in raport.propozycje:
    print(
        f"\n{f.tytul} [{f.kategoria} z {f.premiera}, reż.: {f.rezyser}] - Ocena: {f.ocena}/10"
    )
    print(f"Uzasadnienie: {f.uzasadnienie}")

print(f"\nPodsumowanie: {raport.podsumowanie}")

# Zrzut do czystego JSON gotowego do wysłania przez REST API
print("\n--- JSON wygenerowany przez Pydantic ---")
print(raport.model_dump_json(indent=2))
