# Data Ingestion Contract: RAG Chatbot Pipeline

## Overview

This contract defines the data flow and interfaces for the RAG Chatbot Data Ingestion Pipeline. The pipeline processes web content from the book site and transforms it into vector embeddings stored in Qdrant.

## Data Flow Contract

### 1. Input Interface
- **Source**: Web pages from BOOK_URL (https://project-physical-ai-text-book.vercel.app/)
- **Format**: HTML content
- **Access Method**: Playwright browser automation
- **Authentication**: None required (public site)

### 2. Processing Interface
- **Content Extraction**: HTML parsing to extract text content (title, headings, paragraphs, code blocks)
- **Noise Filtering**: Remove navigation, footer, scripts, and other non-content elements
- **Chunking**: Split content into 400-600 token chunks with overlap
- **Validation**: Ensure chunks meet quality criteria

### 3. Embedding Interface
- **Model**: Cohere embedding model (latest suitable version)
- **Input**: Text chunks (400-600 tokens)
- **Output**: Vector embeddings
- **Format**: Array of floating-point numbers

### 4. Storage Interface
- **Destination**: Qdrant vector database
- **Collection**: Configured COLLECTION_NAME
- **Vector Size**: Determined by Cohere model used
- **Metadata**: URL, title, section, and other contextual information

## Quality Assurance Contract

### Content Extraction Quality
- **Noise Removal**: At least 95% accuracy in removing navigation, footer, and UI elements
- **Content Preservation**: All main content (headings, paragraphs, code blocks) must be preserved
- **Structure Retention**: Maintain semantic structure of the content

### Embedding Quality
- **Response Time**: Embedding generation should complete within 5 seconds per chunk
- **Consistency**: Similar content should produce similar embeddings
- **Model Version**: Use latest suitable Cohere model version

### Storage Quality
- **Success Rate**: 99.9% success rate for storing embeddings
- **Metadata Completeness**: All required metadata fields must be present
- **Idempotency**: Re-running the process should not create duplicate entries

## Error Handling Contract

### Crawler Errors
- **Network Failures**: Implement retry logic with exponential backoff
- **Rate Limits**: Detect and respect rate limiting, add appropriate delays
- **Page Not Found**: Log and continue processing other pages

### Processing Errors
- **Content Extraction Failures**: Skip problematic content and continue
- **Chunking Errors**: Log and continue with remaining content
- **Invalid Content**: Skip content that doesn't meet quality criteria

### Storage Errors
- **Qdrant Connection**: Retry with exponential backoff
- **Authentication Failures**: Fail the process with clear error message
- **Quota Exceeded**: Stop processing and report the issue

## Performance Contract

### Processing Performance
- **Crawling Speed**: Process all pages within reasonable time (under 30 minutes for full book)
- **Embedding Speed**: Generate embeddings efficiently with batch processing where possible
- **Memory Usage**: Process large sites without excessive memory consumption

### Resilience
- **Partial Failure**: Continue processing when individual pages fail
- **Resume Capability**: Ability to resume from where the process left off
- **Idempotency**: Safe to run multiple times without creating duplicates