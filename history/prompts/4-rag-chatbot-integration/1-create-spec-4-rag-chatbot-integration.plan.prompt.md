---
id: 1
title: "create-spec-4-rag-chatbot-integration"
stage: "plan"
date_iso: "2025-12-26"
surface: "agent"
model: "claude-sonnet-4-5-20250929"
feature: "4-rag-chatbot-integration"
branch: "4-rag-chatbot-integration"
user: "pc"
command: "sp.plan"
labels: ["spec", "plan", "rag", "chatbot", "fastapi", "docusaurus"]
links:
  spec: "../spec.md"
  ticket: null
  adr: null
  pr: null
files_yaml:
  - "specs/4-rag-chatbot-integration/spec.md"
  - "specs/4-rag-chatbot-integration/plan.md"
  - "specs/4-rag-chatbot-integration/research.md"
  - "specs/4-rag-chatbot-integration/data-model.md"
  - "specs/4-rag-chatbot-integration/quickstart.md"
  - "specs/4-rag-chatbot-integration/contracts/api-contract.md"
  - "specs/4-rag-chatbot-integration/checklists/requirements.md"
tests_yaml: []
---

# Create Spec 4: RAG Chatbot Integration

## PROMPT_TEXT

```
RAG Chatbot Integration – Spec 4: FastAPI backend + embed chatbot UI into Docusaurus book

Existing status:
- Spec 1–3 complete & working
- Agent uses free Gemini API (gemini-2.5-flash) via OpenAI-compatible client
- .env has GEMINI_API_KEY, COHERE_API_KEY, QDRANT_URL, QDRANT_API_KEY
- backend/agent.py is fully functional (CLI mode)

Success criteria:
- FastAPI backend exposes POST /chat endpoint: accepts { "question": "...", "context": "..." (optional) } → calls agent logic → returns JSON { "answer": "...", "sources": [ { "url": "...", "text": "..." } ] }
- Simple React chat widget (input box, message history, source links) embedded in Docusaurus (floating button or sidebar)
- Works locally (Docusaurus dev + uvicorn backend)
- Works deployed (GitHub Pages frontend calls live backend URL)
- Handles CORS for github.io domain
- Answers cite sources properly

Constraints:
- Backend: FastAPI + uvicorn, single main.py file preferred
- Frontend: React component in Docusaurus (src/components/ChatbotWidget.jsx)
- Use same Gemini model (gemini-2.5-flash)
- Keep UI minimal: no auth, no history persistence yet
- Deployment: backend free tier (suggest Render/Railway)

Timeline: 3–5 days max

Not building:
- Chat history/memory
- Voice input
- Advanced styling

Please:
1. Start with /sp.plan for Spec 4 (structure, files, steps)
2. Then /sp.tasks and /sp.implement as needed
3. Make backend call the existing agent.py logic (import or copy functions)
4. Add env var for BACKEND_URL in Docusaurus (for local vs prod)

Begin now — generate the /sp.plan first!
```

## RESPONSE_TEXT

Created comprehensive specification and planning documents for the RAG Chatbot Integration (Spec 4):

1. Created spec.md: Complete feature specification with user scenarios, requirements, success criteria, and scope definition
2. Created plan.md: Implementation plan with technical context, project structure, and architecture decisions
3. Created research.md: Technical research on FastAPI, React integration, API design, and security considerations
4. Created data-model.md: Complete API and internal data models with validation rules
5. Created quickstart.md: Step-by-step guide for setting up and running the integrated system
6. Created contracts/api-contract.md: Detailed API contract with request/response schemas and error handling
7. Created checklists/requirements.md: Quality checklist for specification validation

The specification covers all requirements from the prompt:
- FastAPI backend with POST /chat endpoint
- React chat widget for Docusaurus integration
- CORS support for GitHub Pages deployment
- Source citation functionality
- Integration with existing agent.py RAG logic
- Environment variable configuration for local vs production

## OUTCOME

Successfully completed the planning phase for Spec 4 RAG Chatbot Integration. All necessary planning artifacts created and ready for the implementation phase.

## EVALUATION

All planning requirements met:
- ✅ Comprehensive specification created
- ✅ Implementation plan defined
- ✅ Technical research documented
- ✅ Data models specified
- ✅ API contract defined
- ✅ Quickstart guide provided
- ✅ Quality validation checklist created