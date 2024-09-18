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

# Run the scraping and analysis script
COPY swimmers.csv .

COPY badi.py .
RUN chmod +x badi.py

COPY heatmap.py .
RUN chmod +x heatmap.py

CMD ["python3", "badi.py"]
CMD ["python3", "heatmap.py"]