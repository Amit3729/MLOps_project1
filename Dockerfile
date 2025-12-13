    FROM python:3.10-slim-buster

    ENV PYTHONDONTWRITEBYTECODE=1
    ENV PYTHONUNBUFFERED=1
    
    WORKDIR /app

    # THIS LINE IS THE FIX – copy requirements first
    COPY requirements.txt .

    # Install dependencies
    RUN pip install --no-cache-dir -r requirements.txt

    # Copy the rest of the code
    COPY app.py .
    COPY src/ src/
    COPY config/ config/
    COPY templates/ templates/
    COPY static/ static/

    EXPOSE 5001
    CMD ["python3", "app.py"]