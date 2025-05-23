# Use the official Python image as the base image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /api

# Copy the application code into the container
COPY /api /api

# Install Python dependencies
RUN pip install -r /api/requirements.txt

# Set environment variables
ENV DB_USER=admin
ENV DB_PASSWORD=parola
ENV DB_HOST=host
ENV DB_PORT=3306
ENV DB_NAME=snack

# Run the application
CMD ["python", "/api/app.py"]