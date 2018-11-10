# -*- coding: utf-8 -*-

"""Generate command module."""

import os
import click
import json
import _jsonnet
import cli.utils as utils


PROJ_FILES = ['.env',
              'Pipfile',
              'ci-sample-app-pipeline.jsonnet',
              'ci-input-app-pipeline.jsonnet',
              'ci-output-app-pipeline.jsonnet',
              'ci-integration-pipeline.jsonnet',
              'input-app-docker-compose.yml',
              'output-app-docker-compose.yml',
              'sample-app-docker-compose.yml']


@click.command()
@click.option('--force', '-f', is_flag=True, default=False, required=False,
              help='Ovewrite existing manifest file')
@click.option('--config', '-c', required=False, default='./manifest.json',
              help='Path to manifest.json file')
@click.argument('folder', type=click.Path(), default='.', required=False)
def generate(force, config, folder) -> int:
    """Generates an agogosml project"""
    # Read Manifest file
    if os.path.isfile(config):
        with open(config) as f:
            manifest = json.load(f)
            utils.validate_manifest(manifest)
            # Retrieve values
            proj_name = manifest['name']
    else:
        click.echo('manifest.json not found. Please run agogosml init first.')
        raise click.Abort()
    # Create folder if not exists
    if not os.path.isdir(folder):
        os.makedirs(folder)
    for proj_file in PROJ_FILES:
        # Check if Files exists
        if (os.path.exists(os.path.join(folder, proj_file))):
            if not force:
                click.echo('Files already exists. Use --force to overwrite')
                raise click.Abort()
        # Must end w/ -pipeline.json
        if proj_file.endswith('-pipeline.jsonnet'):
            # Modify pipeline file from defaults
            write_pipeline_json(proj_file, folder, proj_name)
        else:
            # Copy files as is from default
            utils.copy_module_templates(proj_file, folder)


def write_pipeline_json(pipeline_file: str,
                        outfolder: str, proj_name: str) -> None:
    """Writes out a pipeline json file
    Args:
        pipeline_file (string):  Name of the pipeline file in module
        outfolder (string): Name of the output folder
        proj_name (string): Value to overwrite - name of the agogosml project
    """
    pipeline_json = json.loads(_jsonnet.evaluate_file(
        filename=utils.get_template_full_filepath(pipeline_file),
        ext_vars={'PROJECT_NAME': proj_name}))
    full_out_file = os.path.join(
        outfolder,
        os.path.splitext(pipeline_file)[0] + '.json')
    with open(full_out_file, 'w') as f:
        json.dump(pipeline_json, f, indent=4)
