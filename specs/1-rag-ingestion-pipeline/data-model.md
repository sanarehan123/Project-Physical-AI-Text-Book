# Data Model: RAG Chatbot Data Ingestion Pipeline

## Content Chunk Entity

**Description**: A segment of extracted text content with associated metadata that gets converted to embeddings

**Fields**:
- `id`: Unique identifier (derived from URL + chunk index)
- `text`: The actual text content of the chunk
- `url`: Source URL where the content was found
- `title`: Page title from the source
- `section`: Section or heading under which the content appears
- `created_at`: Timestamp when the chunk was created
- `embedding`: Vector representation of the text content

**Validation Rules**:
- `text` must not be empty
- `url` must be a valid URL format
- `text` length should be within 400-600 token range (approximately 1000-2000 characters)

## Crawled Page Entity

**Description**: Raw information extracted from a single crawled page before chunking

**Fields**:
- `url`: The URL of the page
- `title`: The page title
- `content`: The cleaned HTML or text content
- `status_code`: HTTP status code from the crawl
- `crawled_at`: Timestamp when the page was crawled
- `links`: Array of URLs found on the page (for navigation)

**Validation Rules**:
- `url` must be a valid URL format
- `content` must not be empty after cleaning

## Embedding Vector Entity

**Description**: Numerical representation of text content for semantic search

**Fields**:
- `vector`: Array of floating point numbers representing the embedding
- `model`: Name/version of the model used to generate the embedding
- `dimension`: Number of dimensions in the vector
- `input_text`: Original text that was embedded (for reference)

**Validation Rules**:
- `vector` must have consistent dimensions based on the model used
- `model` must match the configured embedding model

## Metadata Entity

**Description**: Additional information stored alongside embeddings for retrieval context

**Fields**:
- `source_url`: Original URL of the content
- `title`: Title of the source page
- `section`: Section or heading where content appeared
- `chunk_index`: Position of this chunk within the original page
- `created_at`: Timestamp when the metadata was created

**Validation Rules**:
- `source_url` must be a valid URL
- `chunk_index` must be a non-negative integer