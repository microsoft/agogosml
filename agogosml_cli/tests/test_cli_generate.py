# -*- coding: utf-8 -*-

"""Tests for `agogosml_cli` package."""

# from click.testing import CliRunner
# import cli.generate as generate


def test_generate_schema():
    print("TEST SCHEMA VALIDATION BY GIVING IT A VALID AND INVALID SCHEMA...")


def test_generate():
    """
    http://click.palletsprojects.com/en/7.x/testing/
    You want to test the ff. commands (lets start w/ one test case for now):
    * agogosml generate
        * should fail if no manifest.json is in working directory
        * should fail if manifest.json is invalid
        * should fail if files we expect to generate already exist.
            Should it give warning and ask to overwrite?
        * should generate .env file, datapipeline.yml, cicd.yml, Pipfile,
            tests/e2e/, tests/validation exist
        * should fail if any yml file is not valid yaml.
    """
