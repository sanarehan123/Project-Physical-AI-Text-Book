from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import os
import logging
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient
import uvicorn

# Load environment variables
load_dotenv()

# Initialize logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(title="RAG API for Docusaurus Book", version="1.0.0")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://project-physical-ai-text-book-c5mvhfw7z-sana-rehans-projects.vercel.app",
        "http://localhost",
        "http://localhost:3000",
        "http://localhost:8000",
        "http://127.0.0.1",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:8000"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_vector_store():
    """Initialize and return the Qdrant vector store - called when needed"""
    qdrant_client = QdrantClient(
        url=os.getenv("QDRANT_URL"),
        api_key=os.getenv("QDRANT_API_KEY"),
    )

    embeddings = OpenAIEmbeddings(
        model="text-embedding-3-small",
        openai_api_key=os.getenv("OPENAI_API_KEY")
    )

    vector_store = QdrantVectorStore(
        client=qdrant_client,
        collection_name="book_chunks",  # This should match your ingestion script
        embedding=embeddings,
    )

    return vector_store

# Initialize OpenAI LLM
llm = ChatOpenAI(
    model="gpt-4o-mini",  # Using gpt-4o-mini as requested
    openai_api_key=os.getenv("OPENAI_API_KEY"),
    temperature=0.1
)

# Request models
class QueryRequest(BaseModel):
    query: str
    source_url: Optional[str] = None

# Response models
class QueryResponse(BaseModel):
    answer: str
    sources: List[str]

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "ok"}

@app.post("/rag", response_model=QueryResponse)
async def rag_query(request: QueryRequest):
    """RAG endpoint that retrieves relevant chunks and generates an answer"""
    try:
        logger.info(f"Received query: {request.query}")
        logger.info(f"Source filter: {request.source_url}")

        # Get vector store (this will initialize it when needed)
        vector_store = get_vector_store()

        # Prepare search filters based on source_url if provided
        filter_dict = None
        if request.source_url:
            # Create a filter to match documents with the specified source_url
            # Based on the ingestion script, the field is stored as "source"
            filter_dict = {"source": request.source_url}

        # Perform similarity search to retrieve relevant chunks
        # Using similarity search to get top 8 relevant chunks
        relevant_docs = vector_store.similarity_search(
            request.query,
            k=8,
            filter=filter_dict
        )

        logger.info(f"Retrieved {len(relevant_docs)} relevant documents")

        # Build context from retrieved documents
        context_parts = []
        source_urls = set()

        for doc in relevant_docs:
            content = doc.page_content
            source = doc.metadata.get("source", "")

            if content:
                context_parts.append(content)
            if source:
                source_urls.add(source)

        context = "\n\n".join(context_parts)
        logger.info(f"Context length: {len(context)} characters")

        # If no context found, return a helpful message
        if not context.strip():
            return QueryResponse(
                answer="I couldn't find any relevant information in the book to answer your question.",
                sources=[]
            )

        # Create the prompt for the LLM
        prompt = f"""
        You are an assistant for a Physical AI textbook. Answer the user's question based strictly on the provided context from the textbook.
        If the answer cannot be found in the context, say so clearly.

        Context:
        {context}

        Question: {request.query}

        Answer:
        """

        # Generate the answer using the LLM
        response = llm.invoke(prompt)
        answer = response.content

        logger.info("Successfully generated answer")

        return QueryResponse(
            answer=answer,
            sources=list(source_urls)
        )

    except Exception as e:
        logger.error(f"Error processing query: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error processing query: {str(e)}")

if __name__ == "__main__":
    # Run the server on localhost:8000
    uvicorn.run(app, host="0.0.0.0", port=8000)