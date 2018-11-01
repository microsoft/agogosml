# -*- coding: utf-8 -*-

"""Tests for `agogosml_cli` package."""

from click.testing import CliRunner

import cli.init as init
import os


def test_init_generate_empty_json():
    # http://click.palletsprojects.com/en/7.x/testing/
    # Tests if init creates a valid json file
    print("")


def test_init():
    """Tests of init command"""
    runner = CliRunner()
    with runner.isolated_filesystem():
        """
        RUN: agogosml init
        RESULT: Produces a manifest.json in the current working directory
        """
        result = runner.invoke(init.init, input='my_project_name')
        assert result.exit_code == 0
        assert os.path.exists('./manifest.json')

        """
        RUN: agogosml init -f
        RESULT: Overwrites existing manifest.json
        """
        modified_time = os.path.getmtime('./manifest.json')
        result = runner.invoke(init.init, ['--force'], input='proj_name')
        assert result.exit_code == 0
        assert os.path.exists('./manifest.json')
        assert modified_time != os.path.getmtime('./manifest.json')

        """
        RUN: agogosml init
        RESULT: Fail if manifest.json already exists and should NOT overwite
        """
        modified_time = os.path.getmtime('./manifest.json')
        result = runner.invoke(init.init, input='proj_name')
        assert result.exit_code == 1
        assert os.path.exists('./manifest.json')
        assert modified_time == os.path.getmtime('./manifest.json')


def test_init_folder():
    """Tests of init <folder> command"""
    runner = CliRunner()
    with runner.isolated_filesystem():
        """
        RUN: agogosml init <folder>
        RESULT: Produces a manifest.json in the right folder.
        """
        result = runner.invoke(init.init, ['folder'], input='proj_name')
        assert result.exit_code == 0
        assert os.path.exists('./folder/manifest.json')

        """
        RUN: agogosml init -f <folder>
        RESULT: Ovewrite a manifest.json in the right folder.
        """
        modified_time = os.path.getmtime('./folder/manifest.json')
        result = runner.invoke(init.init, ['--force', 'folder'],
                               input='proj_name')
        assert result.exit_code == 0
        assert os.path.exists('./folder/manifest.json')
        assert modified_time != os.path.getmtime('./folder/manifest.json')

        """
        RUN: agogosml init <folder>
        RESULT: Fail if manifest.json already exists in folder & NOT overwite
        """
        modified_time = os.path.getmtime('./folder/manifest.json')
        result = runner.invoke(init.init, ['folder'], input='proj_name')
        assert result.exit_code == 1
        assert os.path.exists('./folder/manifest.json')
        assert modified_time == os.path.getmtime('./folder/manifest.json')
