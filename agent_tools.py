from langchain.tools import tool

from domain_tools import (
    pobierz_szczegoly_filmu as pobierz_szczegoly_filmu_sql,
    szukaj_filmow_gatunku as szukaj_filmow_gatunku_sql,
)


@tool
def szukaj_filmow_gatunku(nazwa_gatunku: str) -> list[dict]:
    """Wyszukuje filmy w bazie na podstawie nazwy gatunku (np. Sci-Fi, Komedia)."""
    return szukaj_filmow_gatunku_sql(nazwa_gatunku)


@tool
def pobierz_szczegoly_filmu(tytul: str) -> dict:
    """Pobiera szczegóły filmu: twórców, gatunek, ocenę i obsadę aktorską."""
    return pobierz_szczegoly_filmu_sql(tytul)
