# -*- coding: utf-8 -*-

"""Generate command module."""

import click


@click.command()
def generate(args=None):
    """Generates an agogosml project"""
    click.echo("Replace this message by putting your code into "
               "agogosml_cli.cli.main")
    click.echo("See click documentation at http://click.pocoo.org/")
    return 0
