# Use a specific Selenium standalone Chrome image
FROM selenium/standalone-chrome:115.0

# Set the working directory
WORKDIR /app

# Install Python
USER root
RUN apt-get update && \
    apt-get install -y python3 python3-pip

# Copy Python dependencies
# COPY requirements.txt .
# RUN pip3 install --no-cache-dir -r requirements.txt

# Copy the Python script into the container
COPY badi.py .

# Set the entry point
CMD ["python3", "badi.py"]
