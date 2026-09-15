from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import List, Optional


class ChatMessageBase(BaseModel):
    content: str


class ChatMessageCreate(ChatMessageBase):
    pass


class ChatMessageResponse(ChatMessageBase):
    id: int
    role: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class ChatHistoryResponse(BaseModel):
    messages: List[ChatMessageResponse]


class ChatRequest(BaseModel):
    message: str
    # Optional: limit chat to a specific document ID
    document_id: Optional[int] = None
