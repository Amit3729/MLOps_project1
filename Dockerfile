# Use a modern, supported Python base image
FROM python:3.10-slim-bullseye

# Set working directory
WORKDIR /app

# Install build tools (gcc, g++), required for some Python packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    g++ \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy only requirements first for better caching
COPY requirements-prod.txt .
COPY requirements-dev.txt .
RUN pip install --no-cache-dir -r requirements-prod.txt


# Copy the rest of the application
COPY . .

# Expose the port your app runs on
EXPOSE 5001

# Run the application
CMD ["python3", "app.py"]
