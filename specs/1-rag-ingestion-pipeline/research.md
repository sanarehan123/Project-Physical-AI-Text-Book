# Research: RAG Chatbot Data Ingestion Pipeline

## Decision: Choose crawling library (Playwright vs requests+BeautifulSoup)

**Rationale**: Playwright was selected based on the user's input requirements. Playwright is better for dynamic content and JavaScript-heavy sites like Docusaurus, while requests+BeautifulSoup works well for static content. Since Docusaurus sites may have dynamic elements, Playwright provides more robust crawling capabilities.

**Alternatives considered**:
- requests + BeautifulSoup: Good for static content, simpler setup
- Scrapy: More powerful for complex crawling, but potentially overkill for this use case
- Selenium: Similar to Playwright but heavier

## Decision: Cohere embedding model selection

**Rationale**: Using Cohere's latest suitable embed model as specified in the requirements. Cohere's embed-multilingual-v3.0 or embed-english-v3.0 are likely candidates depending on the content language.

**Alternatives considered**:
- OpenAI embeddings: Alternative option but not requested
- Hugging Face models: Self-hosted option but adds complexity
- Sentence Transformers: Open source alternative but not requested

## Decision: Qdrant vector database setup

**Rationale**: Using Qdrant cloud tier as specified in requirements. Qdrant is efficient for similarity search and has good Python client support.

**Alternatives considered**:
- Pinecone: Alternative vector database but not requested
- Weaviate: Alternative vector database but not requested
- Chroma: Open source option but cloud tier preferred

## Decision: Content chunking strategy

**Rationale**: Fixed chunking of ~400-600 tokens with overlap as specified in requirements. This provides a good balance between context preservation and retrieval efficiency.

**Alternatives considered**:
- Semantic chunking: More sophisticated but potentially more complex
- Recursive chunking: Standard approach but fixed size requested
- Code-aware chunking: For code-heavy content but not specifically requested

## Decision: Idempotent processing approach

**Rationale**: Using URL-based document IDs in Qdrant to enable idempotent processing. When the same URL is processed again, it will overwrite the existing entry rather than creating a duplicate.

**Alternatives considered**:
- Timestamp-based filtering: More complex logic required
- Content hash comparison: Potential for false positives/negatives
- Separate tracking database: Adds complexity but could work

## Decision: Rate limiting and retry strategy

**Rationale**: Implementing exponential backoff with configurable delays to handle rate limits gracefully. This ensures the crawler doesn't overwhelm the target server while maintaining reliability.

**Alternatives considered**:
- Fixed delay: Simpler but less adaptive
- No delays: Could cause issues with rate limits
- Random delays: Could be less predictable