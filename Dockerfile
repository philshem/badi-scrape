# Use lightweight Python image with Chromium support
FROM python:3.11-slim

# Set the working directory
WORKDIR /app

# Install only needed dependencies: chromium, wget for downloads, and ca-certificates
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    chromium-browser \
    chromium-driver \
    ca-certificates && \
    rm -rf /var/lib/apt/lists/*

# Copy Python dependencies first (leverages Docker layer caching)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Create data directory
RUN mkdir -p data

# Copy all application files
COPY data/swimmers.csv data/
COPY badi.py heatmap.py entrypoint.sh ./

# Make scripts executable
RUN chmod +x badi.py heatmap.py entrypoint.sh

ENTRYPOINT ["./entrypoint.sh"]
