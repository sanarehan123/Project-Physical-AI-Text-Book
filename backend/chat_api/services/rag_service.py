"""
RAG service module for RAG Chatbot Integration - Spec 4
T007: Create RAG service module in `backend/chat_api/services/rag_service.py` that reuses agent.py functions
"""
import os
import logging
import re
from typing import List, Dict, Any, Optional
from qdrant_client import QdrantClient
from qdrant_client.http import models
import cohere
from openai import OpenAI
from chat_api.config import Config

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Cohere client globally to avoid repeated initialization
co = cohere.Client(Config.COHERE_API_KEY)


def connect_qdrant() -> QdrantClient:
    """
    Connect to Qdrant vector database

    Returns:
        QdrantClient: Connected client instance
    """
    try:
        client = QdrantClient(
            url=Config.QDRANT_URL,
            api_key=Config.QDRANT_API_KEY,
            timeout=30
        )

        # Test the connection
        client.get_collection(Config.QDRANT_COLLECTION_NAME)
        logger.info(f"Successfully connected to Qdrant collection: {Config.QDRANT_COLLECTION_NAME}")
        return client
    except Exception as e:
        logger.error(f"Failed to connect to Qdrant: {str(e)}")
        raise


def expand_query(query_text: str) -> str:
    """
    Expand query to include synonyms and related terms to improve retrieval

    Args:
        query_text (str): Original query text

    Returns:
        str: Expanded query text
    """
    # Dictionary of common terms and their expansions in the context of the textbook
    expansions = {
        'humanoid robotics': 'humanoid robot OR robotics OR humanoid OR robots',
        'humanoid robot': 'humanoid robotics OR robotics OR humanoid OR robots',
        'physical ai': 'physical artificial intelligence OR embodied ai OR embodied artificial intelligence',
        'ai': 'artificial intelligence',
        'constraints': 'constraints OR limitations OR challenges OR restrictions',
        'gaps': 'gaps OR limitations OR challenges OR differences',
        'reality': 'reality OR real world OR practical OR actual',
        'simulation': 'simulation OR simulated OR modeling OR model',
        'physics': 'physics OR physical laws OR physical constraints',
        'dynamics': 'dynamics OR dynamic systems OR motion OR movement',
        'kinematics': 'kinematics OR motion OR movement OR positioning',
        'control': 'control OR controller OR controlling OR regulation',
        'locomotion': 'locomotion OR walking OR movement OR gait OR mobility',
        'balance': 'balance OR stability OR equilibrium OR posture',
        'sensors': 'sensors OR sensing OR perception OR sensor',
        'actuators': 'actuators OR motors OR actuation OR motor',
        'embodiment': 'embodiment OR embodied OR physical form OR physical body',
    }

    expanded_query = query_text.lower()

    # Apply expansions
    for term, expansion in expansions.items():
        if term in expanded_query:
            expanded_query = expanded_query.replace(term, expansion)

    # Combine original and expanded query
    final_query = f"{query_text} {expanded_query}"

    logger.info(f"Expanded query: '{query_text}' -> '{final_query}'")
    return final_query


def embed_query(query_text: str) -> List[float]:
    """
    Generate embedding vector for a text query using Cohere

    Args:
        query_text (str): The text to be embedded

    Returns:
        List[float]: Vector representation of the query
    """
    try:
        # Expand the query to improve retrieval
        expanded_query = expand_query(query_text)

        # Generate embedding using the same model as Spec 1
        response = co.embed(
            texts=[expanded_query],
            model="embed-english-v3.0",
            input_type="search_query"
        )

        # Extract the embedding from response
        embedding = response.embeddings[0]
        logger.info(f"Generated embedding for query: {query_text[:50]}...")
        return embedding
    except Exception as e:
        logger.error(f"Failed to generate embedding for query '{query_text}': {str(e)}")
        raise


def retrieve_chunks(query_embedding: List[float], top_k: int = 10) -> List[Dict[str, Any]]:
    """
    Perform vector search in Qdrant to find similar content

    Args:
        query_embedding (List[float]): Vector to search for
        top_k (int): Number of results to return (default 3)

    Returns:
        List[Dict[str, Any]]: Top matching content chunks with metadata
    """
    try:
        client = connect_qdrant()

        # Perform vector search in Qdrant
        search_results = client.query_points(
            collection_name=Config.QDRANT_COLLECTION_NAME,
            query=query_embedding,
            limit=top_k,
            with_payload=True,
        )

        # Format results
        formatted_results = []
        for result in search_results.points:
            formatted_result = {
                'content': result.payload.get('content', '') if result.payload else '',
                'similarity_score': result.score,
                'source_url': result.payload.get('source_url', '') if result.payload else '',
                'title': result.payload.get('title', '') if result.payload else '',
                'section': result.payload.get('section', '') if result.payload else '',
                'chunk_id': result.id
            }
            formatted_results.append(formatted_result)

        logger.info(f"Found {len(formatted_results)} results for the query")
        return formatted_results

    except Exception as e:
        logger.error(f"Search failed: {str(e)}")
        raise


def generate_response(question: str, context_chunks: List[Dict[str, Any]], user_context: str = None) -> Dict[str, Any]:
    """
    Generate natural language response using Google Gemini API

    Args:
        question (str): Original user question
        context_chunks (List[Dict[str, Any]]): Relevant context chunks
        user_context (str, optional): Additional user-provided context

    Returns:
        Dict[str, Any]: Generated answer and sources
    """
    try:
        # Check if GEMINI_API_KEY is available
        if not Config.GEMINI_API_KEY:
            raise ValueError("GEMINI_API_KEY environment variable is not set. Please add it to your .env file.")

        # Initialize OpenAI client with Gemini's OpenAI-compatible endpoint
        client = OpenAI(
            api_key=Config.GEMINI_API_KEY,
            base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
        )

        # Build the system message with context
        context_text = ""
        for i, chunk in enumerate(context_chunks, 1):
            content_preview = chunk['content'][:500] if chunk['content'] else "[No content available]"
            # Handle special characters by encoding/decoding safely
            try:
                content_str = content_preview.encode('utf-8', errors='ignore').decode('utf-8')
            except:
                content_str = "[Content with encoding issues]"

            context_text += f"Context {i}:\n"
            context_text += f"Content: {content_str}{'...' if len(chunk['content']) > 500 else ''}\n"
            context_text += f"Source: {chunk['source_url']}\n"
            context_text += f"Title: {chunk['title']}\n"
            context_text += f"Section: {chunk['section']}\n\n"

        # Add user-provided context if available
        if user_context:
            context_text += f"Additional User Context:\n{user_context}\n\n"

        # Construct the system message
        system_message = f"""You are a helpful assistant answering questions about the book. Answer only using the provided context. Be concise and accurate.

Context:
{context_text}

Instructions:
- Answer the question based only on the provided context
- Include source citations in your response when referencing specific information
- If partial information is found, summarize what is available and suggest related sections
- Do not refuse to answer unless absolutely no relevant context exists
- Be concise and accurate in your response
- If the context contains related information but not the exact answer, provide what you can find"""

        # Create messages for the API
        messages = [
            {"role": "system", "content": system_message},
            {"role": "user", "content": question}
        ]

        # Call Gemini API via OpenAI-compatible endpoint
        response = client.chat.completions.create(
            model="gemini-2.5-flash",  # Using Gemini flash model for free tier
            messages=messages,
            temperature=0.3,  # Lower temperature for more consistent answers
            max_tokens=1000
        )

        # Extract the answer
        answer = response.choices[0].message.content

        # Format sources
        sources = []
        for chunk in context_chunks:
            source_info = {
                'url': chunk['source_url'],
                'text': chunk['content'][:200] + '...' if len(chunk['content']) > 200 else chunk['content']
            }
            sources.append(source_info)

        logger.info(f"Generated response for question: {question[:50]}...")

        return {
            'answer': answer,
            'sources': sources
        }
    except Exception as e:
        logger.error(f"Failed to generate response: {str(e)}")
        raise