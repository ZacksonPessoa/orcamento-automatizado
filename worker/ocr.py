from pathlib import Path
from typing import Optional


def extract_text(image_path: str) -> Optional[str]:
    """Extrai texto de imagem/PDF usando OCR (placeholder)."""
    path = Path(image_path)
    if not path.exists():
        return None
    # TODO: integrar pytesseract ou outro OCR
    return ""
