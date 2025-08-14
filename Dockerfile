# Use a slim Python base image
FROM python:3.13-slim

# Environment settings for Python and pip
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Set work directory
WORKDIR /app

# Install system dependencies (minimal)
RUN apt-get update \
    && apt-get install -y --no-install-recommends build-essential curl \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies first (better caching)
COPY requirements.txt /app/requirements.txt
RUN pip install --upgrade pip \
    && pip install -r requirements.txt

# Copy the rest of the application code
COPY . /app

# Make the entrypoint executable
RUN chmod +x /app/run_server.sh \
    # Normalize Windows line endings if present
    && sed -i 's/\r$//' /app/run_server.sh

# Expose the default FastAPI port
EXPOSE 8000

# Set entrypoint to the server start script
ENTRYPOINT ["./run_server.sh"]
