# Deployment Guide for RAG Chatbot API Backend

## Overview
This guide provides instructions for deploying the RAG Chatbot API backend to various platforms. The backend is built with FastAPI and serves as the API layer for the RAG functionality.

## Prerequisites
Before deploying, ensure you have the following:
- Google Gemini API key (free tier)
- Cohere API key
- Qdrant vector database URL and API key
- Access to a deployment platform (Render, Railway, or Docker-compatible)

## Deployment Options

### 1. Deploy to Render

#### Using the Render Button (Recommended)
[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy)

#### Manual Deployment
1. Create an account at [Render](https://render.com)
2. Fork this repository to your GitHub account
3. Create a new **Web Service** on Render
4. Connect to your forked repository
5. Configure the following settings:
   - **Environment**: Python
   - **Build Root**: `backend` (set this as the working directory)
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn chat_api.main:app --host 0.0.0.0 --port $PORT`
6. Add environment variables:
   - `GEMINI_API_KEY`: Your Google Gemini API key
   - `COHERE_API_KEY`: Your Cohere API key
   - `QDRANT_URL`: Your Qdrant database URL
   - `QDRANT_API_KEY`: Your Qdrant API key
   - `QDRANT_COLLECTION_NAME`: Your Qdrant collection name (optional, defaults to "book_chunks")
7. Deploy and note the assigned URL

### 2. Deploy to Railway

#### Using Railway Dashboard
1. Create an account at [Railway](https://railway.app)
2. Create a new project and link it to your repository
3. Railway will automatically detect the `railway.toml` configuration
4. Add your environment variables in the Railway dashboard:
   - `GEMINI_API_KEY`
   - `COHERE_API_KEY`
   - `QDRANT_URL`
   - `QDRANT_API_KEY`
   - `QDRANT_COLLECTION_NAME` (optional)
5. Deploy and note the assigned URL

### 3. Deploy with Docker

#### Building and Running Locally
```bash
# Clone the repository
git clone <your-repo-url>
cd <repo-name>

# Build the Docker image
docker build -t rag-chatbot-backend .

# Run the container with environment variables
docker run -p 8000:8000 \
  -e GEMINI_API_KEY=your_gemini_key \
  -e COHERE_API_KEY=your_cohere_key \
  -e QDRANT_URL=your_qdrant_url \
  -e QDRANT_API_KEY=your_qdrant_key \
  rag-chatbot-backend
```

#### Pushing to Container Registry
```bash
# Tag the image
docker tag rag-chatbot-backend <your-registry>/rag-chatbot-backend:latest

# Push to your registry
docker push <your-registry>/rag-chatbot-backend:latest

# Run from registry
docker run -p 8000:8000 \
  -e GEMINI_API_KEY=your_gemini_key \
  -e COHERE_API_KEY=your_cohere_key \
  -e QDRANT_URL=your_qdrant_url \
  -e QDRANT_API_KEY=your_qdrant_key \
  <your-registry>/rag-chatbot-backend:latest
```

## Environment Variables

### Required Variables
- `GEMINI_API_KEY`: Google Gemini API key for response generation
- `COHERE_API_KEY`: Cohere API key for embeddings
- `QDRANT_URL`: URL for your Qdrant vector database
- `QDRANT_API_KEY`: API key for your Qdrant database

### Optional Variables
- `QDRANT_COLLECTION_NAME`: Name of the collection in Qdrant (default: "book_chunks")

## CORS Configuration
The backend is pre-configured with CORS settings to allow requests from:
- `http://localhost:3000` (local Docusaurus development)
- `https://*.github.io` (GitHub Pages)
- `https://*.vercel.app` (Vercel deployments)
- `https://*.netlify.app` (Netlify deployments)
- `https://*.pages.dev` (Cloudflare Pages)

## Health Check
After deployment, verify the service is running by accessing the health check endpoint:
```
GET /health
```

## API Documentation
After deployment, API documentation is available at:
```
GET /docs
```

## Troubleshooting

### Common Issues
1. **Environment Variables Not Set**: Ensure all required environment variables are correctly configured in your deployment platform.

2. **API Keys Expired**: Verify that your API keys are valid and have not exceeded usage limits.

3. **Qdrant Connection Issues**: Check that your Qdrant URL and API key are correct and the database is accessible.

4. **CORS Errors**: If the frontend cannot connect to the backend, verify the frontend origin is included in the CORS configuration.

### Logging
Check your deployment platform's logs for error messages. Common errors include:
- Missing environment variables
- Invalid API keys
- Network connectivity issues
- Resource limitations

## Scaling Considerations
- The free tier should handle low to moderate traffic
- For higher traffic, consider upgrading to paid plans on your deployment platform
- Monitor API usage to stay within free tier limits
- Consider implementing caching for frequently asked questions

## Security Best Practices
- Never expose API keys in client-side code
- Use HTTPS for all API communications
- Regularly rotate API keys
- Monitor API usage for unusual patterns
- Implement rate limiting for production deployments