# Hackathon Submission: Physical AI & Humanoid Robotics Textbook with RAG Chatbot

## Project Description (150-200 words)

This project presents a comprehensive Physical AI & Humanoid Robotics textbook built with Docusaurus, featuring an integrated AI-powered chatbot that enhances learning through contextual assistance. The textbook covers foundational concepts to advanced implementations in embodied intelligence.

The standout feature is the RAG (Retrieval-Augmented Generation) chatbot with a unique selected-text question capability. Users can highlight any text on a page and click "Ask AI" to get explanations focused only on that specific content. This provides precise, contextual learning support.

The backend uses FastAPI with Qdrant vector database and OpenAI's embedding models to store and retrieve textbook content. The frontend integrates seamlessly with Docusaurus using React components. Deployment is handled through Vercel for the frontend and a cloud service for the backend API.

This innovative approach transforms static educational content into an interactive learning experience, demonstrating the practical application of AI in education.

## Live Links

- **Book URL**: https://project-physical-ai-text-book.vercel.app/
- **GitHub Frontend**: https://github.com/sanarehan123/Project-Physical-AI-Text-Book
- **Backend Code**: Included in rag-backend directory of the same repository
- **Backend URL**: [Your deployed backend URL]

## Tech Stack

- **Frontend**: Docusaurus, React, JavaScript/TypeScript
- **Backend**: FastAPI, Python
- **Vector Database**: Qdrant Cloud
- **Embeddings**: OpenAI text-embedding-3-small
- **Language Model**: OpenAI GPT-4o-mini
- **Database**: Neon Postgres with pgvector
- **Deployment**: Vercel (frontend), Cloud provider (backend)
- **Additional**: React Markdown, LangChain

## Demo Video Suggestions

Create a 1-2 minute screen recording showing:
1. Navigating the textbook
2. Asking a general question via the chat widget
3. Highlighting text and using the "Ask AI" feature
4. Demonstrating accurate, context-aware responses