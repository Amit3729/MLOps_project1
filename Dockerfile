# Use official Python image
FROM python:3.10-slim-buster

# Set app directory
WORKDIR /app

# Copy all project files
COPY app.py .
COPY src/ src/
COPY config/ config/
COPY templates/ templates/
COPY static/ static/

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose FastAPI port
EXPOSE 5001

# Run the FastAPI app
CMD ["python3", "app.py"]
