# -*- coding: utf-8 -*-

"""Generate command module."""

import click


@click.command()
@click.option('--config', '-c', required=False,
              help='Path to manifest.json file')
@click.argument('folder', type=click.Path(), default='.', required=False)
def generate(config, folder):
    """Generates an agogosml project"""
    click.echo("NOT IMPLMENTED")
    return 0
