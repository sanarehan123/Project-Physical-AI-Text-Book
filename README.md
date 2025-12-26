# Physical AI & Humanoid Robotics - RAG Chatbot Integration

## Project Overview
This repository contains the implementation of a RAG (Retrieval-Augmented Generation) chatbot integrated into a Docusaurus documentation site. The project allows users to ask questions about the Physical AI & Humanoid Robotics book and receive contextual answers with source citations.

## Features
- **FastAPI Backend**: REST API with /chat endpoint for RAG processing
- **Docusaurus Integration**: Chat widget embedded into documentation site
- **RAG Processing**: Uses vector search to retrieve relevant content before generating responses
- **Source Citations**: All answers include links to original book sections
- **CORS Support**: Configured for GitHub Pages and other deployment platforms
- **Error Handling**: Graceful error handling for API and network issues

## Architecture
- **Backend**: FastAPI server with RAG service
- **Frontend**: React chat widget embedded in Docusaurus
- **Vector Database**: Qdrant for content retrieval
- **AI Models**: Google Gemini (via OpenAI-compatible endpoint) for generation, Cohere for embeddings

## Tech Stack
- **Backend**: Python, FastAPI, uvicorn
- **Frontend**: React, JavaScript, CSS Modules
- **Vector Database**: Qdrant
- **AI Services**: Google Gemini, Cohere
- **Documentation**: Docusaurus
- **Deployment**: Render, Railway, Docker

## Installation & Setup

### Backend Setup
1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Create `.env` file with your API keys:
   ```env
   GEMINI_API_KEY=your_gemini_api_key
   COHERE_API_KEY=your_cohere_api_key
   QDRANT_URL=your_qdrant_url
   QDRANT_API_KEY=your_qdrant_api_key
   QDRANT_COLLECTION_NAME=book_chunks
   ```

5. Start the backend server:
   ```bash
   uvicorn chat_api.main:app --reload --host 0.0.0.0 --port 8000
   ```

### Frontend Setup
1. Navigate to the Docusaurus directory:
   ```bash
   cd physical-ai-textbook
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Create `.env` file for frontend:
   ```env
   REACT_APP_BACKEND_URL=http://localhost:8000
   ```

4. Start the development server:
   ```bash
   npm start
   ```

## API Endpoints
- `GET /` - Root endpoint
- `GET /health` - Health check
- `POST /chat` - Main chat endpoint accepting question and context

## Deployment

### Backend Deployment
The backend can be deployed to:
- Render (using render.yaml)
- Railway (using railway.toml)
- Any Docker-compatible platform

### Frontend Deployment
The Docusaurus site can be deployed to:
- GitHub Pages
- Vercel
- Netlify
- Any static hosting service

## Testing
1. Start both backend and frontend servers
2. Open the Docusaurus site in your browser
3. Click the floating chat button
4. Ask a question about the book
5. Verify that you receive a response with source citations

## Project Structure
```
backend/
├── chat_api/
│   ├── main.py          # FastAPI application
│   ├── models.py        # Request/response models
│   ├── config.py        # Configuration and environment variables
│   └── services/
│       ├── rag_service.py    # RAG processing logic
│       └── chat_service.py   # Chat business logic
├── requirements.txt     # Python dependencies
├── render.yaml          # Render deployment config
├── railway.toml         # Railway deployment config
└── Dockerfile          # Docker configuration

physical-ai-textbook/
├── src/
│   └── components/
│       └── ChatWidget/  # React chat widget components
└── src/theme/Root.js    # Docusaurus theme integration

specs/
└── 4-rag-chatbot-integration/  # Project specifications
```

## Environment Variables
### Backend (.env)
- `GEMINI_API_KEY`: Google Gemini API key
- `COHERE_API_KEY`: Cohere API key
- `QDRANT_URL`: Qdrant database URL
- `QDRANT_API_KEY`: Qdrant database API key
- `QDRANT_COLLECTION_NAME`: Collection name (optional)

### Frontend (.env)
- `REACT_APP_BACKEND_URL`: Backend API URL

## Security Considerations
- API keys are handled server-side only
- CORS is configured for trusted domains
- Input validation is performed on all requests
- Error messages do not expose sensitive information

## Performance
- Responses typically return within 3-5 seconds
- Supports concurrent users
- Configured for efficient vector search

## Troubleshooting
- Check that all environment variables are properly set
- Verify API keys have sufficient permissions
- Ensure Qdrant database is accessible
- Check CORS configuration if frontend cannot connect to backend

## Contributing
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License
This project is licensed under the MIT License - see the LICENSE file for details.