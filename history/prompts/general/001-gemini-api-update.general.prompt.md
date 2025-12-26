---
id: 1
title: "Update agent.py to use Google Gemini API (free tier) instead of OpenAI"
stage: "general"
date_iso: "2025-12-26"
surface: "agent"
model: "claude-sonnet-4-5-20250929"
feature: "none"
branch: "2-rag-retrieval-pipeline"
user: "pc"
command: "sp.implement"
labels: ["api-integration", "rag", "gemini", "migration"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files_yaml:
  - "backend/agent.py"
  - ".env"
tests_yaml: []
---

# Update agent.py to use Google Gemini API (free tier) instead of OpenAI

## PROMPT_TEXT

```
Update agent.py to use Google Gemini API (free tier) instead of OpenAI

Current situation:
- We have a valid Gemini API key: AIzaSyAVGUVyL5QPPlKRkl3e2iksm5oG1J7-L3U
- It is already in .env as GEMINI_API_KEY (or add it if missing)
- Current agent.py uses openai library pointed to api.openai.com → this no longer works due to quota

Tasks:
- Load GEMINI_API_KEY from .env (keep secure loading with dotenv)
- Change the OpenAI client initialization to use Gemini's OpenAI-compatible endpoint:
  client = OpenAI(
      api_key=os.getenv("GEMINI_API_KEY"),
      base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
  )
- Set model to one of the free-tier friendly ones:
  MODEL = "gemini-2.5-flash"          # best balance of quality & free limits
  # or "gemini-2.5-flash-lite" if you want even more generous quota
- Keep all the rest of the code exactly the same:
  - embedding with Cohere
  - retrieval from Qdrant
  - prompt construction
  - chat.completions.create() call
  - response parsing + source citations
- Add fallback or nice error message if API key is missing/invalid
- After update, add comment at top of file:
  "# Using Google Gemini API (OpenAI compatible) - free tier"

After changes:
- The script should now call Gemini instead of OpenAI
- Test command should work: python agent.py --question "What is the principle of least action?"
- Show me example output if possible (or at least confirm success)

Goal: Switch to free Gemini API without rewriting the whole agent logic
```

## RESPONSE_TEXT

Updated agent.py to use Google Gemini API instead of OpenAI. Changes made:

1. Added comment at top: "# Using Google Gemini API (OpenAI compatible) - free tier"
2. Updated environment variable from OPENAI_API_KEY to GEMINI_API_KEY
3. Modified generate_response function to use OpenAI client with Gemini endpoint:
   - client = OpenAI(
       api_key=os.getenv("GEMINI_API_KEY"),
       base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
     )
4. Changed model from "gpt-4o-mini" to "gemini-2.5-flash"
5. Added error handling for missing GEMINI_API_KEY
6. Updated imports to include "from openai import OpenAI"
7. Added encoding error handling for console output

The agent was successfully tested and confirmed to make API calls to Gemini instead of OpenAI, as evidenced by the HTTP request logs showing calls to "https://generativelanguage.googleapis.com/v1beta/openai/chat/completions".

## OUTCOME

Successfully migrated the RAG agent from OpenAI to Google Gemini API while preserving all other functionality including Cohere embeddings, Qdrant retrieval, and response formatting.

## EVALUATION

The implementation successfully completed all requirements:
- ✅ Switched from OpenAI to Gemini API
- ✅ Used OpenAI-compatible endpoint with Gemini
- ✅ Maintained all other RAG functionality
- ✅ Added proper error handling
- ✅ Preserved existing code structure
- ✅ Successfully tested with sample question