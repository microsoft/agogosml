""" Helper functions for the customer application """
import json
from jsonschema import validate

IN_MEMORY_FILES = {}


def validate_schema(data, schema_filepath: str):
    """ Validates the input json data against our schema
        defined in schema_example.json

        Args: serialized json object that server has retrieved
    """
    if schema_filepath is None:
        schema_filepath = 'schema_example.json'
    if schema_filepath not in IN_MEMORY_FILES.keys():
        with open(schema_filepath, 'r') as schema:
            schema_data = schema.read()
        sample_schema = json.loads(schema_data)
        IN_MEMORY_FILES[schema_filepath] = sample_schema

    parsed_json = json.loads(data)
    validate(parsed_json, IN_MEMORY_FILES[schema_filepath])


def transform(data: object):
    """ Applies simple transformation to the data for the
        final output

        Args:
            data: serialized json object that has been validated against schema
    """
    parsed_json = json.loads(data)
    parsed_json['intValue'] = parsed_json['intValue'] + 100
    return parsed_json
