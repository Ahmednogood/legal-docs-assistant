# Use the official Python base image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Set env for Chainlit to avoid permission error
ENV CHAINLIT_FILES_DIR=.chainlit_files

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    tesseract-ocr \
    poppler-utils \
    && rm -rf /var/lib/apt/lists/*

# Copy only requirement files first
COPY requirements.txt .

# Install Python dependencies
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy rest of the app code
COPY . .

# Create the writable folder for file uploads
RUN mkdir -p .chainlit_files

# Expose default port
EXPOSE 7860

# Run Chainlit app
CMD ["chainlit", "run", "main.py", "-h", "0.0.0.0", "-p", "7860"]
