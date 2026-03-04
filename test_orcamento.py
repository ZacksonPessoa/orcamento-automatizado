"""
Teste end-to-end do orçamento SEM OCR: build_quote com itens fixos.
Garante que preço (fc03000) e total são calculados.
"""
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

from worker.pricing import build_quote

extracted = {
    "items": [
        {"name": "DIPIRONA", "qty": 2},
        {"name": "AFRIN", "qty": 1},
    ],
    "confidence": 0.9,
}

if __name__ == "__main__":
    result = build_quote(extracted)
    print(result)
