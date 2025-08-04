# Use official Python image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy your app code
COPY . .

# Expose port (change if your app uses a different port)
EXPOSE 10000

# Start FastAPI app (adjust if your entrypoint is different)
CMD ["python3", "backend/backendApp.py"]
