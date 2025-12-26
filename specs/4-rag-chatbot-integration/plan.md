# Implementation Plan: RAG Chatbot Integration – Spec 4

**Branch**: `4-rag-chatbot-integration` | **Date**: 2025-12-26 | **Spec**: [link to spec](../spec.md)

**Note**: This template is filled in by the `/sp.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Integrate a RAG (Retrieval-Augmented Generation) chatbot into the Docusaurus documentation site with a FastAPI backend and React frontend component. The system will accept user questions, retrieve relevant information from the Qdrant vector database, generate contextual responses using the Google Gemini API, and provide source citations. The architecture follows a microservice approach with a dedicated backend service and a React widget embedded in the Docusaurus documentation site.

## Technical Context

**Language/Version**: Python 3.11 for backend, JavaScript/React for frontend
**Primary Dependencies**: FastAPI, uvicorn, openai, cohere, qdrant-client, React, Docusaurus
**Storage**: Qdrant vector database (external)
**Testing**: pytest for backend, Jest for frontend (if applicable)
**Target Platform**: Web application (backend server + Docusaurus documentation site)
**Project Type**: web (dual project: backend API + frontend widget)
**Performance Goals**: Response time under 5 seconds for 95% of queries, support 50 concurrent users
**Constraints**: Free tier usage of Gemini API, CORS support for GitHub Pages domain, under 5s response time
**Scale/Scope**: Support 1000+ daily active users, handle various book-related queries

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

Constitution requirements verified:
- Uses existing agent.py RAG logic for consistency
- Follows security best practices for API key management
- Implements proper error handling and validation
- Maintains separation of concerns between frontend and backend
- Uses environment variables for configuration

## Project Structure

### Documentation (this feature)

```text
specs/4-rag-chatbot-integration/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (/sp.plan command output)
├── data-model.md        # Phase 1 output (/sp.plan command output)
├── quickstart.md        # Phase 1 output (/sp.plan command output)
├── contracts/           # Phase 1 output (/sp.plan command output)
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
backend/
├── chat_api/
│   ├── main.py          # FastAPI application with /chat endpoint
│   ├── models.py        # Request/response models
│   ├── services/        # RAG service implementation
│   │   ├── chat_service.py
│   │   └── rag_agent.py  # Adapted from existing agent.py
│   └── dependencies.py  # API dependencies and config
└── tests/
    └── test_chat_api.py

physical-ai-textbook/src/
├── components/
│   └── ChatWidget/
│       ├── ChatWidget.jsx  # React chat component
│       ├── ChatWidget.module.css  # Component styling
│       └── ChatMessage.jsx     # Individual message component
├── pages/
└── theme/
    └── Root.js            # Docusaurus root component to integrate chat widget

# Environment configuration
.env                           # Backend environment variables
physical-ai-textbook/.env      # Frontend environment variables (BACKEND_URL)
```

**Structure Decision**: Selected dual-project structure (backend/ + frontend in Docusaurus) to maintain separation of concerns while enabling tight integration. Backend provides API service, frontend provides React widget for Docusaurus integration.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| Dual project structure | Clear separation of backend API service and frontend widget | Single project would mix server-side and client-side code |
| CORS configuration | Required for GitHub Pages frontend to call external backend | Would limit deployment options to same domain only |