"""
API request/response models for RAG Chatbot Integration - Spec 4
T004: Create API request/response models in `backend/chat_api/models.py` using Pydantic
"""
from pydantic import BaseModel, Field
from typing import List, Optional


class ChatRequest(BaseModel):
    """
    Request model for chat endpoint
    """
    question: str = Field(..., min_length=1, max_length=2000, description="The user's question to be answered")
    context: Optional[str] = Field(None, max_length=5000, description="Optional additional context for the question")


class SourceReference(BaseModel):
    """
    Model for source reference in chat responses
    """
    url: str = Field(..., description="URL to the source document")
    text: str = Field(..., description="Relevant text snippet from the source")


class ChatResponse(BaseModel):
    """
    Response model for chat endpoint
    """
    answer: str = Field(..., description="The generated answer to the question")
    sources: List[SourceReference] = Field(..., description="List of sources used in the response")


class HealthResponse(BaseModel):
    """
    Response model for health check endpoint
    """
    status: str = Field(..., description="Health status of the service")
    timestamp: str = Field(..., description="Timestamp of the health check")
    version: str = Field(..., description="Version of the service")