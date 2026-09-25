FROM node:20-slim AS frontend-builder

WORKDIR /frontend
COPY fronted/package*.json ./
RUN npm install
COPY fronted ./
RUN npm run build

FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir \
    -r requirements.txt

COPY app ./app
COPY --from=frontend-builder /frontend/dist ./frontend

EXPOSE 8000

CMD [
    "uvicorn",
    "app.main:app",
    "--host",
    "0.0.0.0",
    "--port",
    "8000"
]