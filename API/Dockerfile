# Use the official Python image
FROM python:3.7

# Set working directory
RUN mkdir /app
WORKDIR /app

# Set environment variables used by Flask
ENV FLASK_APP=server.py
ENV FLASK_RUN_HOST=0.0.0.0

# Install ffmpeg
RUN apt-get update && apt-get install -y ffmpeg

# Copy requeriments.txt and install dependencies
COPY requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt

# Copy the current directory in the project to
# the working directory of the Docker image
COPY . /app

# Run the web service on container startup. Here we use the gunicorn
# webserver, with one worker process and 8 threads
CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 server:app