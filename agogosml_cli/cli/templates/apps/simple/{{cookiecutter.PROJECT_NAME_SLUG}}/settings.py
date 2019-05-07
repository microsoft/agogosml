"""
Module to hold all application configuration.

All environment variable access hould happen in this module only.
"""
from environs import Env

env = Env()
env.read_env()

PORT = env.int('PORT', 8888)
HOST = env('HOST', '127.0.0.1')
DATA_SCHEMA = env('SCHEMA_FILEPATH', 'data.spec.yaml')
OUTPUT_URL = env('OUTPUT_URL', '')
LOG_LEVEL = env('LOG_LEVEL', 'INFO').upper()
