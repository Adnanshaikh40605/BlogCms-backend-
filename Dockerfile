FROM python:3.11-slim

WORKDIR /app

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Copy requirements first for better caching
COPY requirements.txt /app/

# Install dependencies
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Copy project
COPY . /app/

# Create static directory
RUN mkdir -p static

# Set execute permissions on entrypoint
RUN chmod +x entrypoint.sh

# Run the entry point script
CMD ["/bin/bash", "entrypoint.sh"] 