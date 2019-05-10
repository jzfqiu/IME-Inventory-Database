"""
Load configuration from environment variables
"""

import os


class Config:
    SECRET_KEY = os.environ['SECRET_KEY']
    DEBUG = os.environ['FLASK_ENV'] == 'development'

    MONGO_HOST = os.environ['MONGO_HOST']
    MONGO_PORT = os.environ['MONGO_PORT']
    MONGO_INITDB_ROOT_USERNAME = os.environ['MONGO_INITDB_ROOT_USERNAME']
    MONGO_INITDB_ROOT_PASSWORD = os.environ['MONGO_INITDB_ROOT_PASSWORD']

    AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID', None)
    AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY', None)
    AWS_BUCKET_NAME = os.getenv('AWS_BUCKET_NAME', None)
    USE_AWS_SERVICE = AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY and AWS_BUCKET_NAME
