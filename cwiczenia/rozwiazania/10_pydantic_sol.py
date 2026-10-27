from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from pydantic import BaseModel, Field

load_dotenv()


class RekomendacjaKina(BaseModel):
    tytul: str = Field(description="Tytuł rekomendowanego filmu")
    ocena_w_skali_10: float = Field(ge=1.0, le=10.0, description="Ocena filmu")
    gatunek: str = Field(description="Główny gatunek")
    dlaczego_warto: str = Field(description="Jednozdaniowe uzasadnienie")


model = init_chat_model("gpt-4o-mini", temperature=0.1)
structured_model = model.with_structured_output(RekomendacjaKina)

wynik: RekomendacjaKina = structured_model.invoke("Poleć jeden wybitny film science-fiction.")

print(f"Tytuł: {wynik.tytul} ({wynik.gatunek})")
print(f"Ocena: {wynik.ocena_w_skali_10}/10")
print(f"Uzasadnienie: {wynik.dlaczego_warto}")
print("\nZrzut do czystego JSON:\n", wynik.model_dump_json(indent=2))
