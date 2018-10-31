# -*- coding: utf-8 -*-

"""Tests for `agogosml_cli` package."""

from click.testing import CliRunner

import pytest
import cli.init

def test_init_generate_empty_json():
    # http://click.palletsprojects.com/en/7.x/testing/
    # Tests if init creates a valid json file 
    print("")

def test_init():
    # http://click.palletsprojects.com/en/7.x/testing/
    # You want to test the following commands:
    # * agogosml init -> produces a manifest.json in the current working directory
    # * agogosml init -f -> test if it overwrites an existing manifest.json in the isolated file system 
    # * agogosml init folder -> test if it produces a manifest.json in the right folder.
    # * agogosml init -f folder -> test if it overwrites in a folder
    print("Hello World")