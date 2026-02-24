import os
from ocr import extract_text
from pricing import process_pricing

# Placeholder: conectar a fila (Redis/Celery) e processar jobs
if __name__ == "__main__":
    print("Worker started. OCR and pricing modules loaded.")
