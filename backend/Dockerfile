# Use official Python image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy requirements 
COPY requirements.txt .

# Install dependencies
# Use --no-cache-dir to avoid caching the installed packages
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the backend code
COPY . .

# Set the default command (adjust if your entry point is different)
CMD ["python", "main.py"]
