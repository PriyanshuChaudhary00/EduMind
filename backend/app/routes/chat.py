from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import desc
from app.database import get_db
from app.utils.dependencies import get_current_user
from app.models.user import User
from app.models.chat import ChatMessage
from app.schemas.chat import ChatRequest, ChatMessageResponse, ChatHistoryResponse
from app.services.chat_engine import generate_answer

router = APIRouter()


@router.post("/send", response_model=ChatMessageResponse)
def send_message(
    request: ChatRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Receive user message, run RAG pipeline, return AI response.
    """
    if not request.message.strip():
        raise HTTPException(status_code=400, detail="Message cannot be empty")

    # 1. Save user message to DB
    user_msg = ChatMessage(
        user_id=current_user.id,
        role="user",
        content=request.message
    )
    db.add(user_msg)
    db.commit()

    # 2. Generate AI Answer (RAG)
    try:
        ai_response_text = generate_answer(
            query=request.message,
            user_id=current_user.id,
            db=db,
            document_id=request.document_id
        )
    except Exception as e:
        print(f"Chat generation error: {e}")
        raise HTTPException(status_code=500, detail="Failed to generate AI response.")

    # 3. Save AI message to DB
    ai_msg = ChatMessage(
        user_id=current_user.id,
        role="assistant",
        content=ai_response_text
    )
    db.add(ai_msg)
    db.commit()
    db.refresh(ai_msg)

    return ai_msg


@router.get("/history", response_model=ChatHistoryResponse)
def get_chat_history(
    limit: int = 50,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Retrieve the user's chat history.
    """
    messages = db.query(ChatMessage).filter(
        ChatMessage.user_id == current_user.id
    ).order_by(desc(ChatMessage.created_at)).limit(limit).all()
    
    # Return in chronological order
    messages.reverse()
    
    return ChatHistoryResponse(messages=messages)
