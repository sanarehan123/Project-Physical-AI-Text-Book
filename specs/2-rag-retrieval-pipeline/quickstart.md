# Quickstart: RAG Chatbot Retrieval Pipeline

## Prerequisites

1. **Python 3.11+** installed on your system
2. **Environment variables** configured:
   - `QDRANT_URL`: URL of your Qdrant instance
   - `QDRANT_API_KEY`: API key for Qdrant authentication
   - `QDRANT_COLLECTION_NAME`: Name of the collection created in Spec 1
   - `COHERE_API_KEY`: API key for Cohere embedding service

3. **Installed dependencies** (install with pip):
   - qdrant-client
   - cohere
   - python-dotenv

## Setup

1. **Clone the repository** (if not already done):
   ```bash
   git clone <repository-url>
   cd <repository-name>
   ```

2. **Navigate to the backend directory**:
   ```bash
   cd backend/
   ```

3. **Install dependencies**:
   ```bash
   pip install qdrant-client cohere python-dotenv
   ```

4. **Create or update your `.env` file** with the required environment variables:
   ```env
   QDRANT_URL=your_qdrant_url
   QDRANT_API_KEY=your_qdrant_api_key
   QDRANT_COLLECTION_NAME=your_collection_name
   COHERE_API_KEY=your_cohere_api_key
   ```

## Usage

### Run All Test Questions
Execute the retrieval script with all predefined test questions:
```bash
python retrieve.py --all
```

### Test a Specific Question
Test a specific question directly:
```bash
python retrieve.py --question "What is the principle of least action in physics?"
```

### Advanced Options
- **Recreate collection**: If the collection seems corrupted or incomplete:
  ```bash
  python retrieve.py --all --recreate
  ```

## Expected Output

The script will output results in the following format:

```
Question: [Your test question]
─────────────────────────────────────────────────────────────────────────────
Retrieved Results:
1. [Content chunk text...] (Score: 0.XX, Source: https://example.com/section)
2. [Content chunk text...] (Score: 0.XX, Source: https://example.com/section)
3. [Content chunk text...] (Score: 0.XX, Source: https://example.com/section)
─────────────────────────────────────────────────────────────────────────────
Relevance Check: [PASS/FAIL] - X/X relevant results above 0.78 threshold
```

## Troubleshooting

1. **Connection errors**: Verify QDRANT_URL and QDRANT_API_KEY are correct
2. **API errors**: Check COHERE_API_KEY and ensure you have access to the embedding service
3. **No results**: Verify that the Qdrant collection from Spec 1 was created successfully
4. **Low similarity scores**: This may indicate issues with the ingestion pipeline or embedding consistency

## Next Steps

After validating retrieval quality:
1. Review the similarity scores and content relevance
2. Identify any patterns in retrieval failures
3. Proceed to Spec 3 for LLM-based answer generation