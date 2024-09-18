# Use a specific Selenium standalone Chrome image
FROM selenium/standalone-chrome:115.0

# Set the working directory
WORKDIR /app

# Install Python
USER root
RUN apt-get update && \
    apt-get install -y python3 python3-pip

# Copy Python dependencies
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

# Copy the Python script and entrypoint script into the container
COPY badi.py .
COPY entrypoint.sh .

# Create the data directory
RUN mkdir -p data
COPY data/out.csv data/out.csv

# Make the entrypoint script executable
RUN chmod +x entrypoint.sh

# Set the entry point to the entrypoint script
ENTRYPOINT ["./entrypoint.sh"]
