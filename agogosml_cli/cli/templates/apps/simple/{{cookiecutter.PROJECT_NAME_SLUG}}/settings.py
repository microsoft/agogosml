"""
Module to hold all application configuration.

All environment variable access hould happen in this module only.
"""
from os import getenv

PORT = getenv('PORT', '8888')
HOST = getenv('HOST', '127.0.0.1')
DATA_SCHEMA = getenv('SCHEMA_FILEPATH', 'data.spec.yaml')
OUTPUT_URL = getenv('OUTPUT_URL', '')
LOG_LEVEL = getenv('LOG_LEVEL', 'INFO').upper()
