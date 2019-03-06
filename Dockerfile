#Build an image starting with the Python 3.4 image.
FROM python:3.7-alpine

# Add the current directory into the path /code in the image.
ADD . /code

# Set working directory to code
WORKDIR /code

# Install requirements
RUN pip install -r requirements.txt

# Set default command to 'python3 web/app.py'
CMD ["python3", "web/app.py"]
