# -*- coding: utf-8 -*-

"""Utility functions."""

import os
import json
from jsonschema import validate
from shutil import copy


SCHEMA_FILE = 'manifest.schema.json'
ARTIFACTS_FOLDER = 'artifacts'


def get_json_module_artifacts(file):
    """Retrieve JSON from file in module artifacts
    Args:
        file (string):  Name of the file in module
    """
    module_path = os.path.dirname(__file__)
    full_file = os.path.join(module_path, ARTIFACTS_FOLDER, file)
    with open(full_file) as f:
        file_json = json.load(f)
    return file_json


def copy_module_artifacts(file, out):
    """Copies a file from the module artifacts
    Args:
        file (string):  Name of the file in module
        file (string):  Full filepath of output file
    """
    module_path = os.path.dirname(__file__)
    full_file = os.path.join(module_path, ARTIFACTS_FOLDER, file)
    copy(full_file, out)


def validate_manifest(manifest_json):
    """Validates a given JSON string against schema file.
    Throws an error if invalid."""
    schema_json = get_json_module_artifacts(SCHEMA_FILE)
    validate(manifest_json, schema_json)
    return
