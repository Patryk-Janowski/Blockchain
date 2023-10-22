# Use an official Python runtime as the base image
FROM python:3.9-slim

# Set the working directory in the container to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt

# Make ports 50000 and 50001 available to the world outside this container
EXPOSE 50000
EXPOSE 50001

# Define environment variable for better debugging
ENV PYTHONUNBUFFERED=1

# RUN apt-get update && \
#     apt-get install -y net-tools inetutils-ping && \
#     apt-get clean && \
#     rm -rf /var/lib/apt/lists/*

# Set the entry point to bash
ENTRYPOINT ["/bin/bash"]
