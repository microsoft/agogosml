# -*- coding: utf-8 -*-

"""Init command module."""

import os
import click
import json
import cli.utils as utils


DEFAULT_MANIFEST_FILE = 'default-manifest.json'


@click.command()
@click.option('--force', '-f', is_flag=True, default=False, required=False,
              help='Ovewrite existing manifest file')
@click.option('--project-name', prompt=True, required=False,
              help='Name of your project')
@click.argument('folder', type=click.Path(), default='.', required=False)
def init(force, project_name, folder):
    """Initializes an agogosml project by creating a manifest file"""
    # Check if exists
    outfile = os.path.join(folder, 'manifest.json')
    if os.path.isfile(outfile):
        if force:
            click.echo('Overwriting %s' % outfile)
        else:
            click.echo('Manifest already exists. Use --force to overwrite')
            raise click.Abort()
    # Create folder if not exists
    if not os.path.exists(os.path.dirname(outfile)):
        os.makedirs(os.path.dirname(outfile))
    manifest = build_manifest(project_name)
    with open(outfile, 'w') as f:
        json.dump(manifest, f, indent=4)
    return 0


def build_manifest(project_name):
    """Builds the Manifest python object"""
    manifest_json = utils.get_json_module_templates(DEFAULT_MANIFEST_FILE)
    manifest_json['name'] = project_name
    # default_manifest_json['tests'] = ??? Prompt user?
    utils.validate_manifest(manifest_json)
    return manifest_json
