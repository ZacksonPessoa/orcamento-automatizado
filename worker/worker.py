import os, json, re
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from ocr import run_ocr
from pricing import build_quote

DATABASE_URL = os.getenv("DATABASE_URL")


def _extrair_itens_do_texto(text: str) -> list:
    """
    Extrai itens de texto (OCR ou .txt): cada linha = nome (+ opcional qty no final).
    Ex.: "DIPIRONA 500MG 30" -> name DIPIRONA 500MG, qty 30; "CAFEÍNA" -> qty 1.
    """
    items = []
    for line in (text or "").splitlines():
        line = line.strip()
        if not line:
            continue
        m = re.match(r"^(.+?)\s+(\d+)\s*$", line)
        if m:
            name, qty = m.group(1).strip(), int(m.group(2))
            if name:
                items.append({"name": name, "qty": max(1, qty)})
        else:
            items.append({"name": line, "qty": 1})
    return items


def _extrair_itens_do_ocr(text: str) -> list:
    """Extrai itens do texto (OCR ou .txt). Fallback TXT usa _extrair_itens_do_texto."""
    return _extrair_itens_do_texto(text)


engine = create_engine(DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

def process_quote(req_id: str):
    from api.models import QuoteRequest  # import tardio para evitar circularidade

    db = SessionLocal()
    qr = db.get(QuoteRequest, req_id)
    if not qr:
        db.close()
        return

    try:
        qr.status = "PROCESSING"
        db.commit()

        file_path = qr.file_path or ""
        if file_path.lower().endswith(".txt"):
            with open(file_path, encoding="utf-8", errors="replace") as f:
                text = f.read()
        else:
            prev = os.environ.get("OCR_PROVIDER")
            prov = (qr.provider or "auto").strip().lower()
            if prov in ("google", "aws", "tesseract"):
                os.environ["OCR_PROVIDER"] = prov
            try:
                text = run_ocr(file_path)
            finally:
                if prev is not None:
                    os.environ["OCR_PROVIDER"] = prev
                elif prov in ("google", "aws", "tesseract"):
                    os.environ.pop("OCR_PROVIDER", None)

        qr.ocr_text = text

        # Extração: lista de itens com "name" (e opcionalmente "qty") para build_quote
        # buscar preço na fc03000 por descrição (PRVEN)
        extracted = {
            "confidence": 0.6,
            "items": _extrair_itens_do_ocr(text),  # placeholder até parser real
        }

        quote = build_quote(extracted)

        qr.extracted_json = json.dumps(extracted, ensure_ascii=False)
        qr.quote_json = json.dumps(quote, ensure_ascii=False)
        qr.status = "DONE"
        db.commit()

    except Exception as e:
        qr.status = "ERROR"
        qr.error = str(e)
        db.commit()
    finally:
        db.close()