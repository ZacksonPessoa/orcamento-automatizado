from sqlalchemy import Column, String, DateTime, Text
from sqlalchemy.sql import func
from db import Base
import uuid

class QuoteRequest(Base):
    __tablename__ = "quote_requests"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    status = Column(String, default="RECEIVED")  # RECEIVED | PROCESSING | DONE | ERROR
    file_path = Column(String, nullable=False)
    ocr_text = Column(Text, nullable=True)
    extracted_json = Column(Text, nullable=True)  # JSON string
    quote_json = Column(Text, nullable=True)      # JSON string
    error = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())