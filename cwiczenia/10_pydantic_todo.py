from pydantic import BaseModel, Field
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model

load_dotenv()

# Model danych
class RekomendacjaKina(BaseModel):
    tytul: str = Field(description="Tytuł rekomendowanego filmu")
    ocena_w_skali_10: float = Field(ge=1.0, le=10.0, description="Ocena filmu")
    gatunek: str = Field(description="Główny gatunek")
    dlaczego_warto: str = Field(description="Jednozdaniowe uzasadnienie")

model = init_chat_model("gpt-4o-mini", temperature=0.1)

# TODO 1: Wymuś format odpowiedzi przekazując model Pydantic do with_structured_output
structured_model = model. # <-- UZUPEŁNIJ

# Wywołanie modelu
wynik: RekomendacjaKina = structured_model. # <-- UZUPEŁNIJ

# TODO 2: Wypisz zwalidowany obiekt
print("\nZrzut do czystego JSON:\n", wynik.model_dump_json(indent=2))
print(f"Tytuł:...")  # <-- UZUPEŁNIJ
print(f"Ocena:...")  # <-- UZUPEŁNIJ
print(f"Uzasadnienie:...")  # <-- UZUPEŁNIJ
