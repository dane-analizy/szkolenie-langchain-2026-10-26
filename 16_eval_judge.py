from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from pydantic import BaseModel, Field

load_dotenv()


# Schemat werdyktu sędziowskiego
class WerdyktSedziowski(BaseModel):
    ocena_wiernosci: int = Field(description="Ocena wierności faktom (Faithfulness) w skali 1-5")
    ocena_trafnosci: int = Field(description="Ocena trafności odpowiedzi na pytanie użytkownika (Relevance) w skali 1-5")
    uzasadnienie_krok_po_kroku: str = Field(description="Szczegółowe uzasadnienie werdyktu sędziego (Chain-of-Thought)")
    decyzja: str = Field(description="'ZATWIERDZONA' jeśli obie oceny >= 4, w przeciwnym razie 'ODRZUCONA'")


# Przykładowy scenariusz ewaluacyjny z Golden Dataset
KONTRAKT_TESTOWY = {
    "pytanie": "Kto wyreżyserował film Diuna i jaką ma ocenę na Filmwebie?",
    "kontekst_zrodlowy": "Tytuł: Diuna, Reżyser: Denis Villeneuve, Ocena Filmweb: 7.82, Liczba głosów: 70 022.",
    "odpowiedz_bota_do_oceny": "Film Diuna wyreżyserował Krzysztof Villeneuve. Na portalu Filmweb film uzyskał ocenę 7.9 przy ponad 170 tysiącach głosów.",
}

RUBRYKA_SEDZIOWSKA = """
Jesteś niezależnym sędzią AI (LLM-as-a-Judge). Twoim zadaniem jest ocena jakości odpowiedzi bota produkcyjnego.

Kryteria oceny (skala 1 - 5):
1. Wierność (Faithfulness):
   - 5: Odpowiedź zawiera wyłącznie fakty obecne w kontekście źródłowym. Zero halucynacji.
   - 3: Odpowiedź w większości poprawna, ale dodaje nieistotne spekulacje.
   - 1: Odpowiedź zawiera ewidentne zmyślenia lub zaprzecza kontekstowi źródłowemu.

2. Trafność (Answer Relevance):
   - 5: Odpowiedź precyzyjnie odpowiada na wszystkie człony pytania użytkownika.
   - 3: Odpowiedź odpowiada tylko na część pytania.
   - 1: Odpowiedź całkowicie nie na temat.
"""


def uruchom_ewaluacje():
    judge_model = init_chat_model("gpt-4o-mini", temperature=0.0)
    structured_judge = judge_model.with_structured_output(WerdyktSedziowski)

    prompt = f"""
{RUBRYKA_SEDZIOWSKA}

---
DANE DO OCENY:
Pytanie użytkownika: {KONTRAKT_TESTOWY["pytanie"]}
Kontekst źródłowy: {KONTRAKT_TESTOWY["kontekst_zrodlowy"]}
Odpowiedź bota: {KONTRAKT_TESTOWY["odpowiedz_bota_do_oceny"]}

Oceń odpowiedź zgodnie ze schematem i przedstaw werdykt.
"""

    print("Uruchamiam proces ewaluacji jakości (LLM-as-a-Judge)...\n")
    werdykt: WerdyktSedziowski = structured_judge.invoke(prompt)

    print("--- WERDYKT SĘDZIEGO AI ---")
    print(f"Decyzja: {werdykt.decyzja}")
    print(f"Wierność (Faithfulness): {werdykt.ocena_wiernosci} / 5")
    print(f"Trafność (Relevance):    {werdykt.ocena_trafnosci} / 5")
    print(f"\nUzasadnienie:\n{werdykt.uzasadnienie_krok_po_kroku}")
    print(f"\nJSON:\n{werdykt.model_dump_json(indent=2)}")


if __name__ == "__main__":
    uruchom_ewaluacje()
