from sqlalchemy import Column, Integer, String, ForeignKey, Text
from pgvector.sqlalchemy import Vector
from app.database import Base


class DocumentChunk(Base):
    __tablename__ = "document_chunks"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    document_id = Column(Integer, ForeignKey("documents.id", ondelete="CASCADE"), nullable=False, index=True)
    page_number = Column(Integer, nullable=True)  # Nullable for TXT files
    text_content = Column(Text, nullable=False)
    
    # 3072 dimensions for gemini-embedding-2
    embedding = Column(Vector(3072), nullable=False)
