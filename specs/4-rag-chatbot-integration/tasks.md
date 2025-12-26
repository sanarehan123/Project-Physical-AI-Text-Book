# Task List: RAG Chatbot Integration – Spec 4

**Feature**: RAG Chatbot Integration – FastAPI backend + embed chatbot UI into Docusaurus book site
**Branch**: 4-rag-chatbot-integration
**Date**: 2025-12-26
**Input**: Feature specification from `specs/4-rag-chatbot-integration/spec.md`

## Task Dependencies

- **Phase 1**: Setup tasks (no dependencies)
- **Phase 2**: Foundational tasks (depends on Phase 1)
- **Phase 3**: Backend API (depends on Phase 2)
- **Phase 4**: Frontend Widget (depends on Phase 3)
- **Phase 5**: Integration & Testing (depends on Phases 3-4)

## Parallel Execution Opportunities

- T007 [P], T008 [P], T009 [P]: Backend service components can be developed in parallel
- T014 [P], T015 [P], T016 [P]: Frontend components can be developed in parallel

## Implementation Strategy

MVP scope includes: Basic FastAPI backend with /chat endpoint, minimal React chat widget, and core functionality. Additional features will be added incrementally.

---

## Phase 1: Setup

### Goal
Initialize project structure and install required dependencies for both backend and frontend components.

- [ ] T001 Create backend directory structure: `backend/chat_api/`
- [ ] T002 Install backend dependencies: fastapi, uvicorn, pydantic, python-dotenv, openai, cohere, qdrant-client
- [ ] T003 Create frontend component directory: `physical-ai-textbook/src/components/ChatWidget/`

---

## Phase 2: Foundational Components

### Goal
Set up foundational components that will be used across all user stories, including configuration, models, and base services.

- [ ] T004 Create API request/response models in `backend/chat_api/models.py` using Pydantic
- [ ] T005 Set up environment variable loading and validation in `backend/chat_api/config.py`
- [ ] T006 Create base FastAPI app structure in `backend/chat_api/main.py`

---

## Phase 3: Backend API Implementation

### Goal
Implement the core backend functionality with the /chat endpoint that integrates with the existing RAG agent logic.

- [ ] T007 [P] [US1] Create RAG service module in `backend/chat_api/services/rag_service.py` that reuses agent.py functions
- [ ] T008 [P] [US1] Create chat service module in `backend/chat_api/services/chat_service.py`
- [ ] T009 [P] [US1] Create API dependencies module in `backend/chat_api/dependencies.py`
- [ ] T010 [US1] Implement /chat endpoint in `backend/chat_api/main.py` that accepts question and optional context
- [ ] T011 [US1] Add CORS middleware to FastAPI app to allow GitHub Pages domain
- [ ] T012 [US1] Implement error handling for missing question (400) and LLM failures (500)
- [ ] T013 [US1] Add health check endpoint at /health for monitoring

---

## Phase 4: Frontend Widget Implementation

### Goal
Create the React chat widget that will be embedded in the Docusaurus documentation site.

- [ ] T014 [P] [US2] Create ChatWidget React component in `physical-ai-textbook/src/components/ChatWidget/ChatWidget.jsx`
- [ ] T015 [P] [US2] Create ChatMessage component in `physical-ai-textbook/src/components/ChatWidget/ChatMessage.jsx`
- [ ] T016 [P] [US2] Create CSS module for chat widget styling in `physical-ai-textbook/src/components/ChatWidget/ChatWidget.module.css`
- [ ] T017 [US2] Implement API communication logic in ChatWidget to call backend /chat endpoint
- [ ] T018 [US2] Add loading states and error handling to ChatWidget
- [ ] T019 [US2] Implement source citation rendering with clickable links to book URLs

---

## Phase 5: Integration & Testing

### Goal
Integrate the chat widget into the Docusaurus site and perform comprehensive testing.

- [ ] T020 [US3] Integrate ChatWidget into Docusaurus theme in `physical-ai-textbook/src/theme/Root.js`
- [ ] T021 [US3] Add environment variable for backend URL in `physical-ai-textbook/.env`
- [ ] T022 [US3] Test local integration with backend running on localhost:8000
- [ ] T023 [US3] Verify source citations render correctly with clickable links
- [ ] T024 [US3] Test error handling scenarios (API errors, network issues)
- [ ] T025 [US3] Validate CORS configuration works with GitHub Pages domain

---

## Phase 6: Polish & Cross-Cutting Concerns

### Goal
Finalize the implementation with deployment preparation and documentation.

- [ ] T026 Add deployment configuration files for Render/Railway in backend directory
- [ ] T027 Update quickstart guide with deployment instructions
- [ ] T028 Add README.md to ChatWidget component directory explaining usage
- [ ] T029 Test complete end-to-end flow: question → backend → RAG processing → response → frontend display
- [ ] T030 Document environment variables needed for deployment