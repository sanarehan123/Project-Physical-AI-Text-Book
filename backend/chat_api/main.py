"""
FastAPI backend for RAG Chatbot Integration - Spec 4
T001: Create backend directory structure: `backend/chat_api/`
T006: Create base FastAPI app structure in `backend/chat_api/main.py`
T010: Implement /chat endpoint in `backend/chat_api/main.py` that accepts question and optional context
T011: Add CORS middleware to FastAPI app to allow GitHub Pages domain
"""
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from .models import ChatRequest, ChatResponse, HealthResponse, RAGRequest
from .config import Config
from .services.chat_service import ChatService
from .dependencies import validate_question, validate_context
import os
from datetime import datetime

# Initialize FastAPI app
app = FastAPI(
    title="RAG Chatbot API",
    description="API for RAG Chatbot Integration with Docusaurus",
    version="1.0.0"
)

# Add CORS middleware to allow requests from Docusaurus frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",      # Local Docusaurus development
        "http://localhost:3001",      # Alternative local dev port
        "http://127.0.0.1:3000",      # Local Docusaurus development with 127.0.0.1
        "http://127.0.0.1:3001",      # Alternative local dev port with 127.0.0.1
        "https://*.vercel.app",       # Vercel deployments
        "https://*.github.io",        # GitHub Pages
        "https://*.netlify.app",      # Netlify deployments
        "https://*.pages.dev",        # Cloudflare Pages
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    # Additional origins can be added as needed for deployment
)

@app.get("/")
async def root():
    return {"message": "RAG Chatbot API is running"}

@app.get("/health", response_model=HealthResponse)
async def health_check():
    """
    Health check endpoint to verify the service is running
    """
    return HealthResponse(
        status="ok",
        timestamp=datetime.now().isoformat(),
        version="1.0.0"
    )

@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    """
    Chat endpoint that accepts a question and optional context, then returns an answer with sources
    """
    try:
        # Validate inputs using dependencies
        validated_question = validate_question(request.question)
        validated_context = validate_context(request.context)

        # Process the chat request using the chat service
        result = ChatService.process_chat_request(validated_question, validated_context)

        # Return the response in the expected format
        return ChatResponse(
            answer=result['answer'],
            sources=result['sources']
        )
    except HTTPException:
        # Re-raise HTTP exceptions (like 400 for validation errors)
        raise
    except ValueError as ve:
        # Handle value errors (like empty question)
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        # Handle any other errors (like LLM failures)
        raise HTTPException(status_code=500, detail=f"Failed to process the request: {str(e)}")


@app.post("/rag", response_model=ChatResponse)
async def rag_endpoint(request: RAGRequest):
    """
    RAG endpoint that accepts a query and optional source_url, then returns an answer with sources
    """
    try:
        # Validate inputs
        validated_question = validate_question(request.query)
        validated_context = validate_context(request.source_url) if request.source_url else None

        # Process the RAG request using the chat service
        result = ChatService.process_chat_request(validated_question, validated_context)

        # Return the response in the expected format
        return ChatResponse(
            answer=result['answer'],
            sources=result['sources']
        )
    except HTTPException:
        # Re-raise HTTP exceptions (like 400 for validation errors)
        raise
    except ValueError as ve:
        # Handle value errors (like empty question)
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        # Handle any other errors (like LLM failures)
        raise HTTPException(status_code=500, detail=f"Failed to process the request: {str(e)}")

# Validate configuration on startup
try:
    Config.validate()
except ValueError as e:
    print(f"Configuration error: {e}")
    raise

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8002)