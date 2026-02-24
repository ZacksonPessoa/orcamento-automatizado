from typing import Any, Dict, List


def process_pricing(raw_text: str) -> Dict[str, Any]:
    """Processa texto extraído e retorna estrutura de preços (placeholder)."""
    return {
        "items": [],
        "totals": {},
        "raw_text": raw_text,
    }
