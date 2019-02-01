import json
from pathlib import Path

import click
import giturlparse
from cookiecutter.exceptions import OutputDirExistsException
from cookiecutter.main import cookiecutter

import _jsonnet
import cli.utils as utils

# Project files to output with src and dst names.
PROJ_FILES = {
    'pipeline/azure-ci-agogosml-pipeline.jsonnet':
        'ci-agogosml-pipeline.json',
    'pipeline/azure-ci-app-pipeline.jsonnet':
        'ci-app-pipeline.json',
    'pipeline/azure-cd-pipeline.jsonnet':
        'cd-pipeline.json',
    'pipeline/azure-ci-e2e-tests-pipeline.jsonnet':
        'e2e-pipeline.json'
}

APP_TEMPLATES = {
    'simple': 'apps/simple',
    'mleap':  'apps/mleap'
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
@click.option('--app-base', type=click.Choice(APP_TEMPLATES.keys()), default='simple')
@click.argument('folder', type=click.Path(), default='.', required=False)
def generate(force, config, app_base, folder) -> int:
    """Generates an agogosml project"""
    template_vars = {}
    template_file = utils.get_template_full_filepath('cookiecutter.json')
    with template_file.open() as f:
        template_vars = json.load(f)

    # Create folder if not exists
    folder = Path(folder)
    folder.mkdir(parents=True, exist_ok=True)

    # Read Manifest file
    config_path = Path(config)
    if not config_path.is_file() and (folder / config).is_file():
        config_path = folder / config

    if config_path.is_file():
        with config_path.open() as f:
            manifest = json.load(f)
            utils.validate_manifest(manifest)
            # Retrieve values
            template_vars = {**template_vars, **extractTemplateVarsFromManifest(manifest)}
    else:
        click.echo('manifest.json not found. Please run agogosml init first.')
        raise click.Abort()

    try:
        # Write cookiecutter template
        write_cookiecutter(utils.get_template_full_filepath(''),
                           folder, template_vars, force)
    except OutputDirExistsException:
        # Handle situation where template folder exists and force is not set to true
        click.echo('Files already exists in directory. Use --force to overwrite')
        raise click.Abort()

    try:
        # Write App Template
        write_cookiecutter(utils.get_template_full_filepath(APP_TEMPLATES[app_base]),
                           folder / template_vars['PROJECT_NAME_SLUG'],
                           template_vars, True)
    except OutputDirExistsException:
        # Handle situation where template folder exists and force is not set to true
        click.echo('Files already exists in directory. Use --force to overwrite')
        raise click.Abort()

    del template_vars['_copy_without_render']

    for template_src, template_dst in PROJ_FILES.items():
        template_src_filename = Path(template_src).name
        # Check if files exists in dst
        if (folder / template_dst).exists():
            if not force:
                click.echo('Files already exists in directory. Use --force to overwrite')
                raise click.Abort()

        # Must end w/ -pipeline.json
        if 'CLOUD_VENDOR' in template_vars and template_vars['CLOUD_VENDOR'] == 'azure' \
           and template_src_filename.startswith('azure') and template_src_filename.endswith('-pipeline.jsonnet'):
            # Modify pipeline file from defaults
            write_jsonnet(Path(template_src), Path(template_dst), folder, template_vars)


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
    if 'azureContainerRegistry' not in azure_props:
        click.echo('Azure property is missing or invalid.')
        raise click.Abort()
    else:
        acr = azure_props['azureContainerRegistry']
        template_vars['AZURE_CONTAINER_REGISTRY'] = acr
        if not acr.endswith('/'):
            acr += '/'
        template_vars['AZURE_DOCKER_BUILDARGS'] = \
            '--build-arg CONTAINER_REG=$(container_registry) --build-arg AGOGOSML_TAG=$(Build.BuildId)'
    return template_vars


def write_jsonnet(source_path: Path, target_path: Path, base_path: Path, template_vars: object):
    pipeline_json = json.loads(_jsonnet.evaluate_file(
        filename=str(utils.get_template_full_filepath(source_path)),
        ext_vars=template_vars))
    full_path = base_path / target_path
    with full_path.open('w') as f:
        json.dump(pipeline_json, f, indent=4)


def write_cookiecutter(source_path: Path, target_path: Path, template_vars: object, overwrite=False) -> None:
    return cookiecutter(str(source_path), extra_context=template_vars, no_input=True,
                        output_dir=str(target_path), overwrite_if_exists=overwrite)


def safe_filename(name: str) -> str:
    keepcharacters = (' ', '.', '_')
    return "".join(c for c in name if c.isalnum() or c in keepcharacters).rstrip()
