# API Contracts for RAG Agent

## Function Interfaces

### connect_qdrant()
- **Purpose**: Establish connection to Qdrant vector database
- **Input**: None (uses environment variables)
- **Output**: QdrantClient instance
- **Errors**: ConnectionError, AuthenticationError

### embed_query(query_text: str)
- **Purpose**: Generate embedding vector for a text query using Cohere
- **Input**: query_text (string) - The text to be embedded
- **Output**: List[float] - Vector representation of the query
- **Errors**: APIError, InvalidInputError

### retrieve_chunks(query_embedding: List[float], top_k: int = 3)
- **Purpose**: Perform vector search in Qdrant to find similar content
- **Input**:
  - query_embedding (List[float]) - Vector to search for
  - top_k (int, default 3) - Number of results to return
- **Output**: List[RetrievedChunk] - Top matching content chunks with metadata
- **Errors**: SearchError, DatabaseError

### generate_response(question: str, context_chunks: List[RetrievedChunk], user_context: str = None)
- **Purpose**: Generate natural language response using OpenAI API
- **Input**:
  - question (str) - Original user question
  - context_chunks (List[RetrievedChunk]) - Relevant context to use
  - user_context (str, optional) - Additional user-provided context
- **Output**: LLMResponse - Generated answer and sources
- **Errors**: APIError, RateLimitError

### format_sources(chunks: List[RetrievedChunk])
- **Purpose**: Format source information for citation
- **Input**: List of retrieved chunks
- **Output**: List of formatted source objects with URL and snippet

## CLI Interface

### Command Line Arguments
- --question (required): The question to answer
- --context (optional): Additional context to include in the response

### Exit Codes
- 0: Success
- 1: General error
- 2: Missing required environment variables
- 3: API connection error