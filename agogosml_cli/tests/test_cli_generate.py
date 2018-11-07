# -*- coding: utf-8 -*-

"""Tests for `agogosml_cli` package."""

import os
import json
from click.testing import CliRunner
import cli.generate as generate


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


def test_generate():
    """
    RUN: agogosml generate
    RESULT: Produces the ff in the current working directory:
        - .env
        - datapipeline.yml
        - cicd.yml
        - Pipfile
        - test/e2e
        - tests/validation
    """
    runner = CliRunner()
    with runner.isolated_filesystem():
        manifest_str = """
        {
            "name": "my-data-pipeline",
            "tests": [{
                "name": "Sanity Check",
                "type": "language-specific",
                "input": "in.json",
                "output": "out.json",
                "outputFormatter": "ConsoleOutputFormatterClass"
            }]
        }
        """
        manifest = json.loads(manifest_str)
        with open('manifest.json', 'w') as f:
            json.dump(manifest, f, indent=4)

        result = runner.invoke(generate.generate)
        assert result.exit_code == 0
        assert os.path.exists('./.env')
        assert os.path.exists('./Pipfile')
        assert os.path.exists('./azure-customer-app-pipeline.json')
        assert os.path.exists('./azure-input-output-pipeline.json')
        assert os.path.exists('./azure-integration-pipeline.json')


def test_generate_invalid_schema():
    """
    RUN: agogosml generate (with invalid manifest file)
    RESULT: Produces the ff in the current working directory:
        - .env
        - datapipeline.yml
        - cicd.yml
        - Pipfile
        - test/e2e
        - tests/validation
    """
    runner = CliRunner()
    with runner.isolated_filesystem():
        manifest_str = """
        {
            "dummy": "abc"
        }
        """
        manifest = json.loads(manifest_str)
        with open('manifest.json', 'w') as f:
            json.dump(manifest, f, indent=4)

        result = runner.invoke(generate.generate)
        assert result.exit_code == 1
