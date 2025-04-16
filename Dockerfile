# Use the official Python 3.11 slim image as the base
FROM python:3.11-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file to install dependencies
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project into the container
COPY . .

# Verify directory structure for debugging
RUN ls -R

# Add src/ to PYTHONPATH to ensure module resolution
ENV PYTHONPATH=/app:/app/src

# Expose the port the app will run on
EXPOSE 5000

# Set environment variables
ENV FLASK_APP=src/app.py
ENV FLASK_ENV=production
ENV PORT=5000

# Command to run the app with Gunicorn, with increased timeout and logging
CMD ["gunicorn", "--timeout", "120", "--log-level", "debug", "-w", "4", "-b", "0.0.0.0:5000", "src.app:app"]
