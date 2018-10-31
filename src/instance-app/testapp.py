
import datahelper
import json
from hypothesis import given
from hypothesis.strategies import fixed_dictionaries, text, characters, integers

#TO DO: Make Unit Tests More Robust

@given(data=fixed_dictionaries({
        'key': text(characters()),
        'intValue': integers()
        }))
def test_validation(data):
    encoded_json = json.dumps(data)
    assert datahelper.validate_schema(encoded_json) is None

@given(data=fixed_dictionaries({
        'key': text(characters()),
        'intValue': integers()
        }))
def test_transform(data):
    encoded_original_json = json.dumps(data)
    transformed_object = datahelper.transform(encoded_original_json)

    data['intValue'] = data['intValue'] + 100
    
    assert transformed_object == data

if __name__ == '__main__':
    test_validation()
    test_transform()