import json
from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import desc
from google import genai
from app.config import settings
from app.models.document import Document
from app.models.chunk import DocumentChunk
from app.models.chat import ChatMessage


def generate_answer(query: str, user_id: int, db: Session, document_id: Optional[int] = None) -> str:
    """
    RAG pipeline:
    1. Embed the query
    2. Search vector database for context
    3. Generate response using LLM
    """
    client = genai.Client(api_key=settings.GEMINI_API_KEY)
    
    # 1. Embed the user's query
    embed_response = client.models.embed_content(
        model="gemini-embedding-2",
        contents=query
    )
    query_embedding = embed_response.embeddings[0].values
    
    # 2. Search database for relevant context (Top 5 chunks)
    # Join with Document to ensure we only search the user's own documents
    base_query = db.query(DocumentChunk, Document.filename).join(
        Document, DocumentChunk.document_id == Document.id
    ).filter(Document.user_id == user_id, Document.status == "ready")
    
    if document_id:
        base_query = base_query.filter(Document.id == document_id)
        
    # pgvector cosine distance: <=> 
    results = base_query.order_by(
        DocumentChunk.embedding.cosine_distance(query_embedding)
    ).limit(5).all()
    
    if not results:
        return "I couldn't find any relevant information in your uploaded documents. Please upload some study materials first!"
        
    # 3. Construct the prompt with context
    context_parts = []
    for chunk, filename in results:
        page_ref = f" (Page {chunk.page_number})" if chunk.page_number else ""
        context_parts.append(f"--- Source: {filename}{page_ref} ---\n{chunk.text_content}")
        
    context_string = "\n\n".join(context_parts)
    
    # Get previous chat history for context (last 5 interactions)
    history = db.query(ChatMessage).filter(
        ChatMessage.user_id == user_id
    ).order_by(desc(ChatMessage.created_at)).limit(10).all()
    history.reverse()  # chronological order
    
    history_string = ""
    if history:
        history_string = "Previous Conversation:\n"
        for msg in history:
            role = "User" if msg.role == "user" else "Assistant"
            history_string += f"{role}: {msg.content}\n"
    
    prompt = f"""You are EduMind, an AI study assistant. Your job is to answer the user's question based strictly on the provided context extracted from their study materials.

{history_string}

CONTEXT FROM USER'S DOCUMENTS:
{context_string}

USER'S QUESTION:
{query}

INSTRUCTIONS:
1. Answer the question using ONLY the provided context.
2. If the answer is not in the context, politely say "I cannot find the answer to this in your uploaded documents." Do not hallucinate or use outside knowledge.
3. Cite your sources implicitly or explicitly using the source filename and page numbers provided in the context (e.g., "According to Biology_Notes.pdf (Page 4)...").
4. Format your answer nicely using Markdown (bullet points, bold text, code blocks if necessary) to make it easy to read.
"""

    # 4. Generate the response
    chat_response = client.models.generate_content(
        model=settings.GEMINI_MODEL,
        contents=prompt
    )
    
    return chat_response.text
