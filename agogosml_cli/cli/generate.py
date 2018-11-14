# -*- coding: utf-8 -*-

"""Generate command module."""

import os
import click
import json
import _jsonnet
import validators
import giturlparse
import cli.utils as utils


# Project files to output with src and dst names.
PROJ_FILES = {
    '.env': '.env',
    'Pipfile': 'Pipfile',
    'logging.yaml': 'logging.yaml',
    'pipeline/azure-ci-sample-app-pipeline.jsonnet':
        'ci-sample-app-pipeline.json',
    'pipeline/azure-ci-input-app-pipeline.jsonnet':
        'ci-input-app-pipeline.json',
    'pipeline/azure-ci-output-app-pipeline.jsonnet':
        'ci-output-app-pipeline.json'
}


@click.command()
@click.option('--force', '-f', is_flag=True, default=False, required=False,
              help='Ovewrite existing manifest file')
@click.option('--config', '-c', required=False, default='./manifest.json',
              help='Path to manifest.json file')
@click.argument('folder', type=click.Path(), default='.', required=False)
def generate(force, config, folder) -> int:
    """Generates an agogosml project"""
    injected_variables = {
        "REPOSITORY_TYPE": "GitHub",
        "REPOSITORY_URL": "https://github.com/Microsoft/agogosml.git",
        "REPOSITORY_OWNER": "Microsoft",
        "REPOSITORY_REPO": "agogosml"
    }
    cloud_vendor = None

    # Read Manifest file
    if os.path.isfile(config):
        with open(config) as f:
            manifest = json.load(f)
            utils.validate_manifest(manifest)
            # Retrieve values
            injected_variables['PROJECT_NAME'] = manifest['name']
            injected_variables['SUBSCRIPTION_ID'] = manifest['cloud']['subscriptionId']
            # Add cloud vender specific variables
            cloud_vendor = manifest['cloud']['vendor']
            if cloud_vendor == 'azure':
                azure_props = manifest['cloud']['otherProperties']
                if 'azureContainerRegistry' not in azure_props or \
                   not validators.url(azure_props['azureContainerRegistry']):
                    click.echo('Azure Container Registry is missing or invalid URL.')
                    raise click.Abort()
                else:
                    acr = manifest['cloud']['otherProperties']['azureContainerRegistry']
                    injected_variables['AZURE_CONTAINER_REGISTRY'] = acr
                    if not acr.endswith('/'):
                        acr += '/'
                    injected_variables['AZURE_DOCKER_BUILDARGS'] = \
                        '--build-arg CONTAINER_REG=%s --build-arg AGOGOSML_TAG=$(Build.TriggeredBy.BuildId)' % acr
            # Add git repository variables
            if 'repository' in manifest:
                # if it is in the manifest then it is validated by the schema to be complete.
                parsed_giturl = giturlparse.parse(manifest['repository']['url'])
                injected_variables['REPOSITORY_TYPE'] = manifest['repository']['type']
                injected_variables['REPOSITORY_URL'] = manifest['repository']['url']
                injected_variables['REPOSITORY_OWNER'] = parsed_giturl.owner
                injected_variables['REPOSITORY_REPO'] = parsed_giturl.name

    else:
        click.echo('manifest.json not found. Please run agogosml init first.')
        raise click.Abort()
    # Create folder if not exists
    if not os.path.isdir(folder):
        os.makedirs(folder)
    for template_src, template_dst in PROJ_FILES.items():
        template_src_filename = os.path.basename(template_src)
        # Check if files exists in dst
        if (os.path.exists(os.path.join(folder, template_dst))):
            if not force:
                click.echo('Files already exists. Use --force to overwrite')
                raise click.Abort()

        # Must end w/ -pipeline.json
        if cloud_vendor == 'azure' and template_src_filename.startswith('azure') \
           and template_src_filename.endswith('-pipeline.jsonnet'):
            # Modify pipeline file from defaults
            write_jsonnet(template_src, template_dst, folder, injected_variables)
        else:
            # Copy files as is from default
            utils.copy_module_templates(template_src, folder)


def write_jsonnet(source_path: str, target_path: str, base_path: str, injected_variables: object) -> None:
    """Writes out a pipeline json file
    Args:
        src (string):  Name of the pipeline file in module
        outfolder (string): Name of the output folder
        injected_variables (object): Values to inject into jsonnet as extVars.
    """
    pipeline_json = json.loads(_jsonnet.evaluate_file(
        filename=utils.get_template_full_filepath(source_path),
        ext_vars=injected_variables))
    full_path = os.path.join(base_path, target_path)
    with open(full_path, 'w') as f:
        json.dump(pipeline_json, f, indent=4)
