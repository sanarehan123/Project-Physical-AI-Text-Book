# Quickstart Guide for RAG Agent

## Prerequisites
- Python 3.11+
- Qdrant collection 'book_chunks' populated with content (from Spec 1)
- Environment variables configured in .env file:
  - QDRANT_URL
  - QDRANT_API_KEY
  - COHERE_API_KEY
  - OPENAI_API_KEY

## Setup
1. Install required dependencies:
   ```bash
   pip install qdrant-client cohere openai python-dotenv argparse
   ```

2. Ensure .env file contains all required API keys

## Usage Examples
1. Basic question answering:
   ```bash
   python backend/agent.py --question "What is the principle of least action?"
   ```

2. With additional context:
   ```bash
   python backend/agent.py --question "Explain quantum entanglement" --context "The user highlighted this paragraph about quantum states..."
   ```

## Expected Output
- Natural language answer to the question
- List of sources used (URLs and short snippets)
- Confidence in the response based on source relevance

## Troubleshooting
- If getting 404 errors, ensure the Qdrant collection 'book_chunks' exists and has content
- If API calls fail, check that all required environment variables are set
- If responses are not relevant, verify the ingestion pipeline (Spec 1) ran successfully