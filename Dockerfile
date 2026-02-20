# Utilize a standard Python base image  
FROM python:3.9-slim

WORKDIR /app

# Install necessary dependencies  
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code and required data files  
COPY run.py .
COPY config.yaml .
COPY data.csv .

# Configure the job to execute automatically upon container startup  
CMD ["python", "run.py", "--input", "data.csv", "--config", "config.yaml", "--output", "metrics.json", "--log-file", "run.log"]