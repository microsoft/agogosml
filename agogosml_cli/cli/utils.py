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


def copy_module_templates(src: str, dst: str) -> str:
    """Copies a file from the module templates, returns dst string.
    Throws SameFileError if both file and destination are the same.
    Args:
        src (string):  Name of the source template file
        dst (string):  Destination folder to copy to
    """
    module_path = os.path.dirname(__file__)
    full_file = os.path.join(module_path, TEMPLATES_FOLDER, src)
    return copy(full_file, dst)


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
