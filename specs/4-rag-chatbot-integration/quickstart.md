# Quickstart Guide: RAG Chatbot Integration – Spec 4

## Overview
This guide provides step-by-step instructions to set up and run the RAG chatbot integration with FastAPI backend and Docusaurus frontend widget.

## Prerequisites
- Python 3.11+ installed
- Node.js 18+ installed
- Access to Google Gemini API (free tier)
- Access to Cohere API
- Access to Qdrant vector database
- Git for version control

## Environment Setup

### Backend Environment
1. Navigate to the project root:
   ```bash
   cd /path/to/your/project
   ```

2. Create a `.env` file in the backend directory with the following variables:
   ```env
   GEMINI_API_KEY=your_gemini_api_key_here
   COHERE_API_KEY=your_cohere_api_key_here
   QDRANT_URL=your_qdrant_url_here
   QDRANT_API_KEY=your_qdrant_api_key_here
   QDRANT_COLLECTION_NAME=book_chunks
   ```

### Frontend Environment
1. Navigate to the Docusaurus directory:
   ```bash
   cd physical-ai-textbook
   ```

2. Create a `.env` file with the backend URL:
   ```env
   REACT_APP_BACKEND_URL=http://localhost:8000
   ```

## Installation

### Backend Setup
1. Navigate to the project root and create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install backend dependencies:
   ```bash
   pip install fastapi uvicorn python-dotenv openai cohere qdrant-client pydantic
   ```

3. Verify the installation:
   ```bash
   python -c "import fastapi, openai, cohere, qdrant_client; print('Backend dependencies installed successfully')"
   ```

### Frontend Setup
1. Navigate to the Docusaurus directory:
   ```bash
   cd physical-ai-textbook
   ```

2. Install frontend dependencies:
   ```bash
   npm install
   ```

## Running the Application

### Backend (FastAPI Server)
1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Activate the virtual environment:
   ```bash
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Start the FastAPI server:
   ```bash
   uvicorn chat_api.main:app --reload --host 127.0.0.1 --port 8000
   ```

   **Note**: Use `--host 127.0.0.1` instead of `0.0.0.0` to ensure the server is accessible from the frontend on Windows systems. If you encounter import errors, ensure that the `backend/chat_api/__init__.py` file exists to make chat_api a proper Python package.

4. Verify the server is running by visiting:
   - API Documentation: http://127.0.0.1:8000/docs
   - Health check: http://127.0.0.1:8000/health

### Frontend (Docusaurus)
1. Navigate to the Docusaurus directory:
   ```bash
   cd physical-ai-textbook
   ```

2. Start the Docusaurus development server:
   ```bash
   npm run dev
   ```

3. Visit http://localhost:3000 to see the documentation site with the integrated chat widget

## API Usage

### Chat Endpoint
Send a POST request to `/chat` with the following JSON structure:

```json
{
  "question": "What is the principle of least action?",
  "context": "I'm studying physics concepts"
}
```

The API will return a response like:

```json
{
  "answer": "The principle of least action states that...",
  "sources": [
    {
      "url": "https://example.com/book/chapter-5",
      "text": "The principle of least action is a variational principle..."
    }
  ]
}
```

### Testing the API
You can test the API using curl:

```bash
curl -X POST "http://localhost:8000/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "question": "What is machine learning?",
    "context": "I am a beginner in AI"
  }'
```

## Integration with Docusaurus

The chat widget is automatically integrated into the Docusaurus site. You can:

1. Toggle the chat widget using the floating button
2. Type questions in the input field
3. Receive answers with source citations
4. Click on source links to navigate to relevant documentation

## Development Workflow

### Backend Development
1. Make changes to backend files in `backend/chat_api/`
2. The server will automatically reload due to `--reload` flag
3. Check the API documentation at http://localhost:8000/docs for testing

### Frontend Development
1. Make changes to React components in `physical-ai-textbook/src/components/ChatWidget/`
2. The Docusaurus server will automatically reload
3. Changes will be visible at http://localhost:3000

## Troubleshooting

### Common Issues

1. **CORS Errors**: Ensure your backend URL is properly configured in the frontend environment variables and that the backend allows the frontend origin.

2. **API Key Issues**: Verify all API keys are correctly set in the environment variables and have the necessary permissions.

3. **Qdrant Connection**: Check that QDRANT_URL and QDRANT_API_KEY are correct and the vector database is accessible.

4. **Port Conflicts**: If ports 8000 or 3000 are in use, change them in the startup commands and environment variables.

### Debugging Steps

1. Check backend logs for error messages
2. Verify all environment variables are set correctly
3. Test external APIs independently (Cohere, Gemini, Qdrant)
4. Use the API documentation at `/docs` to test endpoints manually

## Deployment

### Backend Deployment

#### Option 1: Deploy to Render
1. Create an account at [Render](https://render.com)
2. Fork this repository to your GitHub account
3. Create a new Web Service on Render
4. Connect to your forked repository
5. Configure the following settings:
   - Environment: Python
   - Build Command: `pip install -r backend/requirements.txt`
   - Start Command: `cd backend && uvicorn chat_api.main:app --host 0.0.0.0 --port $PORT`
6. Add environment variables:
   - `GEMINI_API_KEY`: Your Google Gemini API key
   - `COHERE_API_KEY`: Your Cohere API key
   - `QDRANT_URL`: Your Qdrant database URL
   - `QDRANT_API_KEY`: Your Qdrant API key
   - `QDRANT_COLLECTION_NAME`: Your Qdrant collection name (optional, defaults to "book_chunks")
7. Deploy and get your backend URL

#### Option 2: Deploy to Railway
1. Install the Railway CLI or use the web dashboard
2. Create a new project and link it to your repository
3. Railway will automatically detect the `railway.toml` configuration
4. Add your environment variables in the Railway dashboard
5. Deploy and get your backend URL

#### Option 3: Deploy with Docker
1. Build the Docker image: `docker build -t rag-chatbot-backend .`
2. Run the container: `docker run -p 8000:8000 rag-chatbot-backend`
3. Ensure all required environment variables are available to the container

### Frontend Deployment

#### Deploy Docusaurus to GitHub Pages
1. Update the `docusaurus.config.js` file with your repository details
2. Set the `REACT_APP_BACKEND_URL` environment variable to your deployed backend URL
3. Run `npm run deploy` to build and deploy to GitHub Pages

#### Deploy Docusaurus to Vercel
1. Create an account at [Vercel](https://vercel.com)
2. Import your repository
3. Set the build command to `npm run build` and output directory to `build`
4. Add the `REACT_APP_BACKEND_URL` environment variable with your backend URL
5. Deploy

#### Deploy Docusaurus to Netlify
1. Create an account at [Netlify](https://netlify.com)
2. Import your repository
3. Set the build command to `npm run build` and publish directory to `build`
4. Add the `REACT_APP_BACKEND_URL` environment variable with your backend URL
5. Deploy

### Important Notes
- Always update the `REACT_APP_BACKEND_URL` environment variable to point to your deployed backend URL
- Test the integration after deploying both frontend and backend
- Monitor your API usage to stay within free tier limits
- Set up proper monitoring and alerting for production deployments