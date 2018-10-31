# -*- coding: utf-8 -*-

"""Tests for `agogosml_cli` package."""

from click.testing import CliRunner

import cli.cli


def test_command_line_interface():
    """Test the CLI."""
    runner = CliRunner()
    result = runner.invoke(cli.cli.main)
    assert result.exit_code == 0
    assert 'cli.cli.main' in result.output
    help_result = runner.invoke(cli.cli.main, ['--help'])
    assert help_result.exit_code == 0
    assert '--help  Show this message and exit.' in help_result.output
