# RAG Chatbot Agent – Spec 3: Build & finalize OpenAI Agents SDK agent with book retrieval

## Overview
Build a RAG agent that can answer questions about the physical AI textbook using the existing Qdrant collection. The agent should retrieve relevant content and generate natural language responses with proper citations.

## Requirements
- Use existing Qdrant collection 'book_chunks' that contains book embeddings
- Use existing .env variables: COHERE_API_KEY, QDRANT_URL, QDRANT_API_KEY
- Add OPENAI_API_KEY for LLM functionality
- Create backend/agent.py as single file implementation

## Core Functionality
1. Accept user questions as input
2. Generate query embedding using the same Cohere model as ingestion
3. Retrieve top-3 most relevant chunks from Qdrant
4. Build system prompt with:
   - Instruction: "You are a helpful assistant answering questions about the book. Answer only using the provided context. Be concise and accurate."
   - Retrieved chunks as context
   - Source citation requirement: include URLs or section titles from metadata
5. Call OpenAI API (gpt-4o-mini or gpt-4o) to generate final answer
6. Return both generated answer and list of used sources

## Additional Features
- Support for selected-text mode with optional --context flag
- Basic CLI interface:
  - `python agent.py --question "What is the principle of least action?"`
  - `python agent.py --question "Explain X..." --context "user highlighted this paragraph..."`
- Proper error handling, logging, and rate-limit respect
- Use python-dotenv to load all keys securely

## Constraints
- Keep simple: single-turn, no memory/chat history yet, no complex tools
- Use same embedding model as Spec 1 for consistency
- Ensure proper content encoding and error handling