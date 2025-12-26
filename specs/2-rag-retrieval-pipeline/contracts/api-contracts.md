# API Contracts: RAG Chatbot Retrieval Pipeline

## Function Interfaces

### connect_qdrant()
- **Purpose**: Establish connection to Qdrant vector database
- **Input**: None (uses environment variables)
- **Output**: QdrantClient instance
- **Errors**: ConnectionError if unable to connect to Qdrant
- **Side Effects**: Establishes database connection

### embed_query(query_text: str)
- **Purpose**: Generate embedding vector for a text query using Cohere
- **Input**:
  - `query_text` (str): The text to be embedded
- **Output**:
  - `embedding` (list[float]): Vector representation of the query
- **Errors**:
  - APIError if Cohere API is unavailable
  - ValueError if query text is invalid
- **Side Effects**: Makes external API call to Cohere

### search(query_embedding: list[float], top_k: int = 5)
- **Purpose**: Perform vector search in Qdrant to find similar content
- **Input**:
  - `query_embedding` (list[float]): Vector to search for
  - `top_k` (int): Number of results to return (default 5)
- **Output**:
  - `results` (list[RetrievedChunk]): Top matching content chunks
- **Errors**:
  - SearchError if Qdrant search fails
  - ValueError if embedding is invalid
- **Side Effects**: Queries Qdrant database

### print_results(question: str, results: list[RetrievedChunk])
- **Purpose**: Format and print retrieval results in human-readable format
- **Input**:
  - `question` (str): Original question
  - `results` (list[RetrievedChunk]): Retrieved content chunks
- **Output**: None (prints to stdout)
- **Errors**: None
- **Side Effects**: Prints formatted results to console

### validate_relevance(results: list[RetrievedChunk], threshold: float = 0.78)
- **Purpose**: Check if retrieved results meet relevance criteria
- **Input**:
  - `results` (list[RetrievedChunk]): Retrieved content chunks
  - `threshold` (float): Minimum similarity score (default 0.78)
- **Output**:
  - `valid` (bool): Whether results meet threshold
  - `relevant_count` (int): Number of relevant results
- **Errors**: None
- **Side Effects**: None

## CLI Interface

### Command: python retrieve.py
- **Purpose**: Execute retrieval validation with test questions
- **Arguments**:
  - `--question` (str): Specific question to test (optional)
  - `--all`: Run all predefined test questions (optional)
  - `--recreate`: Delete and recreate collection before testing (optional)
- **Output**: Human-readable report of question → results mapping
- **Exit Codes**:
  - 0: Success
  - 1: General error
  - 2: Connection error
  - 3: API error

## Environment Variables
- `QDRANT_URL`: URL of Qdrant instance
- `QDRANT_API_KEY`: API key for Qdrant authentication
- `QDRANT_COLLECTION_NAME`: Name of the collection to search
- `COHERE_API_KEY`: API key for Cohere embedding service

## Data Contracts

### Retrieved Chunk Schema
```json
{
  "content": "string",
  "similarity_score": "float",
  "source_url": "string",
  "title": "string",
  "section": "string",
  "chunk_id": "string"
}
```

### Search Results Schema
```json
{
  "question": "string",
  "results": [
    {
      "content": "string",
      "similarity_score": "float",
      "source_url": "string",
      "title": "string",
      "section": "string",
      "chunk_id": "string"
    }
  ],
  "query_embedding": "list[float]",
  "timestamp": "ISO 8601 datetime"
}
```

## Error Contracts
- All API calls follow standard error handling patterns
- Errors are logged with appropriate context
- Graceful degradation when external services are unavailable