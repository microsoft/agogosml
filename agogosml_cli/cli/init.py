import json
from pathlib import Path

import click

import _jsonnet
import cli.utils as utils

DEFAULT_MANIFEST_FILE = 'manifest/manifest.jsonnet'


@click.command()
@click.option('--force', '-f', is_flag=True, default=False, required=False,
              help='Ovewrite existing manifest file')
@click.option('--project-name', prompt=True, required=False,
              help='Name of your project')
@click.option('--cloud-vendor', prompt=True, default='azure', required=False,
              help='Cloud vendor selected')
@click.argument('folder', type=click.Path(), default='.', required=False)
def init(force, project_name, cloud_vendor, folder) -> int:
    """Initializes an agogosml project by creating a manifest file"""
    # Check if exists
    folder = Path(folder)
    outfile = folder / 'manifest.json'
    if outfile.is_file():
        if force:
            click.echo('Overwriting %s' % outfile)
        else:
            click.echo('Manifest already exists. Use --force to overwrite')
            raise click.Abort()
    # Create folder if not exists
    outfile.parent.mkdir(parents=True, exist_ok=True)
    manifest = build_manifest(project_name, cloud_vendor)
    with outfile.open('w') as f:
        json.dump(manifest, f, indent=4)
    return 0


def build_manifest(project_name: str, cloud_vendor: str) -> object:
    """Builds the Manifest python object"""
    manifest_json = json.loads(_jsonnet.evaluate_file(
        filename=str(utils.get_template_full_filepath(DEFAULT_MANIFEST_FILE)),
        ext_vars={'PROJECT_NAME': project_name, 'CLOUD_VENDOR': cloud_vendor}))
    utils.validate_manifest(manifest_json)
    return manifest_json
