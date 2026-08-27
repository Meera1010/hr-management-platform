# Enterprise Deployment & CI/CD Pipeline Reference

## Overview
This document specifies the Production Deployment architecture, Containerization (Docker), Environment Configuration, Database Migration strategies, and Continuous Integration & Continuous Deployment (CI/CD) pipelines for the **AI HR Platform**.

---

## 1. Production Docker Containerization

### Backend Dockerfile (`backend/Dockerfile`)
```dockerfile
FROM python:3.10-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
EXPOSE 5001

CMD ["gunicorn", "--bind", "0.0.0.0:5001", "--workers", "4", "run:app"]
```

### Frontend Dockerfile (`frontend/Dockerfile`)
```dockerfile
FROM node:18-alpine AS build
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

FROM nginx:alpine
COPY --from=build /app/dist /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

---

## 2. Docker Compose Production Topology (`docker-compose.yml`)

```yaml
version: '3.8'

services:
  backend:
    build: ./backend
    ports:
      - "5001:5001"
    environment:
      - FLASK_ENV=production
      - SECRET_KEY=${SECRET_KEY}
      - JWT_SECRET_KEY=${JWT_SECRET_KEY}
    restart: always

  frontend:
    build: ./frontend
    ports:
      - "80:80"
    depends_on:
      - backend
    restart: always
```

---

## 3. GitHub Actions CI/CD Workflow (`.github/workflows/ci.yml`)

```yaml
name: AI HR Platform CI/CD Pipeline

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  test-backend:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.10'
      - name: Install Dependencies
        run: |
          cd backend
          pip install -r requirements.txt
          pip install pytest pytest-cov
      - name: Run Backend Tests
        run: |
          cd backend
          python -m pytest

  build-frontend:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Set up Node.js
        uses: actions/setup-node@v3
        with:
          node-version: '18'
      - name: Install & Build Frontend
        run: |
          cd frontend
          npm ci
          npm run build
```
