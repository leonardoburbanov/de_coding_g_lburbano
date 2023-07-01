# Pull base image
FROM python:3.9-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory inside the container
WORKDIR /app

RUN apt-get -y upgrade
# Copy the requirements file and install Python dependencies
COPY requirements2.txt .
RUN pip install --no-cache-dir -r requirements2.txt

# Copy the rest of the project files
COPY . .

# Specify the command to run when the container starts
CMD [ "python", "main.py" ]