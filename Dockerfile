# Multi-stage Dockerfile for AI-Powered HR Platform
FROM python:3.9-slim as backend-builder

WORKDIR /app
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY backend/ .
EXPOSE 5000
CMD ["python", "app.py"]
