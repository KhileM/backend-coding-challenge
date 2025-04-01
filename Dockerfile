# Use official lightweight Python image
FROM python:3.12-slim

# Set working directory in container
WORKDIR /app

# Copy everything into the container
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port Flask is running on
EXPOSE 4999

# Set environment variables
ENV FLASK_APP=run.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_RUN_PORT=4999

# Run the app
CMD ["flask", "run"]
