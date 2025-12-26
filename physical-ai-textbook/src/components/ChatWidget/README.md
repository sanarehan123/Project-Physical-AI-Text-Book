# ChatWidget Component

## Overview
The ChatWidget is a React component that provides a chat interface for users to ask questions about the Physical AI & Humanoid Robotics book. It integrates with the RAG (Retrieval-Augmented Generation) backend to provide contextual answers with source citations.

## Features
- Floating chat button that appears on all pages
- Expandable/collapsible chat interface
- Real-time messaging with user and assistant messages
- Loading indicators during API calls
- Error handling and display
- Source citations with clickable links to original content
- Responsive design for mobile and desktop
- Accessibility features (ARIA labels, keyboard navigation)

## API Integration
- Connects to backend API at configurable URL (default: http://localhost:8000)
- Sends questions to `/chat` endpoint
- Receives answers with source citations
- Handles API errors gracefully

## Environment Variables
- `REACT_APP_BACKEND_URL`: URL of the backend API (e.g., http://localhost:8000 or production URL)

## Usage
The component is automatically integrated into the Docusaurus site via the Root.js theme override. No additional setup is required for pages using the Docusaurus layout.

## Styling
- Uses CSS modules for scoped styling
- Responsive design with mobile-first approach
- Accessible color contrast and focus states
- Consistent with Docusaurus theme where possible

## Testing
- Manually test on different screen sizes
- Verify API connectivity and error states
- Test accessibility features
- Validate source link functionality