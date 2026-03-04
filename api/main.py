import os, json, uuid
from fastapi import FastAPI, UploadFile, File, HTTPException
from sqlalchemy.orm import Session
from db import Base, engine, SessionLocal
from models import QuoteRequest

from redis import Redis
from rq import Queue

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Orçamento Automatizado - Protótipo")

redis_conn = Redis.from_url(os.getenv("REDIS_URL"))
q = Queue("quotes", connection=redis_conn)

UPLOAD_DIR = os.getenv("UPLOAD_DIR", "/data/uploads")

def db_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/upload")
async def upload_receita(file: UploadFile = File(...)):
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    ext = os.path.splitext(file.filename or "")[1].lower()
    if ext not in [".jpg", ".jpeg", ".png", ".pdf"]:
        raise HTTPException(400, "Envie JPG/PNG/PDF")

    req_id = str(uuid.uuid4())
    path = os.path.join(UPLOAD_DIR, f"{req_id}{ext}")

    with open(path, "wb") as f:
        f.write(await file.read())

    db = SessionLocal()
    qr = QuoteRequest(id=req_id, file_path=path, status="RECEIVED")
    db.add(qr)
    db.commit()
    db.close()

    # Enfileira processamento
    q.enqueue("worker.process_quote", req_id)

    return {"id": req_id, "status": "RECEIVED"}

@app.get("/status/{req_id}")
def status(req_id: str):
    db = SessionLocal()
    qr = db.get(QuoteRequest, req_id)
    db.close()
    if not qr:
        raise HTTPException(404, "Não encontrado")
    return {"id": qr.id, "status": qr.status, "error": qr.error}

@app.get("/result/{req_id}")
def result(req_id: str):
    db = SessionLocal()
    qr = db.get(QuoteRequest, req_id)
    db.close()
    if not qr:
        raise HTTPException(404, "Não encontrado")
    if qr.status != "DONE":
        raise HTTPException(400, f"Ainda não pronto (status={qr.status})")
    return {
        "id": qr.id,
        "ocr_text": qr.ocr_text,
        "extracted": json.loads(qr.extracted_json or "{}"),
        "quote": json.loads(qr.quote_json or "{}"),
    }