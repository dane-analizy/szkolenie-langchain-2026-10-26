from ddgs import DDGS

zapytanie = "Jakie filmy będą w kinach na Halloween?"

with DDGS() as ddgs:
    wyniki = list(ddgs.text(zapytanie, max_results=3))
    for r in wyniki:
        print(f"{r['title']}: {r['body']}")
        print("-------")
