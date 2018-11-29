# -*- coding: utf-8 -*-
"""Tests for `agogosml_cli` package."""

import os
import json
from click.testing import CliRunner
import cli.generate as generate
import tests.test_utils as test_utils


"""
* agogosml generate
    * should fail if no manifest.json is in working directory
    * should fail if manifest.json is invalid
    * should fail if files we expect to generate already exist.
        Should it give warning and ask to overwrite?
    * should generate .env file, pipeline files, Pipfile,
        tests/e2e/, tests/validation exist
    * should fail if any yml file is not valid yaml.
    * shoudl fail if any json file is not valid json.
"""

EXPECTED_OUTPUT_PROJ_FILES = [
    'ci-app-pipeline.json',
    'ci-agogosml-pipeline.json',
    'cd-pipeline.json',
    'testproject/dockerbuild.sh',
    'testproject/.dockerignore',
    'testproject/logging.yaml',
    'testproject/Pipfile',
    'testproject/README.md'
]


def test_generate():
    """Tests of generate command w/o <folder> specified"""
    runner = CliRunner()
    """
    RUN: agogosml generate
    RESULT: Produces the correct files in the current working directory
    """
    with runner.isolated_filesystem():
        _create_test_manifest_azure()
        result = runner.invoke(generate.generate)
        assert result.exit_code == 0
        _assert_template_files_exist()
    """
    RUN: agogosml generate -f
    RESULT: Overwrite existing files
    """
    with runner.isolated_filesystem():
        _create_test_manifest_azure()
        _create_dummy_template_files()
        prevmd5 = _get_md5_template_files()
        result = runner.invoke(generate.generate, ['--force'])
        assert result.exit_code == 0
        assert set(prevmd5) != set(_get_md5_template_files())
        _assert_template_files_exist()
    """
    RUN: agogosml generate
    RESULT: Fail since files already exist and should NOT overwite
    """
    with runner.isolated_filesystem():
        _create_test_manifest_azure()
        _create_dummy_template_files()
        prevmd5 = _get_md5_template_files()
        result = runner.invoke(generate.generate)
        assert result.exit_code == 1
        assert set(prevmd5) == set(_get_md5_template_files())
        _assert_template_files_exist()


def test_generate_folder():
    """Test of generate command with folder specified"""
    runner = CliRunner()
    """
    RUN: agogosml generate <folder>
    RESULT: Produces the correct files in the specified directory
    """
    with runner.isolated_filesystem():
        _create_test_manifest_azure()
        result = runner.invoke(generate.generate, ['folder'])
        assert result.exit_code == 0
        _assert_template_files_exist('folder')
    """
    RUN: agogosml generate -f <folder>
    RESULT: Overwrite existing files in the specified directory
    """
    with runner.isolated_filesystem():
        _create_test_manifest_azure()
        _create_dummy_template_files(folder='folder')
        prevmd5 = _get_md5_template_files(folder='folder')
        result = runner.invoke(generate.generate, ['--force', 'folder'])
        assert result.exit_code == 0
        assert set(prevmd5) != set(_get_md5_template_files(folder='folder'))
        _assert_template_files_exist('folder')
    """
    RUN: agogosml generate <folder>
    RESULT: Fail since files already exist and should NOT overwite
    """
    with runner.isolated_filesystem():
        _create_test_manifest_azure()
        _create_dummy_template_files(folder='folder')
        prevmd5 = _get_md5_template_files(folder='folder')
        result = runner.invoke(generate.generate, ['folder'])
        assert result.exit_code == 1
        assert set(prevmd5) == set(_get_md5_template_files(folder='folder'))
        _assert_template_files_exist('folder')


def test_generate_invalid_schema():
    """
    RUN: agogosml generate (with invalid manifest file)
    RESULT: Produces the ff in the current working directory:
        - .env
        - Pipfile
        - azure-ci-app-pipeline.json
        - ci-input-app-pipeline.json
        - ci-output-app-pipeline.json
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


def _assert_template_files_exist(folder='.'):
    for proj_file in EXPECTED_OUTPUT_PROJ_FILES:
        assert os.path.exists(os.path.join(folder, proj_file))


def _create_test_manifest_azure(folder='.'):
    manifest_str = """
    {
        "name": "testproject",
        "cloud": {
            "vendor": "azure",
            "subscriptionId": "123-123-123-123",
            "otherProperties": {
                "azureContainerRegistry": "https://acr.acr.io"
            }
        },
        "repository": {
            "type": "GitHub",
            "url": "https://github.com/Microsoft/agogosml.git"
        },
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
    if not os.path.isdir(folder):
        os.makedirs(folder)
    outfile = os.path.join(folder, 'manifest.json')
    with open(outfile, 'w') as f:
        json.dump(manifest, f, indent=4)


def _create_dummy_template_files(files=EXPECTED_OUTPUT_PROJ_FILES, folder='.'):
    if not os.path.isdir(folder):
        os.makedirs(folder)

    os.makedirs(os.path.join(folder, 'testproject'))

    for proj_file in files:
        outfile = os.path.join(folder, proj_file)

        with open(outfile, 'w') as f:
            json.dump("test content", f, indent=4)


def _get_md5_template_files(files=EXPECTED_OUTPUT_PROJ_FILES, folder='.'):
    """Get the md5 hashes of the project files. Used to know if files were
    overwritten"""
    allmd5 = []
    for proj_file in files:
        outfile = os.path.join(folder, proj_file)
        allmd5.append(test_utils.md5(outfile))
    return allmd5
