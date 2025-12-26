# Data Model: RAG Chatbot Retrieval Pipeline

## Core Entities

### Test Question
- **Description**: A realistic user query about book content used to validate retrieval quality
- **Fields**:
  - `id`: Unique identifier for the test question
  - `text`: The actual question text
  - `category`: Topic area or book section the question relates to
  - `expected_concepts`: Key concepts that should be found in relevant results
  - `purpose`: Brief explanation of what this question tests

### Retrieved Chunk
- **Description**: A content segment returned by the vector search with similarity score and metadata
- **Fields**:
  - `content`: The actual text content of the retrieved chunk
  - `similarity_score`: Cosine similarity score (0.0-1.0) indicating relevance to query
  - `source_url`: URL where the original content was sourced from
  - `title`: Title of the source document/chapter
  - `section`: Specific section or chapter where the content appears
  - `chunk_id`: Identifier for this specific chunk in the vector database

### Query Embedding
- **Description**: Vector representation of a test question for semantic search
- **Fields**:
  - `vector`: Numerical vector representation of the query
  - `model`: Name of the embedding model used
  - `text`: Original query text that was embedded

### Retrieval Result
- **Description**: Complete result set for a single test question
- **Fields**:
  - `question`: The original test question
  - `top_chunks`: Array of Retrieved Chunk objects (top 3-5 results)
  - `query_embedding`: The Query Embedding used for search
  - `timestamp`: When the retrieval was performed
  - `relevance_score`: Overall assessment of result quality

## Relationships

### Test Question → Retrieval Result (1:1)
- Each test question produces one retrieval result set
- The retrieval result contains the original question and all retrieved chunks

### Retrieval Result → Retrieved Chunk (1:M)
- Each retrieval result contains multiple retrieved chunks
- Typically top 3-5 chunks with highest similarity scores

### Query Embedding → Retrieval Result (1:1)
- Each retrieval result is based on a single query embedding
- The embedding is generated from the original test question

## Validation Rules

### From Requirements:
1. **Similarity Threshold**: All relevant chunks must have similarity scores > 0.78
2. **Metadata Completeness**: Each retrieved chunk must include URL, title, and section
3. **Content Relevance**: Retrieved chunks must contain semantic matches to expected answers
4. **Result Count**: Each query should return top 3 most relevant chunks

### Data Integrity:
1. **Non-empty Content**: Retrieved chunks must have meaningful content
2. **Valid Scores**: Similarity scores must be between 0.0 and 1.0
3. **Valid URLs**: Source URLs must be properly formatted
4. **No Duplicates**: Within a single result set, avoid duplicate content chunks

## State Transitions (if applicable)

### Retrieval Process:
1. **PENDING**: Test question ready for retrieval
2. **EMBEDDING**: Query embedding in progress
3. **SEARCHING**: Vector search in progress
4. **RESULTS_READY**: Retrieval completed with results
5. **VALIDATED**: Results manually validated for quality