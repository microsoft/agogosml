import json
from jsonschema import validate

in_memory_files = {}


def validate_schema(data: object, schema_filepath: str):
    """ Validates the input json data against our schema
        defined in schema_example.json

        Args: serialized json object that server has retrieved
    """
    if schema_filepath not in in_memory_files.keys():
        print("it's not in memory")
        with open(schema_filepath, 'r') as schema:
            schema_data = schema.read()
        sample_schema = json.loads(schema_data)
        in_memory_files[schema_filepath] = sample_schema

    parsed_json = json.loads(data)
    validate(parsed_json, in_memory_files[schema_filepath])


def transform(data: object):
    """ Applies simple transformation to the data for the
        final output

        Args:
            data: serialized json object that has been validated against schema
    """
    parsed_json = json.loads(data)
    parsed_json['intValue'] = parsed_json['intValue'] + 100
    return parsed_json
