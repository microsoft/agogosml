""" Unit tests for the customer app """
import os
import json
from dotenv import load_dotenv
from hypothesis import given
from hypothesis.strategies import fixed_dictionaries, text, characters, integers
import datahelper

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
load_dotenv(dotenv_path=os.path.join(BASE_DIR, ".env"))

SCHEMA_FILEPATH = os.getenv('SCHEMA_FILEPATH')

# TO DO: Make Unit Tests More Robust


@given(
    data=fixed_dictionaries({
        'key': text(characters()),
        'intValue': integers()
    }))
def test_validation(data):
    """ Test that the schema validator is working as expected """
    encoded_json = json.dumps(data)
    assert datahelper.validate_schema(encoded_json, SCHEMA_FILEPATH) is None


@given(
    data=fixed_dictionaries({
        'key': text(characters()),
        'intValue': integers()
    }))
def test_transform(data):
    """ Test the simple transformation on the input data """
    encoded_original_json = json.dumps(data)
    transformed_object = datahelper.transform(encoded_original_json)

    data['intValue'] = data['intValue'] + 100

    assert transformed_object == data
