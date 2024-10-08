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

RUN mkdir -p data

# Copy Python scripts and the entrypoint script
COPY data/swimmers.csv .
COPY badi.py .
COPY heatmap.py .
COPY entrypoint.sh .

# Make sure scripts are executable
RUN chmod +x badi.py
RUN chmod +x heatmap.py
RUN chmod +x entrypoint.sh

RUN mkdir -p data

ENTRYPOINT ["./entrypoint.sh"]
