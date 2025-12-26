# Data Model: RAG Chatbot Integration – Spec 4

## API Data Models

### Request Models

#### ChatRequest
**Purpose**: Represents a user's chat request to the backend
**Location**: `backend/chat_api/models.py`

| Field | Type | Validation | Description |
|-------|------|------------|-------------|
| question | string | Required, minLength: 1, maxLength: 2000 | The user's question |
| context | string | Optional, maxLength: 5000 | Additional context for the question |

**Example**:
```json
{
  "question": "What is the principle of least action?",
  "context": "I'm studying physics concepts"
}
```

### Response Models

#### ChatResponse
**Purpose**: Represents the backend's response to a chat request
**Location**: `backend/chat_api/models.py`

| Field | Type | Validation | Description |
|-------|------|------------|-------------|
| answer | string | Required | The generated answer to the question |
| sources | array[SourceReference] | Required | List of sources used in the response |

**Example**:
```json
{
  "answer": "The principle of least action states that the path taken by a system between two states is the one for which the action is minimized...",
  "sources": [
    {
      "url": "https://example.com/book/chapter-5",
      "text": "The principle of least action is a variational principle that, when applied to the action of a mechanical system, can be used to obtain the equations of motion for that system."
    }
  ]
}
```

#### SourceReference
**Purpose**: Represents a source document used in generating the response
**Location**: `backend/chat_api/models.py`

| Field | Type | Validation | Description |
|-------|------|------------|-------------|
| url | string | Required, valid URL format | URL to the source document |
| text | string | Required | Relevant text snippet from the source |

**Example**:
```json
{
  "url": "https://project-physical-ai-text-book.vercel.app/docs/module-1/chapter-3",
  "text": "The principle of least action is a variational principle that, when applied to the action of a mechanical system, can be used to obtain the equations of motion for that system."
}
```

## Internal Data Models

### QueryContext
**Purpose**: Internal representation of the user's query with additional metadata
**Location**: `backend/chat_api/services/chat_service.py`

| Field | Type | Description |
|-------|------|-------------|
| question | string | The original user question |
| context | string | Additional user-provided context |
| embedding | List[float] | Vector representation of the query |
| timestamp | datetime | When the query was processed |

### RetrievedChunk
**Purpose**: Represents a chunk of content retrieved from the vector database
**Location**: `backend/chat_api/services/rag_agent.py`

| Field | Type | Description |
|-------|------|-------------|
| content | string | The content of the retrieved chunk |
| similarity_score | float | Similarity score from vector search |
| source_url | string | URL where the content originated |
| title | string | Title of the source document |
| section | string | Section within the source document |
| chunk_id | string | Unique identifier for the chunk |

### GeneratedResponse
**Purpose**: Internal representation of the AI-generated response
**Location**: `backend/chat_api/services/rag_agent.py`

| Field | Type | Description |
|-------|------|-------------|
| answer | string | The generated answer text |
| sources | List[RetrievedChunk] | Source chunks used to generate the response |
| model_used | string | The AI model that generated the response |
| tokens_used | int | Number of tokens in the response |

## Frontend Data Models

### ChatMessage
**Purpose**: Represents a single message in the chat interface
**Location**: `physical-ai-textbook/src/components/ChatWidget/ChatMessage.jsx`

| Field | Type | Description |
|-------|------|-------------|
| id | string | Unique identifier for the message |
| content | string | The message content |
| role | 'user' or 'assistant' | Who sent the message |
| timestamp | Date | When the message was created |
| sources | Array<SourceReference> | Sources for assistant messages |

### ChatState
**Purpose**: Represents the state of the chat interface
**Location**: `physical-ai-textbook/src/components/ChatWidget/ChatWidget.jsx`

| Field | Type | Description |
|-------|------|-------------|
| messages | Array<ChatMessage> | All messages in the current chat |
| isLoading | boolean | Whether a response is being generated |
| error | string or null | Any error message |
| isOpen | boolean | Whether the chat widget is open |

## Environment Variables

### Backend Environment Variables
**Location**: `.env` file in backend directory

| Variable | Type | Description | Required |
|----------|------|-------------|----------|
| GEMINI_API_KEY | string | Google Gemini API key | Yes |
| COHERE_API_KEY | string | Cohere API key | Yes |
| QDRANT_URL | string | URL for Qdrant vector database | Yes |
| QDRANT_API_KEY | string | API key for Qdrant database | Yes |
| QDRANT_COLLECTION_NAME | string | Name of the collection in Qdrant | No (default: book_chunks) |
| CORS_ORIGINS | string | Comma-separated list of allowed origins | No (default: all) |

### Frontend Environment Variables
**Location**: `physical-ai-textbook/.env` file

| Variable | Type | Description | Required |
|----------|------|-------------|----------|
| REACT_APP_BACKEND_URL | string | URL of the backend API | Yes |

## Data Flow

### Request Flow
1. User submits question via frontend chat widget
2. Frontend sends ChatRequest to backend `/chat` endpoint
3. Backend validates ChatRequest using Pydantic model
4. Backend processes request using internal data models
5. Backend returns ChatResponse using response model
6. Frontend displays ChatResponse in chat interface

### Error Flow
1. If validation fails, backend returns 422 with validation details
2. If processing fails, backend returns 500 with error details
3. Frontend handles errors and displays appropriate messages

## Validation Rules

### Request Validation
- Question must be 1-2000 characters
- Context (if provided) must be 1-5000 characters
- Question must not be empty or whitespace only
- Question must contain only printable characters

### Response Validation
- Answer must not be empty
- Sources array must contain at least one source if answer is provided
- Each source must have valid URL format
- Each source text must be meaningful (not empty)

### Internal Validation
- Embeddings must be valid float arrays
- Similarity scores must be between 0 and 1
- Timestamps must be valid datetime objects