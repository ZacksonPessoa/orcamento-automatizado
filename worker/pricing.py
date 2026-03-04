import re
from firebird_db import query_fc03000_por_descricao


def _normalizar_nome(nome: str, max_chars: int = 25) -> str:
    """Upper, remove múltiplos espaços, limita tamanho (melhor match na fc03000)."""
    s = (nome or "").strip()
    s = re.sub(r"\s+", " ", s).strip()
    s = s.upper()[:max_chars]
    return s


def build_quote(extracted: dict) -> dict:
    """
    Monta orçamento: para cada item extraído do OCR, busca preço na fc03000
    (por descrição), usa PRVEN como preço; primeiro match resolve por enquanto.
    """
    items_raw = extracted.get("items", [])
    confidence = extracted.get("confidence", 0.0)
    items = []
    total = 0.0

    for item in items_raw:
        if isinstance(item, str):
            name = item
            qty = 1
            item_out = {"name": name, "qty": qty}
        else:
            name = item.get("name") or item.get("nome") or ""
            raw_qty = item.get("qty", 1)
            try:
                qty = max(1, int(raw_qty))
            except (TypeError, ValueError):
                qty = 1
            item_out = dict(item)

        item_out["qty"] = qty
        nome_norm = _normalizar_nome(name)
        preco_venda = None
        match_descr = None
        codigo = None

        if nome_norm:
            matches = query_fc03000_por_descricao(nome_norm, limite=5)
            if matches:
                primeiro = matches[0]
                preco_venda = primeiro.get("PRVEN")
                match_descr = primeiro.get("DESCR")
                codigo = primeiro.get("CODIGO")

        item_out["preco_venda"] = preco_venda
        item_out["match_descr"] = match_descr
        item_out["codigo"] = codigo
        if preco_venda is not None:
            total += float(preco_venda) * qty
        items.append(item_out)

    return {
        "currency": "BRL",
        "total": round(total, 2),
        "notes": "Preços da fc03000 (Fcerta); primeiro match por descrição.",
        "confidence": confidence,
        "items": items,
    }