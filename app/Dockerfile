# Pull base image
FROM python:3.9-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory inside the container
WORKDIR /app

RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*
# Copy the requirements file and install Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the project files
COPY . .

# Run tests
RUN pytest api_test.py

# EXPOSE - informs Docker that the container listens on the specified network ports at runtime
EXPOSE 5000

# ENTRYPOINT - allows you to configure a container that will run as an executable.
ENTRYPOINT [ "python", "app.py" ]