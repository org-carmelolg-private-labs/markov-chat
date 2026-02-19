# Use an official Python runtime as a parent image
FROM python:3.13.12-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY . .

# Make the start script executable
RUN chmod +x run-docker.sh

# Expose the port the app runs on
EXPOSE 8080

# Environment variables (can be overridden at runtime)
# INPUT_FILENAME: Comma-separated list of text files in static/ directory
# MAX_WORDS: Maximum number of words in generated responses
# TEMPERATURE: Controls creativity (0-1, where >=0.5 is more creative)
# Example: docker run -e INPUT_FILENAME="aitw.txt,commedia.txt" -e MAX_WORDS=150 -e TEMPERATURE=0

# Define the entrypoint for the container
ENTRYPOINT ["./run-docker.sh"]