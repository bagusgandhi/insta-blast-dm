# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Install pip packages
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Set the working directory in the container
WORKDIR /app

# Copy the rest of the application code to /app
COPY . .

# Command to run the application
CMD ["python", "scheduler.py"]
