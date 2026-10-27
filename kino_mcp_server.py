import sqlite3

from mcp.server.fastmcp import FastMCP

# 1. Inicjalizacja serwera MCP
mcp = FastMCP("Kino-Analytics-Server")


# 2. Definicja narzędzia: Wyszukiwanie filmów w SQLite
@mcp.tool()
def szukaj_filmow(gatunek: str) -> str:
    """Wyszukuje filmy w bazie SQLite na podstawie gatunku (np. Sci-Fi, Komedia)."""
    conn = sqlite3.connect("filmy.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    query = """
        SELECT f.tytul, f.data_premiery, f.ocena_filmweb, f.liczba_glosow, g.nazwa_gatunku
        FROM fakt_filmy f
        JOIN wymiar_gatunki g ON f.id_gatunku = g.id_gatunku
        WHERE LOWER(g.nazwa_gatunku) = LOWER(?)
        ORDER BY f.ocena_filmweb DESC NULLS LAST
        LIMIT 10;
    """
    cursor.execute(query, (gatunek,))
    wyniki = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return str(wyniki) if wyniki else "Brak filmów w tym gatunku."


# 3. Definicja narzędzia: Kalkulator rentowności ROI
@mcp.tool()
def oblicz_roi(przychody_pln: float, koszty_pln: float) -> str:
    """Oblicza wskaźnik ROI oraz zysk netto filmu w PLN na podstawie przychodów i kosztów."""
    if koszty_pln <= 0:
        return "Błąd: Koszty muszą być większe od zera."
    zysk = przychody_pln - koszty_pln
    roi = (zysk / koszty_pln) * 100
    return f"Zysk netto: {zysk:,.2f} PLN | Wskaźnik ROI: {roi:.2f}%"


if __name__ == "__main__":
    # Uruchomienie w standardowym, bezpiecznym trybie stdio dla klientów MCP (VSCode, Cursor, Claude Desktop)
    mcp.run()
