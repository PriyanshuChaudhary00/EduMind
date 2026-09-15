from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.utils.dependencies import get_current_user
from app.models.user import User
from app.models.document import Document
from app.models.chat import ChatMessage
from pydantic import BaseModel

router = APIRouter()

class DashboardStats(BaseModel):
    documents_count: int
    questions_count: int
    quizzes_count: int
    study_time_hours: int

@router.get("/dashboard", response_model=DashboardStats)
def get_dashboard_stats(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Count user's uploaded documents
    doc_count = db.query(Document).filter(Document.user_id == current_user.id).count()
    
    # Count user's questions (role = user in chat)
    chat_count = db.query(ChatMessage).filter(
        ChatMessage.user_id == current_user.id,
        ChatMessage.role == "user"
    ).count()
    
    # Placeholders for future phases
    quizzes_count = 0
    study_time_hours = 0
    
    return DashboardStats(
        documents_count=doc_count,
        questions_count=chat_count,
        quizzes_count=quizzes_count,
        study_time_hours=study_time_hours
    )
