import os, json
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime

from ocr import run_ocr
from pricing import build_quote

DATABASE_URL = os.getenv("DATABASE_URL")
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

        text = run_ocr(qr.file_path)
        qr.ocr_text = text

        # Extração simplificada (protótipo): placeholder
        extracted = {
            "confidence": 0.6,
            "items": [
                # {"name": "Cafeína", "dose": 200, "unit": "mg", "qty": 30, "form": "caps"}
            ]
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