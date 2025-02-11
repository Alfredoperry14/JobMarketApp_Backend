FROM python:3.9-slim

# Install system dependencies: Chromium browser and its driver
RUN apt-get update && apt-get install -y \
    chromium \
    chromium-driver \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy your requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your application code into the container
COPY . .

# Use the appropriate command (adjust path if needed)
CMD ["python", "jobmarket_backend/scraper.py"]