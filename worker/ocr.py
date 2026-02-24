import os

def run_ocr(file_path: str) -> str:
    provider = os.getenv("OCR_PROVIDER", "google").lower()

    if provider == "google":
        return _google_vision(file_path)
    if provider == "aws":
        return _aws_textract(file_path)
    return _tesseract(file_path)

def _google_vision(file_path: str) -> str:
    from google.cloud import vision
    client = vision.ImageAnnotatorClient()

    with open(file_path, "rb") as f:
        content = f.read()

    image = vision.Image(content=content)
    resp = client.document_text_detection(image=image)
    if resp.error.message:
        raise RuntimeError(resp.error.message)
    return resp.full_text_annotation.text or ""

def _aws_textract(file_path: str) -> str:
    import boto3  # type: ignore[reportMissingImports]
    client = boto3.client("textract", region_name=os.getenv("AWS_REGION", "us-east-1"))
    with open(file_path, "rb") as f:
        bytes_data = f.read()

    resp = client.detect_document_text(Document={"Bytes": bytes_data})
    lines = []
    for b in resp.get("Blocks", []):
        if b.get("BlockType") == "LINE":
            lines.append(b.get("Text", ""))
    return "\n".join(lines)

def _tesseract(file_path: str) -> str:
    import subprocess
    # protótipo: só imagem; PDF exigiria conversão (pdf2image)
    cmd = ["tesseract", file_path, "stdout", "-l", "por"]
    p = subprocess.run(cmd, capture_output=True, text=True)
    if p.returncode != 0:
        raise RuntimeError(p.stderr)
    return p.stdout