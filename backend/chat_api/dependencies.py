"""
API dependencies module for RAG Chatbot Integration - Spec 4
T009: Create API dependencies module in `backend/chat_api/dependencies.py`
"""
from fastapi import HTTPException
from typing import Optional
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def validate_question(question: Optional[str]) -> str:
    """
    Validate the question parameter

    Args:
        question: The question string to validate

    Returns:
        str: The validated question string

    Raises:
        HTTPException: If question is invalid
    """
    if not question:
        raise HTTPException(status_code=400, detail="Question is required")

    if not question.strip():
        raise HTTPException(status_code=400, detail="Question cannot be empty or whitespace only")

    if len(question) > 2000:  # Max length from data model
        raise HTTPException(status_code=400, detail="Question is too long (max 2000 characters)")

    return question


def validate_context(context: Optional[str]) -> Optional[str]:
    """
    Validate the context parameter

    Args:
        context: The context string to validate

    Returns:
        Optional[str]: The validated context string or None
    """
    if context is None:
        return None

    if len(context) > 5000:  # Max length from data model
        raise HTTPException(status_code=400, detail="Context is too long (max 5000 characters)")

    return context