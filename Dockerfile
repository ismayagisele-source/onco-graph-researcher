# Base image: Python 3.14
FROM python:3.14-slim

# Set working directory
WORKDIR /app

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PIP_NO_CACHE_DIR=1

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    zstd \
    && rm -rf /var/lib/apt/lists/*

# Install Ollama
RUN curl -fsSL https://ollama.com/install.sh | sh

# Copy requirements first (for better caching)
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Create directory for Ollama models
RUN mkdir -p /root/.ollama

# Expose ports
# 8501 for Streamlit
# 11434 for Ollama
EXPOSE 8501 11434

# Health check
HEALTHCHECK --interval=30s --timeout=3s \
    CMD curl -f http://localhost:8501/_stcore/health || exit 1

# Run Ollama server and Streamlit
CMD ["sh", "-c", "ollama serve & sleep 5 && ollama pull llama3 && streamlit run app.py --server.address=0.0.0.0 --server.port=8501"]