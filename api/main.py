from fastapi import FastAPI
from db import init_db

app = FastAPI(title="Orçamento Automatizado API")


@app.on_event("startup")
async def startup():
    init_db()


@app.get("/health")
def health():
    return {"status": "ok"}
