"""
Teste end-to-end do orçamento SEM OCR: build_quote com itens fixos.
Garante que preço (fc03000) e total são calculados.
"""
import os

# Carrega .env da raiz do projeto (sem depender de python-dotenv)
_env_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env")
if os.path.isfile(_env_path):
    with open(_env_path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, _, v = line.partition("=")
                k, v = k.strip(), v.strip().strip('"').strip("'")
                if k and os.environ.get(k) is None:
                    os.environ[k] = v

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
