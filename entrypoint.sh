#!/bin/bash

# Define the output file
OUTPUT_FILE="data/out.csv"

# Get the current timestamp
TIMESTAMP=$(date "+%Y-%m-%d %H:%M:%S")

# Run the Python script and append the output with timestamp
python3 badi.py >> "$OUTPUT_FILE"

# Append the timestamp before each new entry
echo "$TIMESTAMP, $(tail -n 1 $OUTPUT_FILE)" >> "$OUTPUT_FILE"
