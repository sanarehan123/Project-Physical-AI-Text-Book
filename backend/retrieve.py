#!/usr/bin/env python3
"""
RAG Chatbot Retrieval Pipeline - Spec 2
Test data extraction, chunking, embedding & retrieval from Qdrant

This script validates the ingestion pipeline by performing vector retrieval tests
on the physical AI textbook content stored in Qdrant.
"""
import os
import argparse
import logging
from typing import List, Dict, Any, Optional
from dotenv import load_dotenv

# Import Qdrant client
try:
    from qdrant_client import QdrantClient
    from qdrant_client.http import models
except ImportError:
    logger.error("qdrant-client is not installed. Please install it with: pip install qdrant-client")
    raise

# Load environment variables from .env file
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Environment variables
QDRANT_URL = os.getenv("QDRANT_URL")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")
QDRANT_COLLECTION_NAME = os.getenv("QDRANT_COLLECTION_NAME", "book_chunks")  # Default collection name
COHERE_API_KEY = os.getenv("COHERE_API_KEY")

# Validate required environment variables
REQUIRED_ENV_VARS = [
    ("QDRANT_URL", QDRANT_URL),
    ("QDRANT_API_KEY", QDRANT_API_KEY),
    ("QDRANT_COLLECTION_NAME", QDRANT_COLLECTION_NAME),
    ("COHERE_API_KEY", COHERE_API_KEY)
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
            # Set timeout for API calls
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
        import cohere
    except ImportError:
        logger.error("cohere is not installed. Please install it with: pip install cohere")
        raise

    try:
        # Expand the query to improve retrieval
        expanded_query = expand_query(query_text)

        # Initialize Cohere client
        co = cohere.Client(COHERE_API_KEY)

        # Generate embedding using the same model as Spec 1
        # Using embed-english-v3.0 as it's the latest recommended model
        response = co.embed(
            texts=[expanded_query],
            model="embed-english-v3.0",
            input_type="search_query"  # Using search_query type for better retrieval performance
        )

        # Extract the embedding from response
        embedding = response.embeddings[0]  # Get the first (and only) embedding
        logger.info(f"Generated embedding for query: {query_text[:50]}...")
        return embedding
    except Exception as e:
        logger.error(f"Failed to generate embedding for query '{query_text}': {str(e)}")
        raise


def search(query_embedding: List[float], top_k: int = 12) -> List[Dict[str, Any]]:
    """
    Perform vector search in Qdrant to find similar content

    Args:
        query_embedding (List[float]): Vector to search for
        top_k (int): Number of results to return (default 5)

    Returns:
        List[Dict[str, Any]]: Top matching content chunks with metadata
    """
    try:
        client = connect_qdrant()

        # Perform vector search in Qdrant (use query_points method on newer client)
        search_results = client.query_points(
            collection_name=QDRANT_COLLECTION_NAME,
            query=query_embedding,
            limit=top_k,
            with_payload=True,  # Include payload (metadata) in results
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


def print_results(question: str, results: List[Dict[str, Any]]) -> None:
    """
    Format and print retrieval results in human-readable format

    Args:
        question (str): Original question
        results (List[Dict[str, Any]]): Retrieved content chunks
    """
    print(f"\nQuestion: {question}")
    print("-" * 80)
    print("Retrieved Results:")

    if not results:
        print("No results found.")
        return

    for i, result in enumerate(results, 1):
        content_preview = result['content'][:300] if result['content'] else "[No content available]"
        # Handle special characters by encoding/decoding safely
        try:
            content_str = content_preview.encode('utf-8', errors='ignore').decode('utf-8')
        except:
            content_str = "[Content with encoding issues]"

        print(f"\n{i}. {content_str}{'...' if len(result['content']) > 300 else '' if result['content'] else ''}")
        print(f"   (Score: {result['similarity_score']:.3f}, Source: {result['source_url']})")
        print(f"   Title: {result['title']}, Section: {result['section']}")

    print("-" * 80)


def validate_relevance(results: List[Dict[str, Any]], threshold: float = 0.78) -> tuple[bool, int]:
    """
    Check if retrieved results meet relevance criteria

    Args:
        results (List[Dict[str, Any]]): Retrieved content chunks
        threshold (float): Minimum similarity score (default 0.78)

    Returns:
        tuple[bool, int]: (valid, relevant_count)
    """
    relevant_count = sum(1 for result in results if result['similarity_score'] >= threshold)
    is_valid = relevant_count > 0  # At least one result should meet threshold
    return is_valid, relevant_count


def retrieve_and_print(question: str) -> bool:
    """
    Retrieve results for a question and print them

    Args:
        question (str): The question to retrieve results for

    Returns:
        bool: True if relevant results were found, False otherwise
    """
    try:
        # Generate embedding for the question
        query_embedding = embed_query(question)

        # Perform search with higher top_k for better coverage
        results = search(query_embedding, top_k=12)  # Get top 12 for better coverage

        # Print results
        print_results(question, results[:3])  # Show top 3 results

        # Validate relevance
        is_valid, relevant_count = validate_relevance(results[:3])
        relevance_msg = f"Relevance Check: {'PASS' if is_valid else 'FAIL'} - {relevant_count}/3 relevant results above 0.78 threshold"
        print(relevance_msg.encode('utf-8', errors='ignore').decode('utf-8'))

        return is_valid
    except Exception as e:
        logger.error(f"Error processing question '{question}': {str(e)}")
        return False


def run_all_tests():
    """Run all predefined test questions covering different book sections/topics"""
    # Define 5-8 realistic test questions about different book sections/topics
    test_questions = [
        {
            "question": "What is the principle of least action in physics?",
            "category": "Classical Mechanics",
            "purpose": "Tests understanding of fundamental physics principles from early chapters"
        },
        {
            "question": "How does quantum entanglement work and what are its implications?",
            "category": "Quantum Mechanics",
            "purpose": "Tests advanced quantum concepts from later chapters"
        },
        {
            "question": "Explain the concept of neural networks and their applications in AI",
            "category": "Artificial Intelligence",
            "purpose": "Tests AI-specific content from AI-focused sections"
        },
        {
            "question": "What are the key differences between supervised and unsupervised learning?",
            "category": "Machine Learning",
            "purpose": "Tests machine learning fundamentals"
        },
        {
            "question": "How does the human brain process information compared to artificial neural networks?",
            "category": "Cognitive Science",
            "purpose": "Tests interdisciplinary content bridging neuroscience and AI"
        },
        {
            "question": "What is the relationship between entropy and information theory?",
            "category": "Information Theory",
            "purpose": "Tests advanced concepts connecting physics and information"
        },
        {
            "question": "Explain the mathematical foundations of quantum mechanics",
            "category": "Mathematical Physics",
            "purpose": "Tests mathematical concepts applied to physics"
        }
    ]

    print(f"Running {len(test_questions)} test questions covering different book sections...\n")

    total_questions = len(test_questions)
    successful_retrievals = 0

    for i, test in enumerate(test_questions, 1):
        print(f"({i}/{total_questions}) Testing: {test['question']}")
        print(f"Category: {test['category']} | Purpose: {test['purpose']}")

        success = retrieve_and_print(test['question'])
        if success:
            successful_retrievals += 1
        print()

    print("=" * 80)
    print(f"SUMMARY: {successful_retrievals}/{total_questions} questions had relevant results")
    print(f"Success rate: {(successful_retrievals/total_questions)*100:.1f}%")

    if successful_retrievals == total_questions:
        print("✅ All questions returned relevant results! Retrieval pipeline validation successful.")
    elif successful_retrievals >= total_questions * 0.8:  # 80% threshold
        print("✅ Most questions returned relevant results. Retrieval pipeline is working well.")
    else:
        print("⚠️  Less than 80% of questions returned relevant results. Check the ingestion pipeline.")


def main():
    """Main function to execute the retrieval pipeline"""
    print("RAG Chatbot Retrieval Pipeline - Validation Script")
    print("=" * 80)

    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Validate RAG retrieval pipeline')
    parser.add_argument('--question', type=str, help='Specific question to test')
    parser.add_argument('--all', action='store_true', help='Run all predefined test questions')
    parser.add_argument('--recreate', action='store_true', help='Delete and recreate collection before testing')

    args = parser.parse_args()

    # If --recreate flag is set, warn user (actual recreation would require additional implementation)
    if args.recreate:
        logger.warning("Recreate flag set - note that actual collection recreation would require additional implementation")
        print("Note: The --recreate flag is recognized but full implementation would require collection management functions.")

    # Run specific question or all predefined questions
    if args.question:
        print(f"Testing specific question: {args.question}")
        retrieve_and_print(args.question)
    elif args.all:
        print("Running all predefined test questions...")
        run_all_tests()
    else:
        print("Please specify either --question 'your question here' or --all")
        print("\nExamples:")
        print("  python retrieve.py --question 'What is the principle of least action?'")
        print("  python retrieve.py --all")
        print("  python retrieve.py --all --recreate")
        return


if __name__ == "__main__":
    main()