# -*- coding: utf-8 -*-

"""Generate command module."""

import os
import click
import json
import cli.utils as utils


@click.command()
@click.option('--force', '-f', is_flag=True, default=False, required=False,
              help='Ovewrite existing manifest file')
@click.option('--config', '-c', required=False, default='./manifest.json',
              help='Path to manifest.json file')
@click.argument('folder', type=click.Path(), default='.', required=False)
def generate(force, config, folder):
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
    # Check if Files exists
    if (os.path.exists(os.path.join(folder, '.env')) or
        os.path.exists(os.path.join(folder, 'Pipefile')) or
        os.path.exists(os.path.join(folder, 'azure-customer-app-pipeline.json')) or  # noqa: E501
        os.path.exists(os.path.join(folder, 'azure-input-output-pipeline.json')) or  # noqa: E501
        os.path.exists(os.path.join(folder, 'azure-integration-pipeline.json'))):  # noqa: E501
        if not force:
            click.echo('Files already exists. Use --force to overwrite')
            raise click.Abort()
    # Create folder if not exists
    if not os.path.isdir(folder):
        os.makedirs(folder)
    # Copy files as if from default
    utils.copy_module_artifacts('.env', folder)
    utils.copy_module_artifacts('Pipfile', folder)
    # Modify file from defaults
    write_mod_pipeline('azure-customer-app-pipeline.json', folder, proj_name)
    write_mod_pipeline('azure-input-output-pipeline.json', folder, proj_name)
    write_mod_pipeline('azure-integration-pipeline.json', folder, proj_name)


def write_mod_pipeline(pipeline_file, outfolder, proj_name):
    """Writes out a modified pipeline json file
    Args:
        pipeline_file (string):  Name of the pipeline file in module
        outfolder (string): Name of the output folder
        proj_name (string): Value to overwrite - name of the agogosml project
    """
    pipeline_json = utils.get_json_module_artifacts(pipeline_file)
    mod_pipeline_json = modify_pipeline_json(pipeline_json, proj_name)
    full_out_file = os.path.join(outfolder, pipeline_file)
    with open(full_out_file, 'w') as f:
        json.dump(mod_pipeline_json, f, indent=4)


def modify_pipeline_json(pipeline_json, proj_name):
    """Given a pipeline_json file, overwrite certain values
    Args:
        pipeline_file (json):  JSON object to modify
        proj_name (string): Value to overwrite - name of the agogosml project
    """
    if 'triggers' in pipeline_json:
        for trigger in pipeline_json['triggers']:
            if ('definition' in trigger and
                    trigger['definition'] is not None):
                trigger['definition']['project']['name'] = proj_name
    return pipeline_json
