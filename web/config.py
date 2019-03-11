"""
Load configuration from environment variables
"""

import os

class Config:
    SECRET_KEY = os.environ['SECRET_KEY']
    DEBUG = os.environ['FLASK_ENV'] == 'development'
    MONGO_HOST = os.environ['MONGO_HOST']
    MONGO_PORT = os.environ['MONGO_PORT']

