import json
from jsonschema import validate

def validate_schema(data: object):  
    """ Validates the input json data against our schema
        defined in schema_example.json

        Args: serialized json object that server has retrieved
    """  
    with open('schema_example.json', 'r') as f:
        schema_data = f.read()
    sample_schema = json.loads(schema_data)

    parsed_json = json.loads(data)
    validate(parsed_json, sample_schema)

def transform(data: object):
    """ Applies simple transformation to the data for the 
        final output

        Args: 
            data: serialized json object that has been validated against schema
    """
    parsed_json = json.loads(data)
    parsed_json['intValue'] = parsed_json['intValue'] + 100
    return parsed_json