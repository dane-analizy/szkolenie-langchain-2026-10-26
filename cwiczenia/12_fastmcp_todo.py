from mcp.server.fastmcp import FastMCP

# Inicjalizacja serwera FastMCP
mcp = FastMCP("Kino-Kalkulator-Server")

# TODO 1: Udekoruj funkcję dekoratorem @mcp.tool()
@  # <-- UZUPEŁNIJ DEKORATOR
def kalkulator_biletow(liczba_biletow: int, ulgowy: bool = False) -> dict:
    """Oblicza łączną kwotę biletów kinowych oraz podatek VAT 8%."""
    cena = 20.0 if ulgowy else 30.0
    brutto = liczba_biletow * cena
    netto = round(brutto / 1.08, 2)
    return {
        "liczba": liczba_biletow,
        "rodzaj": "Ulgowy" if ulgowy else "Normalny",
        "brutto_pln": brutto,
        "vat_8_pln": round(brutto - netto, 2)
    }

# TODO 2: Uruchom serwer za pomocą mcp.run() w bloku if __name__ == '__main__'
# <-- UZUPEŁNIJ URUCHOMIENIE
