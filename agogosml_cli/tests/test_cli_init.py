# -*- coding: utf-8 -*-

"""Tests for `agogosml_cli` package."""

import os
import json
from click.testing import CliRunner
import cli.init as init
import tests.test_utils as test_utils


def test_init_generate_valid_json():
    """Test of init command: generated manifest contains valid json"""
    runner = CliRunner()
    with runner.isolated_filesystem():
        result = runner.invoke(init.init, input='proj_name')
        assert result.exit_code == 0
        assert os.path.exists('./manifest.json')
        with open('./manifest.json') as f:
            json.load(f)  # This will fail if not valid JSON


def test_init():
    """Tests of init command w/o <folder> specified"""
    runner = CliRunner()
    """
    RUN: agogosml init
    RESULT: Produces a manifest.json in the current working directory
    """
    with runner.isolated_filesystem():
        result = runner.invoke(init.init, input='proj_name')
        assert result.exit_code == 0
        assert os.path.exists('./manifest.json')
    """
    RUN: agogosml init -f
    RESULT: Overwrites existing manifest.json
    """
    with runner.isolated_filesystem():
        _create_test_manifest()
        prevmd5 = test_utils.md5('./manifest.json')
        result = runner.invoke(init.init, ['--force'], input='proj_name')
        assert result.exit_code == 0
        assert os.path.exists('./manifest.json')
        assert prevmd5 != test_utils.md5('./manifest.json')
    """
    RUN: agogosml init
    RESULT: Fail if manifest.json already exists and should NOT overwite
    """
    with runner.isolated_filesystem():
        _create_test_manifest()
        prevmd5 = test_utils.md5('./manifest.json')
        result = runner.invoke(init.init, input='proj_name')
        assert result.exit_code == 1
        assert os.path.exists('./manifest.json')
        assert prevmd5 == test_utils.md5('./manifest.json')


def test_init_folder():
    """Tests of init command with <folder> specified"""
    runner = CliRunner()
    """
    RUN: agogosml init <folder>
    RESULT: Produces a manifest.json in the right folder.
    """
    with runner.isolated_filesystem():
        result = runner.invoke(init.init, ['folder'], input='proj_name')
        assert result.exit_code == 0
        assert os.path.exists('./folder/manifest.json')
    """
    RUN: agogosml init -f <folder>
    RESULT: Ovewrite a manifest.json in the right folder.
    """
    with runner.isolated_filesystem():
        _create_test_manifest('folder')
        prevmd5 = test_utils.md5('./folder/manifest.json')
        result = runner.invoke(init.init, ['--force', 'folder'],
                               input='proj_name')
        assert result.exit_code == 0
        assert os.path.exists('./folder/manifest.json')
        assert prevmd5 != test_utils.md5('./folder/manifest.json')
    """
    RUN: agogosml init <folder>
    RESULT: Fail if manifest.json already exists in folder & NOT overwite
    """
    with runner.isolated_filesystem():
        _create_test_manifest('folder')
        prevmd5 = test_utils.md5('./folder/manifest.json')
        result = runner.invoke(init.init, ['folder'], input='proj_name')
        assert result.exit_code == 1
        assert os.path.exists('./folder/manifest.json')
        assert prevmd5 == test_utils.md5('./folder/manifest.json')


def _create_test_manifest(folder='.'):
    """Utility method to write out a test manifest file
    in a specified folder"""
    manifest_str = """
    {
        "name": "test manifest",
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
