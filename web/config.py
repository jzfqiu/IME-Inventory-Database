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
    GOOGLE_MAP_API_KEY = os.environ['GOOGLE_MAP_API_KEY']
    ACCESS_CODE = os.environ['ACCESS_CODE']
