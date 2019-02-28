"""Generate command module."""

import json
from pathlib import Path

import click
import giturlparse
import tldextract
from cookiecutter.exceptions import OutputDirExistsException
from cookiecutter.main import cookiecutter

import cli.utils as utils
from cli import __version__

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
def generate(force, config, app_base, folder):
    """Generates an agogosml project"""
    template_vars = {}
    template_file = utils.get_template_full_filepath('cookiecutter.json')
    with template_file.open() as fobj:
        template_vars = json.load(fobj)

    # Create folder if not exists
    folder = Path(folder)
    folder.mkdir(parents=True, exist_ok=True)

    # Read Manifest file
    config_path = Path(config)
    if not config_path.is_file() and (folder / config).is_file():
        config_path = folder / config

    if config_path.is_file():
        with config_path.open() as fobj:
            manifest = json.load(fobj)
            utils.validate_manifest(manifest)
            # Retrieve values
            template_vars = {**template_vars, **extract_template_vars_from_manifest(manifest)}
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


def extract_template_vars_from_manifest(manifest: dict) -> dict:
    """Extract template variables from manifest"""
    template_vars = {
        'PROJECT_NAME': manifest['name'],
        'PROJECT_NAME_SLUG': safe_filename(manifest['name']),
        'CLOUD_VENDOR': manifest['cloud']['vendor'],
        **add_agogosml_template_vars()
    }

    if manifest['cloud']['vendor'] == 'azure':
        template_vars = {**template_vars, **extract_azure_template_vars(manifest)}

    # Add git repository variables
    if 'repository' in manifest:
        # if it is in the manifest then it is validated by the schema to be complete.
        parsed_giturl = giturlparse.parse(manifest['repository']['url'])
        template_vars['REPOSITORY_TYPE'] = manifest['repository']['type']
        template_vars['REPOSITORY_URL'] = manifest['repository']['url']
        template_vars['REPOSITORY_OWNER'] = parsed_giturl.owner
        template_vars['REPOSITORY_REPO'] = parsed_giturl.name
    return template_vars


def extract_azure_template_vars(manifest: dict) -> dict:
    """Extract Azure template variables from manifest"""
    template_vars = {}
    azure_props = manifest['cloud']['otherProperties']
    if 'azureContainerRegistry' not in azure_props:
        click.echo('Azure property is missing or invalid. - not generating acr')
        return template_vars

    acr = azure_props['azureContainerRegistry']
    try:
        extract_result = tldextract.extract(acr)
    except ValueError:
        # Handle situation where template folder exists and force is not set to true
        click.echo('Azure Container Registry property is not parseable as a url. \
            Valid property: nameacr.azurecr.io.')
        raise click.Abort()

    if extract_result.registered_domain != "azurecr.io":
        click.echo('Azure Container Registry property is not set to an azurecr.io domain.')
        raise click.Abort()
    if len(extract_result.subdomain.split('.')) > 1:
        click.echo('Azure Container Registry property contains multiple subdomains.')
        raise click.Abort()
    template_vars['AZURE_CONTAINER_REGISTRY'] = extract_result.subdomain + '.' + extract_result.registered_domain

    return template_vars


def add_agogosml_template_vars() -> dict:
    """Add agogosml-specific template variables"""
    return {
        'AGOGOSML_CLI_VERSION': __version__
    }


def write_cookiecutter(source_path: Path, target_path: Path, template_vars: object, overwrite=False):
    """Outputs a cookiecutter template"""
    return cookiecutter(str(source_path), extra_context=template_vars, no_input=True,
                        output_dir=str(target_path), overwrite_if_exists=overwrite)


def safe_filename(name: str) -> str:
    """Make string safe for use as a filename"""
    keepcharacters = (' ', '.', '_')
    return "".join(c for c in name if c.isalnum() or c in keepcharacters).rstrip()
