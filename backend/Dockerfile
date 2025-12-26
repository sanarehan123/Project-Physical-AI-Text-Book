# T026: Add deployment configuration files for Render/Railway in backend directory
FROM python:3.11-slim

WORKDIR /app

COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY backend/ .

EXPOSE 8000

CMD ["uvicorn", "chat_api.main:app", "--host", "0.0.0.0", "--port", "8000"]