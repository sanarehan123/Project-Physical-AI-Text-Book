"""
Chat service module for RAG Chatbot Integration - Spec 4
T008: Create chat service module in `backend/chat_api/services/chat_service.py`
"""
import logging
from typing import Dict, Any
from chat_api.services.rag_service import embed_query, retrieve_chunks, generate_response

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ChatService:
    """
    Service class to handle chat operations and RAG processing
    """

    @staticmethod
    def process_chat_request(question: str, context: str = None) -> Dict[str, Any]:
        """
        Process a chat request using RAG (Retrieval-Augmented Generation)

        Args:
            question (str): The user's question
            context (str, optional): Additional context provided by user

        Returns:
            Dict[str, Any]: Response containing answer and sources
        """
        if not question or not question.strip():
            raise ValueError("Question cannot be empty or whitespace only")

        try:
            # Generate embedding for the question
            logger.info(f"Processing question: {question[:100]}...")
            query_embedding = embed_query(question)

            # Retrieve relevant chunks from vector database with higher top_k for better coverage
            retrieved_chunks = retrieve_chunks(query_embedding, top_k=10)

            # Generate response using the retrieved context
            response = generate_response(question, retrieved_chunks, context)

            logger.info("Successfully processed chat request")
            return response

        except ValueError as ve:
            logger.error(f"Value error in chat processing: {str(ve)}")
            raise
        except Exception as e:
            logger.error(f"Error processing chat request: {str(e)}")
            raise