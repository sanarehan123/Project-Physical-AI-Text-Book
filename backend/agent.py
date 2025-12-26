#!/usr/bin/env python3
"""
RAG Chatbot Agent - Spec 3
Google Gemini API agent with book retrieval from Qdrant

This script implements a RAG agent that:
1. Takes a user question as input
2. Generates query embedding using Cohere
3. Retrieves relevant chunks from Qdrant
4. Generates natural language response using Google Gemini
5. Returns answer with source citations
"""
# Using Google Gemini API (OpenAI compatible) - free tier
import os
import argparse
import logging
import json
import re
from typing import List, Dict, Any, Optional
from dotenv import load_dotenv

# Import required libraries
try:
    import cohere
    from openai import OpenAI
    import openai
    from qdrant_client import QdrantClient
    from qdrant_client.http import models
except ImportError as e:
    logger = logging.getLogger(__name__)
    logger.error(f"Missing required packages: {str(e)}")
    logger.error("Please install with: pip install cohere openai qdrant-client python-dotenv argparse")
    raise

# Load environment variables from .env file
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Environment variables
QDRANT_URL = os.getenv("QDRANT_URL")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")
QDRANT_COLLECTION_NAME = os.getenv("QDRANT_COLLECTION_NAME", "book_chunks")
COHERE_API_KEY = os.getenv("COHERE_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Validate required environment variables
REQUIRED_ENV_VARS = [
    ("QDRANT_URL", QDRANT_URL),
    ("QDRANT_API_KEY", QDRANT_API_KEY),
    ("QDRANT_COLLECTION_NAME", QDRANT_COLLECTION_NAME),
    ("COHERE_API_KEY", COHERE_API_KEY),
    ("GEMINI_API_KEY", GEMINI_API_KEY)
]

for var_name, var_value in REQUIRED_ENV_VARS:
    if not var_value:
        logger.error(f"Missing required environment variable: {var_name}")
        raise ValueError(f"Missing required environment variable: {var_name}")


def connect_qdrant() -> QdrantClient:
    """
    Connect to Qdrant vector database

    Returns:
        QdrantClient: Connected client instance
    """
    try:
        client = QdrantClient(
            url=QDRANT_URL,
            api_key=QDRANT_API_KEY,
            timeout=30
        )

        # Test the connection
        client.get_collection(QDRANT_COLLECTION_NAME)
        logger.info(f"Successfully connected to Qdrant collection: {QDRANT_COLLECTION_NAME}")
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

    # Handle "what are X" patterns
    pattern = r"what are (\w+)"
    match = re.search(pattern, query_text.lower())
    if match:
        term = match.group(1)
        query_text = f"define {term} OR explain {term} OR what is {term} OR {term} description OR {query_text}"

    # Handle general questions by appending book-specific terms
    if not query_text.lower().startswith(('hi', 'hello', 'hey')):
        query_text = f"{query_text} in humanoid robotics OR in physical ai OR in the textbook"

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
        # Initialize Cohere client
        co = cohere.Client(COHERE_API_KEY)

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
            collection_name=QDRANT_COLLECTION_NAME,
            query=query_embedding,
            limit=top_k,
            with_payload=True,
        )

        # Format results with similarity threshold filtering
        formatted_results = []
        min_score = 0.65  # Minimum similarity score threshold
        for result in search_results.points:
            # Only include results that meet the minimum similarity threshold
            if result.score >= min_score:
                formatted_result = {
                    'content': result.payload.get('content', '') if result.payload else '',
                    'similarity_score': result.score,
                    'source_url': result.payload.get('source_url', '') if result.payload else '',
                    'title': result.payload.get('title', '') if result.payload else '',
                    'section': result.payload.get('section', '') if result.payload else '',
                    'chunk_id': result.id
                }
                formatted_results.append(formatted_result)

        logger.info(f"Found {len(formatted_results)} results for the query with similarity score >= {min_score}")
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
        gemini_api_key = os.getenv("GEMINI_API_KEY")
        if not gemini_api_key:
            raise ValueError("GEMINI_API_KEY environment variable is not set. Please add it to your .env file.")

        # Initialize OpenAI client with Gemini's OpenAI-compatible endpoint
        client = OpenAI(
            api_key=gemini_api_key,
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
                'title': chunk['title'],
                'section': chunk['section'],
                'snippet': chunk['content'][:200] + '...' if len(chunk['content']) > 200 else chunk['content']
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


def format_sources(chunks: List[Dict[str, Any]]) -> List[Dict[str, str]]:
    """
    Format source information for citation

    Args:
        chunks (List[Dict[str, Any]]): Retrieved chunks

    Returns:
        List[Dict[str, str]]: Formatted source objects
    """
    formatted_sources = []
    for chunk in chunks:
        source_info = {
            'url': chunk['source_url'],
            'title': chunk['title'],
            'section': chunk['section'],
            'snippet': chunk['content'][:200] + '...' if len(chunk['content']) > 200 else chunk['content']
        }
        formatted_sources.append(source_info)
    return formatted_sources


def main():
    """Main function to execute the RAG agent"""
    print("RAG Chatbot Agent - Spec 3")
    print("=" * 80)

    # Parse command line arguments
    parser = argparse.ArgumentParser(description='RAG Chatbot Agent with book retrieval')
    parser.add_argument('--question', type=str, required=True, help='Question to answer')
    parser.add_argument('--context', type=str, help='Additional context to include in response')

    args = parser.parse_args()

    try:
        # Generate embedding for the question
        query_embedding = embed_query(args.question)

        # Retrieve relevant chunks with higher top_k for better coverage
        retrieved_chunks = retrieve_chunks(query_embedding, top_k=10)

        # Generate response using OpenAI
        response = generate_response(args.question, retrieved_chunks, args.context)

        # Print the answer
        print(f"\nQuestion: {args.question}")
        print("-" * 80)
        # Handle potential encoding issues when printing
        try:
            print(f"Answer:\n{response['answer']}")
        except UnicodeEncodeError:
            print(f"Answer:\n{response['answer'].encode('utf-8', errors='ignore').decode('utf-8')}")
        print("-" * 80)

        # Print sources
        print("Sources used:")
        for i, source in enumerate(response['sources'], 1):
            print(f"\n{i}. {source['title']}")
            print(f"   URL: {source['url']}")
            print(f"   Section: {source['section']}")
            try:
                print(f"   Snippet: {source['snippet'][:100]}...")
            except UnicodeEncodeError:
                snippet = source['snippet'][:100].encode('utf-8', errors='ignore').decode('utf-8')
                print(f"   Snippet: {snippet}...")

        print("-" * 80)
        print("✅ RAG agent completed successfully")

    except Exception as e:
        error_msg = str(e)
        logger.error(f"Error processing question: {error_msg}")
        try:
            print(f"Error: {error_msg}")
        except UnicodeEncodeError:
            print(f"Error: {error_msg.encode('utf-8', errors='ignore').decode('utf-8')}")
        return 1

    return 0


if __name__ == "__main__":
    main()