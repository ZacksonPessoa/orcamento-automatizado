def build_quote(extracted: dict) -> dict:
    # Protótipo: ainda sem seu banco real.
    # Aqui vamos plugar a consulta no seu banco e regras.
    return {
        "currency": "BRL",
        "total": 0.0,
        "notes": "Protótipo: motor de preço será conectado ao banco.",
        "confidence": extracted.get("confidence", 0.0),
        "items": extracted.get("items", []),
    }