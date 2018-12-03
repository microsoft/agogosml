# -*- coding: utf-8 -*-

"""Utility functions."""

import os
import json
from jsonschema import validate
from shutil import copy


SCHEMA_FILE = os.path.join(os.path.dirname(__file__), 'manifest.schema.json')
TEMPLATES_FOLDER = os.path.join(os.path.dirname(__file__), 'templates')


def get_template_full_filepath(file: str) -> str:
    """Get full file path for template file.
    Args:
        file (string): Name of the file in module
    """
    return os.path.join(TEMPLATES_FOLDER, file)


def validate_manifest(manifest_json: object) -> None:
    """Validates a manifest file against
    the scheme Throws an error if invalid.
    Args:
        manifest_json (object):
    """
    module_path = os.path.dirname(__file__)
    schema_file = os.path.join(module_path, SCHEMA_FILE)
    with open(schema_file) as f:
        schema_json = json.load(f)
    validate(manifest_json, schema_json)
    return
