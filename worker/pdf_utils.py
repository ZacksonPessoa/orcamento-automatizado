"""
Extração de texto de PDF. MVP: só pypdf (texto selecionável).
PDF escaneado (fallback OCR) pode ser adicionado depois com pdf2image + run_ocr.
"""


def get_text_from_pdf(file_path: str) -> str:
    """
    Extrai texto do PDF com pypdf. Se o PDF for escaneado (sem texto),
    retorna string vazia; fallback OCR pode ser implementado depois.
    """
    try:
        from pypdf import PdfReader
    except ImportError:
        return ""

    try:
        reader = PdfReader(file_path)
        parts = []
        for page in reader.pages:
            t = page.extract_text()
            if t:
                parts.append(t)
        return "\n".join(parts) if parts else ""
    except Exception:
        return ""
