# Research: RAG Chatbot Integration – Spec 4

## Existing System Analysis

### Current Agent Implementation
- **Location**: `backend/agent.py`
- **Functionality**: CLI-based RAG agent that uses Cohere for embeddings, Qdrant for retrieval, and OpenAI-compatible Gemini for responses
- **Key Components**:
  - `embed_query()`: Generates embeddings using Cohere
  - `retrieve_chunks()`: Searches Qdrant for relevant content
  - `generate_response()`: Creates contextual responses with Gemini API
  - Environment variables: GEMINI_API_KEY, COHERE_API_KEY, QDRANT_URL, QDRANT_API_KEY

### API Keys and Services
- **GEMINI_API_KEY**: Google Gemini API key for response generation
- **COHERE_API_KEY**: Cohere API key for embeddings
- **QDRANT_URL/QDRANT_API_KEY**: Vector database access
- **Model**: gemini-2.5-flash (free tier)

## Technology Research

### FastAPI for Backend
- **Advantages**:
  - Python-based with Pydantic validation
  - Automatic OpenAPI documentation
  - Built-in async support
  - Excellent for REST APIs
- **CORS Handling**: Built-in middleware for cross-origin requests

### React Component for Docusaurus
- **Integration Options**:
  - Floating action button widget
  - Sidebar component
  - Embedded chat area
- **State Management**: React hooks for message history and loading states
- **API Communication**: Fetch API or axios for backend communication

### Architecture Patterns
- **Microservice**: Separate backend service for RAG processing
- **API Gateway Pattern**: Single endpoint for chat requests
- **CORS Configuration**: Allow GitHub Pages domain access

## Implementation Approaches

### Approach 1: Direct Agent Integration
- **Method**: Import functions from existing `agent.py`
- **Pros**: Reuse existing tested logic, minimal duplication
- **Cons**: Potential import conflicts, dependency management

### Approach 2: Service Layer Abstraction
- **Method**: Create new service files based on agent.py logic
- **Pros**: Clean separation, testability, maintainability
- **Cons**: Some code duplication

### Approach 3: Agent Module Conversion
- **Method**: Convert agent.py into importable module
- **Pros**: Single source of truth, reusable components
- **Cons**: Requires refactoring existing CLI functionality

## Recommended Approach

**Approach 2 (Service Layer Abstraction)** is recommended because:
1. It maintains clean separation between CLI and API usage
2. Allows for API-specific error handling and validation
3. Enables easier testing of the RAG service
4. Minimizes changes to existing working CLI code

## API Design Research

### Request/Response Schema
```
POST /chat
Request: {
  "question": "string",
  "context": "string" (optional)
}

Response: {
  "answer": "string",
  "sources": [
    {
      "url": "string",
      "text": "string"
    }
  ]
}
```

### Error Handling
- 400: Invalid request format
- 422: Validation errors
- 500: Internal processing errors
- 503: External service unavailable

## Docusaurus Integration Research

### Component Structure
- **ChatWidget**: Main container with input/output areas
- **ChatMessage**: Individual message display with source links
- **State Management**: Loading, error, and message history states

### Deployment Considerations
- GitHub Pages requires static assets only
- Backend API must be hosted separately
- CORS headers must allow GitHub Pages domain
- Environment variable for backend URL configuration

## Security Considerations

### API Key Management
- Environment variables for all API keys
- Server-side only (not exposed to frontend)
- Proper validation and sanitization of inputs

### Rate Limiting
- Implementation needed to prevent abuse
- Consider using external services or middleware

### Input Validation
- Sanitize user inputs
- Prevent injection attacks
- Limit request sizes

## Performance Research

### Caching Strategies
- Consider caching for frequent queries
- Cache at service level or use Redis

### Response Time Optimization
- Async processing where possible
- Connection pooling to external services
- Proper error handling to prevent timeouts

## Dependencies Analysis

### Backend Dependencies
- fastapi: Web framework
- uvicorn: ASGI server
- pydantic: Data validation
- openai: OpenAI-compatible API client
- cohere: Embedding service client
- qdrant-client: Vector database client
- python-dotenv: Environment variable management

### Frontend Dependencies
- React: Component framework
- Standard Docusaurus setup
- CSS modules for styling

## Risk Assessment

### High Risk Items
1. **CORS Configuration**: GitHub Pages domain restrictions
2. **API Key Security**: Ensuring keys are not exposed
3. **External Service Reliability**: Dependency on Gemini, Cohere, Qdrant

### Mitigation Strategies
1. **CORS**: Proper configuration with specific origin allowlist
2. **Security**: Server-side API key management only
3. **Reliability**: Proper error handling and fallbacks