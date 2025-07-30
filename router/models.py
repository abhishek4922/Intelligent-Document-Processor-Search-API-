from sqlalchemy import Column, Integer, String, JSON
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, nullable=False)
    document_type = Column(String, nullable=False)
    extracted_metadata = Column(JSON)  # ✅ renamed, safe to use
