# ADR-1: Technology Stack Selection for RAG Retrieval Pipeline

## Status
Accepted

## Date
2025-12-25

## Context
For the RAG Chatbot Retrieval Pipeline (Spec 2), we need to select an appropriate technology stack that will enable validation of the ingestion pipeline from Spec 1. The system needs to connect to Qdrant vector database, generate embeddings using Cohere API, perform vector search, and output human-readable results for manual validation.

The requirements specify:
- Pure vector retrieval validation (no LLM integration yet)
- Single Python script implementation
- Consistency with embedding model from Spec 1
- CLI interface for testing
- Human-readable output format
- Use of existing Qdrant collection

## Decision
We will use the following integrated technology stack:

**Language**: Python 3.11
- For scripting flexibility and rich ecosystem for AI/ML applications

**Vector Database Client**: qdrant-client
- For connecting to and querying the Qdrant vector database
- Maintains consistency with Spec 1 ingestion pipeline

**Embedding Service**: Cohere API
- For generating text embeddings using the same model as Spec 1
- Provides reliable, managed embedding service

**Configuration**: python-dotenv
- For secure loading of environment variables
- Follows 12-factor app principles

**CLI Framework**: argparse
- For command-line argument parsing
- Built-in Python library, lightweight

## Consequences

### Positive
- Consistency with Spec 1 ingestion pipeline through use of same embedding model and vector database
- Simple, lightweight implementation suitable for validation purposes
- Familiar technology stack for Python developers
- Secure handling of API keys and configuration via environment variables
- Clear separation of concerns between components

### Negative
- Dependency on external services (Cohere API, Qdrant) creates potential availability issues
- API costs for embedding generation during testing
- Potential rate limiting from Cohere during extensive testing
- Limited to Python ecosystem, reducing portability

## Alternatives Considered

### Alternative 1: Different Vector Database
- **Option**: Use Pinecone, Weaviate, or Chroma instead of Qdrant
- **Tradeoffs**: Would require re-ingesting data; loses consistency with Spec 1; different API patterns
- **Decision**: Rejected in favor of Qdrant to maintain consistency with existing ingestion

### Alternative 2: Different Embedding Service
- **Option**: Use OpenAI, Hugging Face, or self-hosted embeddings instead of Cohere
- **Tradeoffs**: Would require re-ingesting with different embeddings; different cost models; potential API compatibility issues
- **Decision**: Rejected to maintain consistency with Spec 1 embedding model

### Alternative 3: Advanced Retrieval Techniques
- **Option**: Implement re-ranking, query expansion, or hybrid search
- **Tradeoffs**: Would add complexity beyond validation scope; deviate from requirements
- **Decision**: Rejected in favor of pure vector search as specified

## References
- specs/2-rag-retrieval-pipeline/plan.md
- specs/2-rag-retrieval-pipeline/research.md