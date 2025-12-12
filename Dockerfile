# Use an official Python 3.10 image
FROM python:3.10-slim-buster

# Set the working directory
WORKDIR /app

# Copy all project files into the container
COPY . /app

# Install dependencies
RUN pip install -r requirements.txt

# Expose the FastAPI port
EXPOSE 5001

# Run the FastAPI app
CMD ["python3", "app.py"]
