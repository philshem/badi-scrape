# Use full Python 3.14 for better runtime performance (optimized wheels, pre-compiled libraries)
FROM python:3.14

# Set the working directory
WORKDIR /app

# Copy Python dependencies first
COPY requirements.txt .

# Install Chromium and upgrade pip/install dependencies in parallel
RUN apt-get update && \
    apt-get install -y chromium chromium-driver && \
    rm -rf /var/lib/apt/lists/* && \
    pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Create data directory
RUN mkdir -p data

# Copy all application files
COPY data/swimmers.csv data/
COPY badi.py heatmap.py entrypoint.sh ./

# Make scripts executable
RUN chmod +x badi.py heatmap.py entrypoint.sh

ENTRYPOINT ["./entrypoint.sh"]
