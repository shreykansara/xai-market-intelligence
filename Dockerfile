# Lightweight Python Container for Omniscope AI
FROM python:3.11-slim

WORKDIR /app

# Install minimal curl for container healthcheck
RUN apt-get update && apt-get install -y --no-install-recommends curl && rm -rf /var/lib/apt/lists/*

# Install lightweight dependencies (no PyTorch, no heavy ML packages)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY . .

ENV PORT=5000
EXPOSE 5000

# Run with Gunicorn WSGI server
CMD ["sh", "-c", "gunicorn server:app --bind 0.0.0.0:${PORT:-5000} --workers 2 --timeout 120"]
