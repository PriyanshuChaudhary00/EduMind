import os
import re
from typing import List, Dict
from pypdf import PdfReader
from docx import Document as DocxDocument
from google import genai
from sqlalchemy.orm import Session
from app.config import settings
from app.models.document import Document, DocumentStatus
from app.models.chunk import DocumentChunk
from app.database import SessionLocal


def extract_text_from_file(file_path: str, content_type: str) -> List[Dict]:
    """
    Extracts text from a file and returns a list of dictionaries:
    [{"page": 1, "text": "content..."}, ...]
    """
    pages = []
    
    if content_type == "application/pdf":
        reader = PdfReader(file_path)
        for i, page in enumerate(reader.pages):
            text = page.extract_text()
            if text:
                pages.append({"page": i + 1, "text": text})
                
    elif content_type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        doc = DocxDocument(file_path)
        full_text = []
        for para in doc.paragraphs:
            full_text.append(para.text)
        # For docx, we don't have true pages, so we treat it as 1 page
        pages.append({"page": 1, "text": "\\n".join(full_text)})
        
    elif content_type == "text/plain":
        with open(file_path, "r", encoding="utf-8") as f:
            text = f.read()
            pages.append({"page": 1, "text": text})
            
    return pages


def chunk_text(pages: List[Dict], chunk_size: int = 500, overlap: int = 50) -> List[Dict]:
    """
    Splits text into chunks of roughly `chunk_size` words with `overlap` words.
    Returns list of dicts with text and page numbers.
    """
    chunks = []
    for p in pages:
        page_num = p["page"]
        text = p["text"]
        
        # Clean text
        text = re.sub(r'\\s+', ' ', text).strip()
        words = text.split()
        
        if not words:
            continue
            
        i = 0
        while i < len(words):
            chunk_words = words[i:i + chunk_size]
            chunk_text = " ".join(chunk_words)
            chunks.append({
                "page": page_num,
                "text": chunk_text
            })
            i += chunk_size - overlap
            
    return chunks


def process_document(document_id: int):
    """
    Background task to process a document: extract text, chunk, embed, save to DB.
    """
    db: Session = SessionLocal()
    
    # Get document
    document = db.query(Document).filter(Document.id == document_id).first()
    if not document:
        db.close()
        return

    try:
        # 1. Update status
        document.status = DocumentStatus.PROCESSING
        db.commit()

        # 2. Extract Text
        pages = extract_text_from_file(document.file_path, document.content_type)
        
        # 3. Chunk Text
        chunks = chunk_text(pages, chunk_size=settings.CHUNK_SIZE, overlap=settings.CHUNK_OVERLAP)
        
        if not chunks:
            raise ValueError("No extractable text found in document.")

        # 4. Initialize Gemini Client
        client = genai.Client(api_key=settings.GEMINI_API_KEY)
        
        # 5. Embed and Save chunks
        for chunk in chunks:
            # Generate embedding using the recommended model for embeddings
            response = client.models.embed_content(
                model="text-embedding-004",
                contents=chunk["text"]
            )
            embedding_vector = response.embeddings[0].values
            
            # Save to DB
            db_chunk = DocumentChunk(
                document_id=document.id,
                page_number=chunk["page"],
                text_content=chunk["text"],
                embedding=embedding_vector
            )
            db.add(db_chunk)
            
        # 6. Finalize
        document.status = DocumentStatus.READY
        db.commit()

    except Exception as e:
        print(f"Error processing document {document_id}: {str(e)}")
        db.rollback()
        # Mark document as error
        # Need to fetch it again in case session is rolled back
        error_doc = db.query(Document).filter(Document.id == document_id).first()
        if error_doc:
            error_doc.status = DocumentStatus.ERROR
            db.commit()
    finally:
        db.close()
