import os
import uuid
from fastapi import APIRouter, Depends, UploadFile, File, HTTPException, status, BackgroundTasks
from sqlalchemy.orm import Session
from app.database import get_db
from app.utils.dependencies import get_current_user
from app.models.user import User
from app.models.document import Document, DocumentStatus
from app.schemas.document import DocumentResponse, DocumentListResponse
from app.config import settings
from app.services.document_processor import process_document

router = APIRouter()

ALLOWED_MIME_TYPES = {
    "application/pdf": ".pdf",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document": ".docx",
    "text/plain": ".txt",
}

@router.post("/upload", response_model=DocumentResponse, status_code=status.HTTP_201_CREATED)
async def upload_document(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if file.content_type not in ALLOWED_MIME_TYPES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Unsupported file type. Only PDF, DOCX, and TXT are allowed."
        )
    
    # Read file content to check size and save
    file_content = await file.read()
    file_size = len(file_content)
    
    # Check file size (e.g., limit to MAX_FILE_SIZE_MB)
    max_size_bytes = settings.MAX_FILE_SIZE_MB * 1024 * 1024
    if file_size > max_size_bytes:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"File too large. Maximum size is {settings.MAX_FILE_SIZE_MB}MB."
        )
    
    # Ensure upload directory exists
    os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
    
    # Generate unique filename to avoid collisions
    file_ext = ALLOWED_MIME_TYPES[file.content_type]
    unique_filename = f"{uuid.uuid4()}{file_ext}"
    file_path = os.path.join(settings.UPLOAD_DIR, unique_filename)
    
    # Write to disk
    with open(file_path, "wb") as f:
        f.write(file_content)
        
    # Create DB record
    new_doc = Document(
        user_id=current_user.id,
        filename=file.filename or "untitled",
        file_path=file_path,
        content_type=file.content_type,
        file_size=file_size,
        status=DocumentStatus.UPLOADED
    )
    
    db.add(new_doc)
    db.commit()
    db.refresh(new_doc)
    
    # Trigger background processing
    background_tasks.add_task(process_document, new_doc.id)
    
    return new_doc


@router.get("/", response_model=DocumentListResponse)
def list_documents(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    documents = db.query(Document).filter(Document.user_id == current_user.id).order_by(Document.created_at.desc()).all()
    return DocumentListResponse(documents=documents, total=len(documents))


@router.delete("/{document_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_document(
    document_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    document = db.query(Document).filter(Document.id == document_id, Document.user_id == current_user.id).first()
    
    if not document:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document not found or you don't have permission to delete it"
        )
        
    # Delete file from disk
    if os.path.exists(document.file_path):
        try:
            os.remove(document.file_path)
        except OSError as e:
            # We log it but continue deleting the DB record
            print(f"Error removing file {document.file_path}: {e}")
            
    # Delete from DB
    db.delete(document)
    db.commit()
    
    return None
