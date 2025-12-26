"""
Environment variable loading and validation for RAG Chatbot Integration - Spec 4
T005: Set up environment variable loading and validation in `backend/chat_api/config.py`
"""
import os
from typing import Optional
from dotenv import load_dotenv
import logging

# Load environment variables from .env file
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Config:
    """
    Configuration class to manage environment variables
    """
    # Load environment variables with defaults
    GEMINI_API_KEY: Optional[str] = os.getenv("GEMINI_API_KEY")
    COHERE_API_KEY: Optional[str] = os.getenv("COHERE_API_KEY")
    QDRANT_URL: Optional[str] = os.getenv("QDRANT_URL")
    QDRANT_API_KEY: Optional[str] = os.getenv("QDRANT_API_KEY")
    QDRANT_COLLECTION_NAME: str = os.getenv("QDRANT_COLLECTION_NAME", "book_chunks")

    # Validate required environment variables
    @classmethod
    def validate(cls):
        """
        Validate that all required environment variables are set
        """
        required_vars = [
            ("GEMINI_API_KEY", cls.GEMINI_API_KEY),
            ("COHERE_API_KEY", cls.COHERE_API_KEY),
            ("QDRANT_URL", cls.QDRANT_URL),
            ("QDRANT_API_KEY", cls.QDRANT_API_KEY)
        ]

        missing_vars = []
        for var_name, var_value in required_vars:
            if not var_value:
                missing_vars.append(var_name)

        if missing_vars:
            error_msg = f"Missing required environment variables: {', '.join(missing_vars)}"
            logger.error(error_msg)
            raise ValueError(error_msg)

        logger.info("All required environment variables are present")
        return True


# Validate configuration on import
try:
    Config.validate()
except ValueError as e:
    logger.error(f"Configuration validation failed: {e}")
    raise