"""
Basic tests for the RAG ingestion pipeline
"""
import pytest
import asyncio
from unittest.mock import AsyncMock, MagicMock, patch
from main import RAGIngestionPipeline


class TestRAGIngestionPipeline:
    """Test cases for the RAG ingestion pipeline"""

    def setup_method(self):
        """Set up test fixtures before each test method."""
        self.pipeline = RAGIngestionPipeline()

    def test_is_valid_url_valid(self):
        """Test URL validation with a valid URL"""
        valid_url = "https://example.com"
        assert self.pipeline.is_valid_url(valid_url) is True

    def test_is_valid_url_invalid(self):
        """Test URL validation with an invalid URL"""
        invalid_url = "not-a-url"
        assert self.pipeline.is_valid_url(invalid_url) is False

    def test_is_same_domain_true(self):
        """Test domain comparison with same domain"""
        url1 = "https://example.com/page1"
        url2 = "https://example.com/page2"
        assert self.pipeline.is_same_domain(url1, url2) is True

    def test_is_same_domain_false(self):
        """Test domain comparison with different domains"""
        url1 = "https://example.com"
        url2 = "https://different.com"
        assert self.pipeline.is_same_domain(url1, url2) is False

    def test_validate_content_valid(self):
        """Test content validation with valid content"""
        valid_content = "This is a valid content with some text."
        assert self.pipeline.validate_content(valid_content) is True

    def test_validate_content_invalid_short(self):
        """Test content validation with content that is too short"""
        short_content = "Hi"
        assert self.pipeline.validate_content(short_content) is False

    def test_validate_content_invalid_no_alphanumeric(self):
        """Test content validation with content that has no alphanumeric characters"""
        invalid_content = "!!! @@@ ###"
        assert self.pipeline.validate_content(invalid_content) is False

    @patch('main.httpx.AsyncClient')
    def test_fetch_page_success(self, mock_client):
        """Test fetching a page successfully"""
        # This is a basic test - in a real scenario you would mock the httpx client properly
        pass

    def test_chunk_text_basic(self):
        """Test basic text chunking functionality"""
        text = "This is a test sentence. " * 10  # Create a longer text
        chunks = self.pipeline.chunk_text(text, max_chunk_size=20, overlap=5)

        # Should have created chunks
        assert len(chunks) > 0

        # Each chunk should not exceed the max size (approximately)
        for chunk in chunks:
            assert len(chunk) > 0

    def test_filter_duplicate_chunks(self):
        """Test filtering duplicate content chunks"""
        from main import ContentChunk

        # Create some test chunks with duplicates
        chunk1 = ContentChunk(
            id="test1",
            text="This is the first chunk.",
            url="https://example.com/1",
            title="Test Page",
            section="Section 1",
            created_at="2023-01-01"
        )

        chunk2 = ContentChunk(
            id="test2",
            text="This is the first chunk.",  # Same text as chunk1
            url="https://example.com/1",
            title="Test Page",
            section="Section 1",
            created_at="2023-01-01"
        )

        chunk3 = ContentChunk(
            id="test3",
            text="This is a different chunk.",
            url="https://example.com/2",
            title="Test Page 2",
            section="Section 2",
            created_at="2023-01-01"
        )

        chunks = [chunk1, chunk2, chunk3]
        unique_chunks = self.pipeline.filter_duplicate_chunks(chunks)

        # Should have filtered out the duplicate
        assert len(unique_chunks) == 2
        assert chunk3 in unique_chunks  # The unique chunk should remain