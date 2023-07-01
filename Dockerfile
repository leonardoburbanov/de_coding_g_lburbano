# Use the base Python image
FROM python:3.9

# Set the working directory in the container
WORKDIR /app

# Copy the necessary files to the container
COPY . /app

# Install the required dependencies
RUN pip install -r requirements.txt

# Set the environment variable
ENV ENVIRONMENT=prod

# Run the script
CMD ["python", "etl.py"]