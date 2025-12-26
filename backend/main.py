#!/usr/bin/env python3
"""
RAG Chatbot Data Ingestion Pipeline
Crawls book content, extracts text, generates embeddings, and stores in Qdrant
"""

import asyncio
import argparse
import logging
from typing import List, Dict, Any, Optional, Callable, TypeVar
from dataclasses import dataclass
from urllib.parse import urljoin, urlparse
import os
from dotenv import load_dotenv
import cohere
from qdrant_client import QdrantClient
from qdrant_client.http import models
import httpx
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup
import tiktoken
import time
import json
from functools import wraps


# Load environment variables
load_dotenv()


T = TypeVar('T')


def retry_async(
    max_attempts: int = 3,
    delay: float = 1.0,
    backoff: float = 2.0,
    exceptions: tuple = (Exception,)
):
    """
    Decorator for retrying async functions with exponential backoff
    """
    def decorator(func: Callable[..., T]):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            current_delay = delay
            last_exception = None

            for attempt in range(max_attempts):
                try:
                    return await func(*args, **kwargs)
                except exceptions as e:
                    last_exception = e
                    if attempt == max_attempts - 1:  # Last attempt
                        break
                    await asyncio.sleep(current_delay)
                    current_delay *= backoff

            raise last_exception
        return wrapper
    return decorator


@dataclass
class ContentChunk:
    """A segment of extracted text content with associated metadata that gets converted to embeddings"""
    id: str
    text: str
    url: str
    title: str
    section: str
    created_at: str
    embedding: Optional[List[float]] = None


@dataclass
class CrawledPage:
    """Raw information extracted from a single crawled page before chunking"""
    url: str
    title: str
    content: str
    status_code: int
    crawled_at: str
    links: List[str]


@dataclass
class EmbeddingVector:
    """Numerical representation of text content for semantic search"""
    vector: List[float]
    model: str
    dimension: int
    input_text: str


@dataclass
class Metadata:
    """Additional information stored alongside embeddings for retrieval context"""
    source_url: str
    title: str
    section: str
    chunk_index: int
    created_at: str


class RAGIngestionPipeline:
    """Main class for the RAG ingestion pipeline"""

    def __init__(self):
        self.cohere_client = None
        self.qdrant_client = None
        self.book_url = os.getenv("BOOK_URL", "https://project-physical-ai-text-book.vercel.app/")
        self.collection_name = os.getenv("COLLECTION_NAME", "book_chunks")  # Changed to match retrieve.py expectation
        self.chunk_size = int(os.getenv("CHUNK_SIZE", "500"))
        self.chunk_overlap = int(os.getenv("CHUNK_OVERLAP", "50"))
        self.batch_size = int(os.getenv("BATCH_SIZE", "10"))
        self.rate_limit_delay = float(os.getenv("RATE_LIMIT_DELAY", "0.5"))  # seconds between requests

        # Setup logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)

    def is_valid_url(self, url: str) -> bool:
        """Validate if a URL is properly formatted"""
        try:
            result = urlparse(url)
            return all([result.scheme, result.netloc])
        except Exception:
            return False

    def is_same_domain(self, url: str, base_url: str) -> bool:
        """Check if a URL is from the same domain as the base URL"""
        try:
            base_domain = urlparse(base_url).netloc
            url_domain = urlparse(url).netloc
            return base_domain == url_domain
        except Exception:
            return False

    @retry_async(max_attempts=3, delay=1.0, backoff=2.0, exceptions=(httpx.RequestError, Exception))
    async def fetch_page(self, url: str) -> Optional[str]:
        """Fetch a page with retry logic"""
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.get(url)
                if response.status_code == 200:
                    return response.text
                else:
                    self.logger.warning(f"Failed to fetch {url}: Status {response.status_code}")
                    return None
        except Exception as e:
            self.logger.error(f"Error fetching {url}: {e}")
            raise

    async def extract_links(self, html_content: str, base_url: str) -> List[str]:
        """Extract all valid links from HTML content"""
        try:
            soup = BeautifulSoup(html_content, 'html.parser')
            links = []

            for link in soup.find_all('a', href=True):
                href = link['href']
                # Convert relative URLs to absolute URLs
                absolute_url = urljoin(base_url, href)

                # Only include same-domain URLs
                if self.is_same_domain(absolute_url, base_url):
                    # Remove URL fragments
                    clean_url = absolute_url.split('#')[0]
                    if clean_url not in links and self.is_valid_url(clean_url):
                        links.append(clean_url)

            return links
        except Exception as e:
            self.logger.error(f"Error extracting links: {e}")
            return []

    def extract_content(self, html_content: str) -> Dict[str, Any]:
        """Extract clean content from HTML, removing noise elements"""
        try:
            soup = BeautifulSoup(html_content, 'html.parser')

            # Remove noise elements
            noise_selectors = [
                'nav', 'header', 'footer', 'aside', '.nav', '.header', '.footer',
                '.sidebar', '.advertisement', '.ads', '.cookie-banner',
                '.modal', '.popup', 'script', 'style', 'noscript'
            ]

            for selector in noise_selectors:
                for element in soup.select(selector):
                    element.decompose()

            # Extract title
            title_tag = soup.find('title')
            title = title_tag.get_text().strip() if title_tag else ""

            # Extract main content - prioritize main content areas
            main_content = None
            for selector in ['main', 'article', '.main-content', '.content', '.post-content', '.article-content']:
                main_content = soup.select_one(selector)
                if main_content:
                    break

            if not main_content:
                # Fallback to body if main content not found
                main_content = soup.find('body')

            if main_content:
                # Extract headings, paragraphs, and code blocks
                content_parts = []

                # Process different content types in order of appearance
                for element in main_content.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p', 'pre', 'code', 'li']):
                    text = element.get_text().strip()
                    if text:
                        content_parts.append({
                            'type': element.name,
                            'text': text,
                            'section': self._get_section_header(main_content, element)
                        })

                return {
                    'title': title,
                    'content_parts': content_parts,
                    'full_text': ' '.join([part['text'] for part in content_parts])
                }
            else:
                # If no main content found, extract all text
                text = soup.get_text()
                return {
                    'title': title,
                    'content_parts': [{'type': 'text', 'text': text, 'section': ''}],
                    'full_text': text
                }

        except Exception as e:
            self.logger.error(f"Error extracting content: {e}")
            return {
                'title': '',
                'content_parts': [],
                'full_text': ''
            }

    def _get_section_header(self, main_content, element):
        """Get the closest section header for an element"""
        # Look for the closest heading element before this element
        for prev_element in element.previous_elements:
            if prev_element.name in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
                return prev_element.get_text().strip()
        return ''

    def validate_content(self, content: str) -> bool:
        """Validate content quality"""
        if not content or len(content.strip()) == 0:
            return False

        # Check if content is too short
        if len(content.strip()) < 10:
            return False

        # Check if content is mostly non-alphanumeric (likely noise)
        alphanumeric_ratio = sum(1 for c in content if c.isalnum() or c.isspace()) / len(content)
        if alphanumeric_ratio < 0.5:
            return False

        return True

    def extract_clean_content_from_page(self, crawled_page: CrawledPage) -> Optional[Dict[str, Any]]:
        """Extract and validate clean content from a crawled page"""
        try:
            extracted = self.extract_content(crawled_page.content)

            # Validate the extracted content
            if not self.validate_content(extracted['full_text']):
                self.logger.warning(f"Content validation failed for {crawled_page.url}")
                return None

            # Create a clean page representation
            clean_page = {
                'url': crawled_page.url,
                'title': extracted['title'],
                'content_parts': extracted['content_parts'],
                'full_text': extracted['full_text'],
                'crawled_at': crawled_page.crawled_at
            }

            return clean_page
        except Exception as e:
            self.logger.error(f"Error extracting clean content from {crawled_page.url}: {e}")
            return None

    def chunk_text(self, text: str, max_chunk_size: int, overlap: int) -> List[str]:
        """Split text into overlapping chunks of specified size"""
        if not text:
            return []

        # Use tiktoken to count tokens more accurately
        try:
            encoding = tiktoken.encoding_for_model("gpt-3.5-turbo")
            tokens = encoding.encode(text)
        except:
            # Fallback to simple character-based chunking if tiktoken fails
            tokens = list(text)
            encoding = None

        chunks = []
        start_idx = 0
        text_length = len(tokens)

        while start_idx < text_length:
            # Determine the end index for this chunk
            end_idx = start_idx + max_chunk_size

            # If this is not the last chunk, add overlap
            if end_idx < text_length:
                end_idx += overlap

            # Extract the chunk
            if encoding:
                chunk_tokens = tokens[start_idx:end_idx - overlap if end_idx < text_length else end_idx]
                chunk_text = encoding.decode(chunk_tokens)
            else:
                # For character-based chunking
                chunk_text = ''.join(tokens[start_idx:end_idx - overlap if end_idx < text_length else end_idx])

            chunks.append(chunk_text)

            # Move the start index forward by the chunk size (without overlap)
            start_idx += max_chunk_size

        return chunks

    def chunk_page_content(self, clean_page: Dict[str, Any]) -> List[ContentChunk]:
        """Chunk the content of a clean page into smaller pieces"""
        try:
            # Create chunks from the full text
            text_chunks = self.chunk_text(
                clean_page['full_text'],
                max_chunk_size=self.chunk_size,
                overlap=self.chunk_overlap
            )

            content_chunks = []
            for i, chunk_text in enumerate(text_chunks):
                chunk_id = f"{clean_page['url']}#{i}"

                content_chunk = ContentChunk(
                    id=chunk_id,
                    text=chunk_text,
                    url=clean_page['url'],
                    title=clean_page['title'],
                    section=clean_page.get('content_parts', [{}])[0].get('section', '') if clean_page.get('content_parts') else '',
                    created_at=clean_page['crawled_at']
                )

                content_chunks.append(content_chunk)

            return content_chunks
        except Exception as e:
            self.logger.error(f"Error chunking content for {clean_page['url']}: {e}")
            return []

    def create_metadata(self, content_chunk: ContentChunk, chunk_index: int) -> Metadata:
        """Create metadata for a content chunk"""
        return Metadata(
            source_url=content_chunk.url,
            title=content_chunk.title,
            section=content_chunk.section,
            chunk_index=chunk_index,
            created_at=content_chunk.created_at
        )

    async def crawl_urls(self, start_url: str) -> List[str]:
        """Crawl all accessible URLs starting from the base URL using httpx"""
        visited_urls = set()
        urls_to_visit = {start_url}
        all_urls = set()

        while urls_to_visit:
            current_url = urls_to_visit.pop()

            if current_url in visited_urls:
                continue

            visited_urls.add(current_url)
            all_urls.add(current_url)

            self.logger.info(f"Crawling: {current_url}")

            try:
                # Fetch the page content
                page_content = await self.fetch_page(current_url)
                if page_content:
                    # Extract links from the page
                    new_links = await self.extract_links(page_content, start_url)

                    # Add new links to visit if they haven't been visited
                    for link in new_links:
                        if link not in visited_urls and len(visited_urls) < 1000:  # Prevent infinite crawling
                            urls_to_visit.add(link)
                            all_urls.add(link)

                # Add delay to respect rate limits
                await asyncio.sleep(self.rate_limit_delay)

            except Exception as e:
                self.logger.error(f"Error crawling {current_url}: {e}")
                continue

        return list(all_urls)

    @retry_async(max_attempts=3, delay=1.0, backoff=2.0, exceptions=(Exception,))
    async def crawl_page_with_playwright(self, url: str) -> Optional[CrawledPage]:
        """Crawl a single page using Playwright to handle dynamic content"""
        try:
            async with async_playwright() as p:
                browser = await p.chromium.launch(headless=True)
                page = await browser.new_page()

                # Set a reasonable timeout
                page.set_default_timeout(30000)

                await page.goto(url, wait_until="networkidle")

                # Extract the content after JavaScript execution
                content = await page.content()
                title = await page.title()

                await browser.close()

                crawled_page = CrawledPage(
                    url=url,
                    title=title,
                    content=content,
                    status_code=200,  # Playwright doesn't directly provide status code
                    crawled_at=str(time.time()),
                    links=[]  # We'll extract these separately if needed
                )

                return crawled_page
        except Exception as e:
            self.logger.error(f"Error crawling {url} with Playwright: {e}")
            raise

    async def crawl_all_pages_with_playwright(self, urls: List[str]) -> List[CrawledPage]:
        """Crawl multiple pages using Playwright"""
        crawled_pages = []

        for i, url in enumerate(urls):
            self.logger.info(f"Crawling ({i+1}/{len(urls)}): {url}")
            try:
                crawled_page = await self.crawl_page_with_playwright(url)
                if crawled_page:
                    crawled_pages.append(crawled_page)
            except Exception as e:
                self.logger.error(f"Failed to crawl {url} after retries: {e}")
                continue

        return crawled_pages

    @retry_async(max_attempts=3, delay=1.0, backoff=2.0, exceptions=(Exception,))
    async def generate_embeddings(self, texts: List[str]) -> List[List[float]]:
        """Generate embeddings for a list of texts using Cohere"""
        try:
            # Note: Cohere embed is async, so we keep this as async
            response = await self.cohere_client.embed(
                texts=texts,
                model="embed-english-v3.0",  # Using a reliable Cohere embedding model
                input_type="search_document"  # Appropriate for document search
            )

            embeddings = []
            for item in response.embeddings:
                embeddings.append(item)

            return embeddings
        except Exception as e:
            self.logger.error(f"Error generating embeddings: {e}")
            raise

    async def setup_clients(self):
        """Setup Cohere and Qdrant clients"""
        # Initialize Cohere client
        cohere_api_key = os.getenv("COHERE_API_KEY")
        if not cohere_api_key:
            raise ValueError("COHERE_API_KEY environment variable is required")
        self.cohere_client = cohere.AsyncClient(cohere_api_key)

        # Initialize Qdrant client
        qdrant_url = os.getenv("QDRANT_URL")
        qdrant_api_key = os.getenv("QDRANT_API_KEY")
        if not qdrant_url or not qdrant_api_key:
            raise ValueError("QDRANT_URL and QDRANT_API_KEY environment variables are required")

        self.qdrant_client = QdrantClient(
            url=qdrant_url,
            api_key=qdrant_api_key,
        )

        # Ensure collection exists
        await self._ensure_collection_exists()

    async def check_existing_chunks(self, urls: List[str]) -> set:
        """Check which URLs have already been processed by checking Qdrant for existing chunks"""
        try:
            existing_urls = set()

            # For each URL, check if we have chunks with that source_url
            for url in urls:
                # Search for points with the specific source_url (scroll is synchronous)
                search_result = self.qdrant_client.scroll(
                    collection_name=self.collection_name,
                    scroll_filter=models.Filter(
                        must=[
                            models.FieldCondition(
                                key="source_url",
                                match=models.MatchValue(value=url)
                            )
                        ]
                    ),
                    limit=1  # We just need to know if any exist
                )

                # Check if any results were returned
                points, next_page = search_result
                if points:  # If any points were found
                    existing_urls.add(url)

            return existing_urls
        except Exception as e:
            self.logger.error(f"Error checking existing chunks: {e}")
            return set()  # Return empty set on error, continue processing

    def save_processing_state(self, processed_urls: List[str], filename: str = "processing_state.json"):
        """Save the current processing state to a file"""
        try:
            state = {
                "processed_urls": processed_urls,
                "timestamp": time.time()
            }
            with open(filename, 'w') as f:
                json.dump(state, f)
            self.logger.info(f"Saved processing state for {len(processed_urls)} URLs to {filename}")
        except Exception as e:
            self.logger.error(f"Error saving processing state: {e}")

    def load_processing_state(self, filename: str = "processing_state.json") -> List[str]:
        """Load the processing state from a file"""
        try:
            with open(filename, 'r') as f:
                state = json.load(f)
                processed_urls = state.get("processed_urls", [])
                self.logger.info(f"Loaded processing state with {len(processed_urls)} URLs from {filename}")
                return processed_urls
        except FileNotFoundError:
            self.logger.info(f"Processing state file {filename} not found, starting fresh")
            return []
        except Exception as e:
            self.logger.error(f"Error loading processing state: {e}")
            return []

    def filter_processed_urls(self, all_urls: List[str], processed_urls: List[str]) -> List[str]:
        """Filter out URLs that have already been processed"""
        return [url for url in all_urls if url not in processed_urls]

    def filter_duplicate_chunks(self, content_chunks: List[ContentChunk]) -> List[ContentChunk]:
        """Filter out duplicate content chunks based on content and URL"""
        seen_chunks = set()
        unique_chunks = []

        for chunk in content_chunks:
            # Create a unique identifier based on URL, text content, and section
            chunk_identifier = (chunk.url, chunk.text.strip(), chunk.section)

            if chunk_identifier not in seen_chunks:
                seen_chunks.add(chunk_identifier)
                unique_chunks.append(chunk)

        self.logger.info(f"Filtered {len(content_chunks) - len(unique_chunks)} duplicate chunks")
        return unique_chunks

    @retry_async(max_attempts=3, delay=1.0, backoff=2.0, exceptions=(Exception,))
    async def store_embeddings_in_qdrant(self, content_chunks: List[ContentChunk], embeddings: List[List[float]]):
        """Store content chunks with embeddings in Qdrant vector database"""
        try:
            # Prepare points for Qdrant
            points = []
            for i, (chunk, embedding) in enumerate(zip(content_chunks, embeddings)):
                # Create metadata dictionary
                metadata = {
                    "content": chunk.text,  # Add the actual content
                    "source_url": chunk.url,
                    "title": chunk.title,
                    "section": chunk.section,
                    "created_at": chunk.created_at,
                    "chunk_index": i
                }

                # Create Qdrant point - use UUID format for the ID instead of URL-based string
                import uuid
                point_id = str(uuid.uuid5(uuid.NAMESPACE_URL, f"{chunk.url}#{i}"))

                # Create Qdrant point
                point = models.PointStruct(
                    id=point_id,  # Use UUID for proper Qdrant ID format
                    vector=embedding,
                    payload=metadata
                )
                points.append(point)

            # Upsert points to Qdrant in batches (upsert is synchronous)
            for i in range(0, len(points), self.batch_size):
                batch = points[i:i + self.batch_size]
                self.qdrant_client.upsert(
                    collection_name=self.collection_name,
                    points=batch
                )
                self.logger.info(f"Stored batch of {len(batch)} embeddings in Qdrant")

            self.logger.info(f"Successfully stored {len(points)} embeddings in Qdrant collection: {self.collection_name}")
            return True

        except Exception as e:
            self.logger.error(f"Error storing embeddings in Qdrant: {e}")
            raise

    async def _ensure_collection_exists(self):
        """Create Qdrant collection if it doesn't exist"""
        try:
            # Check if collection exists (get_collections() is synchronous)
            collections = self.qdrant_client.get_collections()
            collection_exists = any(col.name == self.collection_name for col in collections.collections)

            if not collection_exists:
                # Create collection with appropriate vector size (Cohere embeddings are 1024 dimensions)
                self.qdrant_client.create_collection(
                    collection_name=self.collection_name,
                    vectors_config=models.VectorParams(size=1024, distance=models.Distance.COSINE),
                )
                self.logger.info(f"Created Qdrant collection: {self.collection_name}")
            else:
                self.logger.info(f"Qdrant collection {self.collection_name} already exists")
        except Exception as e:
            self.logger.error(f"Error ensuring collection exists: {e}")
            raise


async def main():
    """Main entry point for the RAG ingestion pipeline"""
    parser = argparse.ArgumentParser(description="RAG Chatbot Data Ingestion Pipeline")
    parser.add_argument("--verbose", "-v", action="store_true", help="Enable verbose logging")
    parser.add_argument("--book-url", help="Base URL of the book to crawl")
    parser.add_argument("--limit-urls", type=int, default=10, help="Limit number of URLs to process (for testing)")

    args = parser.parse_args()

    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    pipeline = RAGIngestionPipeline()

    if args.book_url:
        pipeline.book_url = args.book_url

    try:
        print("Initializing pipeline...")
        await pipeline.setup_clients()
        print(f"Pipeline initialized successfully for URL: {pipeline.book_url}")
        print(f"Collection: {pipeline.collection_name}")

        # Discover and crawl all URLs
        print("Starting URL discovery...")
        discovered_urls = await pipeline.crawl_urls(pipeline.book_url)
        print(f"Discovered {len(discovered_urls)} URLs")

        # Show some discovered URLs
        for i, url in enumerate(discovered_urls[:5]):  # Show first 5 URLs
            print(f"  {i+1}. {url}")

        if len(discovered_urls) > 5:
            print(f"  ... and {len(discovered_urls) - 5} more URLs")

        # Crawl pages with Playwright to handle dynamic content
        print("Starting content extraction from discovered URLs...")
        crawled_pages = await pipeline.crawl_all_pages_with_playwright(discovered_urls[:args.limit_urls])
        print(f"Crawled {len(crawled_pages)} pages")

        # Extract clean content from crawled pages
        clean_pages = []
        for page in crawled_pages:
            clean_page = pipeline.extract_clean_content_from_page(page)
            if clean_page:
                clean_pages.append(clean_page)
                print(f"Extracted content from: {page.url}")

        print(f"Successfully extracted clean content from {len(clean_pages)} pages")

        # Check for existing processed URLs to enable idempotent processing
        print("Checking for previously processed URLs...")
        processed_urls = pipeline.load_processing_state()
        existing_urls = await pipeline.check_existing_chunks([page['url'] for page in clean_pages])
        already_processed = set(processed_urls) | existing_urls
        print(f"Found {len(already_processed)} URLs already processed")

        # Filter out already processed URLs
        urls_to_process = [page for page in clean_pages if page['url'] not in already_processed]
        print(f"Will process {len(urls_to_process)} new URLs")

        # Process each clean page: chunk content, generate embeddings, and store in Qdrant
        total_chunks = 0
        processed_urls = list(already_processed)  # Start with already processed URLs

        for i, clean_page in enumerate(urls_to_process):
            print(f"Processing content chunks for: {clean_page['url']} ({i+1}/{len(urls_to_process)})")

            try:
                # Chunk the page content
                content_chunks = pipeline.chunk_page_content(clean_page)
                print(f"Created {len(content_chunks)} content chunks")

                if content_chunks:
                    # Filter out duplicate chunks
                    unique_chunks = pipeline.filter_duplicate_chunks(content_chunks)
                    print(f"Filtered to {len(unique_chunks)} unique chunks")

                    if unique_chunks:
                        # Extract text from chunks for embedding generation
                        texts_to_embed = [chunk.text for chunk in unique_chunks]

                        # Generate embeddings for the chunks
                        print(f"Generating embeddings for {len(texts_to_embed)} chunks...")
                        embeddings = await pipeline.generate_embeddings(texts_to_embed)
                        print(f"Generated {len(embeddings)} embeddings")

                        # Store embeddings in Qdrant
                        print(f"Storing embeddings in Qdrant...")
                        await pipeline.store_embeddings_in_qdrant(unique_chunks, embeddings)
                        total_chunks += len(unique_chunks)

                # Add current URL to processed list and save state
                processed_urls.append(clean_page['url'])
                pipeline.save_processing_state(processed_urls)
                print(f"Successfully processed: {clean_page['url']}")

            except Exception as e:
                print(f"Error processing {clean_page['url']}: {e}")
                continue  # Continue with next page despite error

        print(f"Successfully processed and stored {total_chunks} content chunks in Qdrant")
        print(f"Total URLs processed: {len(processed_urls)}")

        print("Pipeline execution completed successfully!")

    except Exception as e:
        print(f"Error initializing pipeline: {e}")
        logging.exception("Full traceback for pipeline error:")
        return 1

    return 0


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    exit(exit_code)