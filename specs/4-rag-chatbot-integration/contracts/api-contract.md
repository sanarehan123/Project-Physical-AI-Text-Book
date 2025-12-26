# API Contract: RAG Chatbot Integration – Spec 4

## Overview
This document defines the API contract between the Docusaurus frontend and the FastAPI backend for the RAG chatbot integration. This contract ensures consistent communication and enables independent development of frontend and backend components.

## API Base Information
- **Base URL**: Configurable via environment variables (default: http://localhost:8000)
- **Protocol**: HTTPS in production, HTTP in development
- **Content Type**: All requests and responses use `application/json`
- **Authentication**: None required (API keys managed server-side)

## Endpoints

### POST /chat
**Purpose**: Process a user question and return a contextual answer with source citations

#### Request
- **Method**: POST
- **Path**: `/chat`
- **Content-Type**: `application/json`

##### Request Body Schema
```json
{
  "question": {
    "type": "string",
    "minLength": 1,
    "maxLength": 2000,
    "description": "The user's question to be answered",
    "example": "What is the principle of least action?"
  },
  "context": {
    "type": "string",
    "maxLength": 5000,
    "description": "Optional additional context for the question",
    "example": "I'm studying physics concepts",
    "required": false
  }
}
```

##### Example Request
```json
{
  "question": "What is machine learning?",
  "context": "I am a beginner in AI"
}
```

#### Response
##### Success Response (200 OK)
**Content-Type**: `application/json`

```json
{
  "answer": {
    "type": "string",
    "description": "The generated answer to the user's question",
    "example": "Machine learning is a subset of artificial intelligence that enables computers to learn and improve from experience without being explicitly programmed..."
  },
  "sources": {
    "type": "array",
    "items": {
      "type": "object",
      "properties": {
        "url": {
          "type": "string",
          "format": "uri",
          "description": "URL to the source document",
          "example": "https://project-physical-ai-text-book.vercel.app/docs/module-1/chapter-3"
        },
        "text": {
          "type": "string",
          "description": "Relevant text snippet from the source",
          "example": "Machine learning is a method of data analysis that automates analytical model building..."
        }
      },
      "required": ["url", "text"]
    },
    "description": "List of sources used to generate the answer",
    "example": [
      {
        "url": "https://project-physical-ai-text-book.vercel.app/docs/module-1/chapter-3",
        "text": "Machine learning is a method of data analysis that automates analytical model building using algorithms..."
      }
    ]
  }
}
```

##### Example Success Response
```json
{
  "answer": "Machine learning is a subset of artificial intelligence that enables computers to learn and improve from experience without being explicitly programmed. It involves algorithms that can learn from and make predictions on data...",
  "sources": [
    {
      "url": "https://project-physical-ai-text-book.vercel.app/docs/module-1/chapter-3",
      "text": "Machine learning is a method of data analysis that automates analytical model building using algorithms..."
    },
    {
      "url": "https://project-physical-ai-text-book.vercel.app/docs/module-4/chapter-12",
      "text": "In the context of AI, machine learning algorithms build a model based on training data..."
    }
  ]
}
```

##### Error Responses

**400 Bad Request**
- **Condition**: Invalid request format or missing required fields
- **Content-Type**: `application/json`

```json
{
  "detail": "string",
  "error_code": "string"
}
```

**Example**:
```json
{
  "detail": "Question field is required and cannot be empty",
  "error_code": "INVALID_REQUEST"
}
```

**422 Unprocessable Entity**
- **Condition**: Request validation failed
- **Content-Type**: `application/json`

```json
{
  "detail": [
    {
      "loc": ["string"],
      "msg": "string",
      "type": "string"
    }
  ]
}
```

**Example**:
```json
{
  "detail": [
    {
      "loc": ["body", "question"],
      "msg": "ensure this value has at least 1 characters",
      "type": "value_error.any_str.min_length"
    }
  ]
}
```

**500 Internal Server Error**
- **Condition**: Server-side processing error
- **Content-Type**: `application/json`

```json
{
  "detail": "string",
  "error_code": "INTERNAL_ERROR"
}
```

**Example**:
```json
{
  "detail": "Failed to process the request due to an internal error",
  "error_code": "INTERNAL_ERROR"
}
```

### GET /health
**Purpose**: Check the health status of the API server

#### Request
- **Method**: GET
- **Path**: `/health`

#### Response
##### Success Response (200 OK)
```json
{
  "status": "ok",
  "timestamp": "string",
  "version": "string"
}
```

##### Example Response
```json
{
  "status": "ok",
  "timestamp": "2025-12-26T10:30:00Z",
  "version": "1.0.0"
}
```

## Headers

### Request Headers
- **Content-Type**: `application/json` (for POST requests)
- **Accept**: `application/json` (optional, defaults to JSON)

### Response Headers
- **Content-Type**: `application/json`
- **Access-Control-Allow-Origin**: Configured based on environment (for CORS support)

## Error Handling

### Error Response Format
All error responses follow this standard format:
```json
{
  "detail": "string or array",
  "error_code": "string (optional)"
}
```

### Common Error Codes
- `INVALID_REQUEST`: Request format is invalid
- `VALIDATION_ERROR`: Request validation failed
- `EXTERNAL_SERVICE_ERROR`: External service (Gemini, Cohere, Qdrant) unavailable
- `INTERNAL_ERROR`: Internal server error
- `RATE_LIMIT_EXCEEDED`: Rate limit exceeded

## Rate Limiting
- **Default Limit**: 100 requests per hour per IP
- **Burst Limit**: 10 requests per minute
- **Exceeded Response**: 429 Too Many Requests with retry-after header

## Security Considerations
- API keys are never exposed to the frontend
- All external API calls are made server-side
- Input validation prevents injection attacks
- CORS configured for allowed origins only

## Versioning
- This is version 1.0 of the API contract
- Breaking changes will result in version increments
- Backwards-compatible changes will be made within the same major version

## Testing Contract Compliance
Frontend developers can use this contract to:
1. Mock API responses during development
2. Validate response formats
3. Implement proper error handling
4. Ensure request formats match expectations

Backend developers should:
1. Ensure all responses match the defined schema
2. Maintain backward compatibility for non-breaking changes
3. Update the contract when making changes
4. Provide appropriate error responses as defined

## Changelog
- **v1.0.0**: Initial contract definition for RAG chatbot integration