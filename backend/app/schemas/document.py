from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import List
from app.models.document import DocumentStatus


class DocumentResponse(BaseModel):
    id: int
    filename: str
    content_type: str
    file_size: int
    status: DocumentStatus
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class DocumentListResponse(BaseModel):
    documents: List[DocumentResponse]
    total: int
