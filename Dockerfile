#Build an image starting with the Python 3.4 image.
FROM python:3.7-alpine

# Add the current directory into the path /code in the image.
ADD . /code

# Set working directory to code
WORKDIR /code

# Install requirements
RUN pip install -r requirements.txt

# Use port 8008 to communicate with outside world
EXPOSE 8008

# Set defualt command
CMD flask run --host=0.0.0.0