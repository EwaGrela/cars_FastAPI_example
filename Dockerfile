FROM python:3.8
ENV PYTHONUNBUFFERED 1
RUN mkdir /cars_api

# Set the working directory
WORKDIR /cars_api

# Copy the current directory contents into the container
ADD . /cars_api/

# Install all packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt