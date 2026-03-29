# DevOps Scripts Testing Container
# This container provides all dependencies needed to run the DevOps scripts

FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY scripts/ ./scripts/
COPY tests/ ./tests/
COPY .gitignore ./

# Create necessary directories
RUN mkdir -p logs backups

# Set environment variables for common tools
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Default command
CMD ["python3", "--version"]
