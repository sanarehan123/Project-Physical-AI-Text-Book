# Quickstart: RAG Chatbot Data Ingestion Pipeline

## Prerequisites

- Python 3.11 or higher
- UV package manager
- Access to Cohere API
- Access to Qdrant cloud instance

## Setup

1. **Clone the repository and navigate to the backend directory**:
   ```bash
   cd backend
   ```

2. **Install dependencies using UV**:
   ```bash
   uv init
   uv add cohere qdrant-client playwright python-dotenv httpx
   ```

3. **Set up environment variables**:
   ```bash
   cp .env.example .env
   ```

   Then edit `.env` with your actual values:
   ```env
   COHERE_API_KEY=your_cohere_api_key_here
   QDRANT_URL=your_qdrant_cluster_url_here
   QDRANT_API_KEY=your_qdrant_api_key_here
   BOOK_URL=https://project-physical-ai-text-book-updat.vercel.app/
   COLLECTION_NAME=book_content
   ```

## Usage

### Run the full ingestion pipeline

```bash
uv run python main.py
```

### Run with specific options

```bash
# Run with verbose logging
uv run python main.py --verbose

# Crawl a specific subpath
uv run python main.py --base-url https://project-physical-ai-text-book-updat.vercel.app/guide
```

## Project Structure

```
backend/
├── main.py              # Main ingestion pipeline implementation
├── .env.example         # Example environment variables
├── .gitignore           # Git ignore file
├── pyproject.toml       # Project configuration
├── README.md            # Project documentation
└── tests/
    └── test_main.py     # Tests for the pipeline
```

## Key Components

1. **Crawler**: Uses Playwright to navigate and extract content from the book site
2. **Content Extractor**: Cleans HTML and extracts relevant text content
3. **Chunker**: Splits content into 400-600 token chunks with overlap
4. **Embedder**: Generates vector embeddings using Cohere
5. **Vector Store**: Stores embeddings and metadata in Qdrant

## Configuration

The pipeline can be configured through environment variables in the `.env` file:

- `BOOK_URL`: Base URL of the book to crawl
- `COLLECTION_NAME`: Name of the Qdrant collection to use
- `CHUNK_SIZE`: Target size for text chunks (in tokens)
- `CHUNK_OVERLAP`: Overlap between chunks (in tokens)
- `BATCH_SIZE`: Number of chunks to process in each batch