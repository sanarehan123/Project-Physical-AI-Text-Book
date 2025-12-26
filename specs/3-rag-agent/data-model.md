# Data Model for RAG Agent

## Input Data Structures

### User Query
- question: string - The user's question about the book
- context: string (optional) - Additional context provided by user

## Internal Data Structures

### Query Embedding
- query_text: string - Original question text
- embedding: List[float] - Vector representation of the query
- model: string - Name of the embedding model used

### Retrieved Chunk
- content: string - The text content of the chunk
- similarity_score: float - Cosine similarity score to the query
- source_url: string - URL where the content originated
- title: string - Title of the section/chapter
- section: string - Section identifier
- chunk_id: string - Unique identifier for the chunk

### System Prompt
- instruction: string - The role and constraint instructions
- context: List[RetrievedChunk] - Relevant content chunks to use
- citation_requirement: boolean - Whether to include source citations

### LLM Response
- answer: string - The generated natural language answer
- sources: List[RetrievedChunk] - List of chunks that influenced the response
- confidence_score: float - Estimated confidence in the answer

## Output Data Structure

### Final Response
- generated_answer: string - The final answer to the user's question
- used_sources: List[object] - List of sources with URL and short snippet
- query: string - Original question for reference