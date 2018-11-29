# -*- coding: utf-8 -*-
"""Generate command module."""

import os
import click
import json
import _jsonnet
import validators
import giturlparse
import cli.utils as utils
from cookiecutter.main import cookiecutter

# Project files to output with src and dst names.
PROJ_FILES = {
    'pipeline/azure-ci-agogosml-pipeline.jsonnet':
        'ci-agogosml-pipeline.json',
    'pipeline/azure-ci-app-pipeline.jsonnet':
        'ci-app-pipeline.json',
    'pipeline/azure-cd-pipeline.jsonnet':
        'cd-pipeline.json'
}


@click.command()
@click.option(
    '--force',
    '-f',
    is_flag=True,
    default=False,
    required=False,
    help='Overwrite existing manifest file')
@click.option(
    '--config',
    '-c',
    required=False,
    default='./manifest.json',
    help='Path to manifest.json file')
@click.argument('folder', type=click.Path(), default='.', required=False)
def generate(force, config, folder) -> int:
    """Generates an agogosml project"""
    template_vars = {}
    with open(
        utils.get_template_full_filepath('cookiecutter.json')
    ) as default_template_file:
        template_vars = json.load(default_template_file)

    # Read Manifest file
    if os.path.isfile(config):
        with open(config) as f:
            manifest = json.load(f)
            utils.validate_manifest(manifest)
            # Retrieve values
            template_vars = {**template_vars, **extractTemplateVarsFromManifest(manifest)}
    else:
        click.echo('manifest.json not found. Please run agogosml init first.')
        raise click.Abort()
    # Create folder if not exists
    if not os.path.isdir(folder):
        os.makedirs(folder)

    # Write cookiecutter template
    write_cookiecutter(utils.get_template_full_filepath(''),
                       folder, template_vars, force)

    del template_vars['_copy_without_render']

    for template_src, template_dst in PROJ_FILES.items():
        template_src_filename = os.path.basename(template_src)
        # Check if files exists in dst
        if (os.path.exists(os.path.join(folder, template_dst))):
            if not force:
                click.echo('Files already exists. Use --force to overwrite')
                raise click.Abort()

        # Must end w/ -pipeline.json
        if 'CLOUD_VENDOR' in template_vars and template_vars['CLOUD_VENDOR'] == 'azure' \
           and template_src_filename.startswith('azure') and template_src_filename.endswith('-pipeline.jsonnet'):
            # Modify pipeline file from defaults
            write_jsonnet(template_src, template_dst, folder, template_vars)


def extractTemplateVarsFromManifest(manifest):
    template_vars = {
        'PROJECT_NAME': manifest['name'],
        'PROJECT_NAME_SLUG': safe_filename(manifest['name']),
        'SUBSCRIPTION_ID': manifest['cloud']['subscriptionId'],
        'CLOUD_VENDOR': manifest['cloud']['vendor']
    }

    if manifest['cloud']['vendor'] == 'azure':
        template_vars = {**template_vars, **extractAzureTemplateVars(manifest)}

    # Add git repository variables
    if 'repository' in manifest:
        # if it is in the manifest then it is validated by the schema to be complete.
        parsed_giturl = giturlparse.parse(manifest['repository']['url'])
        template_vars['REPOSITORY_TYPE'] = manifest['repository']['type']
        template_vars['REPOSITORY_URL'] = manifest['repository']['url']
        template_vars['REPOSITORY_OWNER'] = parsed_giturl.owner
        template_vars['REPOSITORY_REPO'] = parsed_giturl.name
    return template_vars


def extractAzureTemplateVars(manifest):
    template_vars = {}
    azure_props = manifest['cloud']['otherProperties']
    if 'azureContainerRegistry' not in azure_props or \
       not validators.url(azure_props['azureContainerRegistry']):
        click.echo('Azure Container Registry is missing or invalid URL.')
        raise click.Abort()
    else:
        acr = manifest['cloud']['otherProperties']['azureContainerRegistry']
        template_vars['AZURE_CONTAINER_REGISTRY'] = acr
        if not acr.endswith('/'):
            acr += '/'
        template_vars['AZURE_DOCKER_BUILDARGS'] = \
            '--build-arg CONTAINER_REG=%s --build-arg AGOGOSML_TAG=$(Build.TriggeredBy.BuildId)' % acr
    return template_vars


def write_jsonnet(source_path: str, target_path: str, base_path: str, template_vars: object) -> None:
    """Writes out a pipeline json file
    Args:
        src (string):  Name of the pipeline file in module
        target_path (string): Name of the output folder
        template_vars (object): Values to inject into jsonnet as extVars.
    """
    pipeline_json = json.loads(_jsonnet.evaluate_file(
        filename=utils.get_template_full_filepath(source_path),
        ext_vars=template_vars))
    full_path = os.path.join(base_path, target_path)
    with open(full_path, 'w') as f:
        json.dump(pipeline_json, f, indent=4)


def write_cookiecutter(source_path: str, target_path: str, template_vars: object, overwrite=False) -> None:
    """Outputs a cookiecutter template
    Args:
        target_path (string): Name of the output folder
    """
    return cookiecutter(source_path, extra_context=template_vars, no_input=True,
                        output_dir=target_path, overwrite_if_exists=overwrite)


def safe_filename(name: str) -> str:
    keepcharacters = (' ', '.', '_')
    return "".join(c for c in name if c.isalnum() or c in keepcharacters).rstrip()
