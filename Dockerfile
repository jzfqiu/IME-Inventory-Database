#Build an image starting with the Python 3.4 image.
FROM python:3.7-alpine

# Add the current directory into the path /code in the image.
ADD . /code

# Set working directory to code
WORKDIR /code

# Install requirements
RUN pip install -r requirements.txt

# Initialize environment variables
ENV FLASK_APP web
ENV FLASK_ENV development
ENV FLASK_RUN_PORT 8008

EXPOSE 8008

# Set defualt command
CMD flask run --host=0.0.0.0