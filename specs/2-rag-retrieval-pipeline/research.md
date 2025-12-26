# Research: RAG Chatbot Retrieval Pipeline

## Decision: Vector Retrieval Implementation
**Rationale**: Implement a simple vector retrieval system using Cohere embeddings and Qdrant vector database to validate the ingestion pipeline from Spec 1. This approach allows for semantic search without requiring complex LLM integration at this stage.

## Unknowns Resolved:

### 1. Cohere Embedding Model Selection
- **Issue**: Which Cohere embedding model to use for consistency with Spec 1
- **Resolution**: Use the same model as Spec 1 (likely embed-english-v3.0 or similar) to ensure compatibility with ingested content
- **Reference**: Need to check the ingestion pipeline from Spec 1 to identify the exact model used

### 2. Qdrant Collection Structure
- **Issue**: Understanding the structure of the existing Qdrant collection created in Spec 1
- **Resolution**: The collection should have documents with embeddings, source URLs, titles, sections, and content chunks
- **Reference**: Will inspect the collection schema during implementation

### 3. Test Question Design
- **Issue**: Creating 5-8 realistic test questions that cover different book sections
- **Resolution**: Design questions that target different chapters/sections of the physical AI textbook to validate comprehensive retrieval
- **Approach**: Focus on conceptual questions, factual questions, and application-based questions from different book parts

### 4. Similarity Threshold Validation
- **Issue**: Validating the 0.78 cosine similarity threshold
- **Resolution**: This threshold balances precision and recall for semantic matching
- **Reference**: Common practice in vector retrieval systems, can be adjusted based on results

## Technology Stack:

### Primary Dependencies:
- **qdrant-client**: Python client for Qdrant vector database
- **cohere**: For generating embeddings with the same model as Spec 1
- **python-dotenv**: For loading environment variables
- **argparse**: For CLI argument parsing

### Integration Points:
- **Environment Variables**: QDRANT_URL, QDRANT_API_KEY, QDRANT_COLLECTION_NAME, COHERE_API_KEY
- **External Services**: Qdrant vector database, Cohere embedding API

## Best Practices Applied:

### 1. Error Handling
- Implement proper error handling for API calls and database connections
- Graceful degradation when services are unavailable

### 2. Performance Considerations
- Single embedding generation per query to minimize API calls
- Efficient vector search with top-k parameter (k=5 initially, but only showing top-3 in results)

### 3. Validation Approach
- Manual verification of results with human-readable output
- Clear display of question, retrieved content, similarity scores, and source metadata

## Alternative Approaches Considered:

### 1. Different Vector Databases
- **Option**: Use Pinecone, Weaviate, or Chroma instead of Qdrant
- **Decision**: Stick with Qdrant since it was used in Spec 1 and already has the ingested content

### 2. Different Embedding Models
- **Option**: Use OpenAI, Hugging Face, or Google embeddings instead of Cohere
- **Decision**: Use Cohere for consistency with Spec 1 ingestion pipeline

### 3. Advanced Retrieval Techniques
- **Option**: Implement re-ranking, query expansion, or hybrid search
- **Decision**: Keep it simple with pure vector search as specified in requirements

## Expected Challenges:
1. Ensuring the Qdrant collection from Spec 1 is properly populated
2. Matching the embedding model used in Spec 1 exactly
3. Designing diverse test questions that effectively validate retrieval quality
4. Handling potential API rate limits from Cohere during testing