# Use official Python image
FROM python:3.10-slim-buster

# Good defaults
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Copy and install requirements FIRST (critical for caching + fixes your error)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Now copy the actual app
COPY app.py .
COPY src/ src/
COPY config/ config/
COPY templates/ templates/
COPY static/ static/

# Expose port
EXPOSE 5001

# Run the app
CMD ["python3", "app.py"]