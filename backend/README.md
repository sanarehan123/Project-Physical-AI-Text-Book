# RAG Chatbot Data Ingestion Pipeline

This project implements a data ingestion pipeline that crawls the deployed book URL, extracts and cleans content, generates Cohere embeddings, and stores them in a Qdrant vector database for RAG (Retrieval Augmented Generation) applications.

## Features

- **Automated Crawling**: Discovers and processes all pages from the book URL
- **Content Extraction**: Extracts clean textual content while removing noise (navigation, footer, etc.)
- **Embedding Generation**: Generates high-quality embeddings using Cohere
- **Vector Storage**: Stores embeddings and metadata in Qdrant vector database
- **Idempotent Processing**: Safe to run multiple times without creating duplicates
- **Resilient Operation**: Handles rate limits and failures gracefully

## Prerequisites

- Python 3.11+
- UV package manager
- Access to Cohere API
- Access to Qdrant vector database

## Setup

1. **Install dependencies**:
   ```bash
   cd backend
   uv sync
   ```

2. **Install Playwright browsers**:
   ```bash
   uv run playwright install
   ```

3. **Configure environment variables**:
   ```bash
   cp .env.example .env
   # Edit .env with your actual values
   ```

## Usage

Run the full ingestion pipeline:
```bash
uv run python main.py
```

Run with specific options:
```bash
# Run with verbose logging
uv run python main.py --verbose

# Crawl a specific book URL
uv run python main.py --book-url https://example-book.com

# Limit number of URLs to process (for testing)
uv run python main.py --limit-urls 5
```

## Configuration

The pipeline can be configured through environment variables in the `.env` file:

- `COHERE_API_KEY`: Your Cohere API key
- `QDRANT_URL`: URL of your Qdrant cluster
- `QDRANT_API_KEY`: Your Qdrant API key
- `COLLECTION_NAME`: Name of the Qdrant collection to use
- `BOOK_URL`: Base URL of the book to crawl
- `CHUNK_SIZE`: Target size for text chunks (in tokens)
- `CHUNK_OVERLAP`: Overlap between chunks (in tokens)
- `BATCH_SIZE`: Number of chunks to process in each batch
- `RATE_LIMIT_DELAY`: Delay in seconds between requests (default: 0.5)

## Project Structure

- `main.py`: Single file implementation with modular functions
- `tests/`: Test directory
- `pyproject.toml`: Project configuration
- `.env.example`: Example environment variables file