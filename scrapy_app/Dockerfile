FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /scrapy_app

# Install system dependencies required for Scrapy and PostgreSQL
RUN apt-get update && apt-get install -y \
    gcc \
    python3-dev \
    libpq-dev \
    libffi-dev \
    libssl-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy only requirements first to leverage Docker cache
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the project files
COPY . .

# Ensure the Python module is found
ENV PYTHONPATH="/scrapy_app"

# Set the default command to run the spider
CMD ["scrapy", "crawl", "quotes"]
