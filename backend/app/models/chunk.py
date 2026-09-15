from sqlalchemy import Column, Integer, String, ForeignKey, Text
from pgvector.sqlalchemy import Vector
from app.database import Base


class DocumentChunk(Base):
    __tablename__ = "document_chunks"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    document_id = Column(Integer, ForeignKey("documents.id", ondelete="CASCADE"), nullable=False, index=True)
    page_number = Column(Integer, nullable=True)  # Nullable for TXT files
    text_content = Column(Text, nullable=False)
    
    # Gemini text-embedding-004 outputs 768 dimensions
    embedding = Column(Vector(768), nullable=False)
