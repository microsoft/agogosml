"""Tests for `agogosml_cli` package."""

import json
from pathlib import Path

from click.testing import CliRunner
import cli.generate as generate
import tests.test_utils as test_utils


"""
* agogosml generate
    * should fail if no manifest.json is in working directory
    * should fail if manifest.json is invalid
    * should fail if files we expect to generate already exist.
        Should it give warning and ask to overwrite?
    * should generate .env file, pipeline files, Pipfile,
        tests/e2e/, tests/validation exist
    * should fail if any yml file is not valid yaml.
    * shoudl fail if any json file is not valid json.
"""

EXPECTED_OUTPUT_PROJ_FILES = (
    'cd-pipeline.json',
    'e2e-pipeline.json',
    'testproject/dockerbuild.sh',
    'testproject/.dockerignore',
    'testproject/README.md',
    'testproject/app-ci-pipeline.yml',
    'testproject/agogosml-ci-pipeline.yml',
    'testproject/agogosml/Dockerfile.agogosml',
    'testproject/input_reader/Dockerfile.input_reader',
    'testproject/input_reader/logging.yaml',
    'testproject/input_reader/main.py',
    'testproject/output_writer/Dockerfile.output_writer',
    'testproject/output_writer/logging.yaml',
    'testproject/output_writer/main.py',
    'testproject/testproject/Dockerfile.testproject',
    'testproject/testproject/logging.yaml',
    'testproject/testproject/main.py',
    'testproject/testproject/requirements-dev.txt',
    'testproject/testproject/requirements.txt',
    'testproject/testproject/datahelper.py',
    'testproject/testproject/schema_example.json',
    'testproject/testproject/testapp.py'
)


def test_generate():
    """Tests of generate command w/o <folder> specified"""
    runner = CliRunner()
    """
    RUN: agogosml generate
    RESULT: Fail because no manifest.json exists
    """
    with runner.isolated_filesystem():
        result = runner.invoke(generate.generate)
        assert result.exit_code == 1
    """
    RUN: agogosml generate
    RESULT: Produces the correct files in the current working directory
    """
    with runner.isolated_filesystem():
        _create_test_manifest_azure()
        result = runner.invoke(generate.generate)
        assert result.exit_code == 0
        _assert_template_files_exist()
    """
    RUN: agogosml generate
    RESULT: Fail because files exist and force is not specified.
    """
    with runner.isolated_filesystem():
        _create_test_manifest_azure()
        _create_dummy_template_files()
        prevmd5 = _get_md5_template_files()
        result = runner.invoke(generate.generate)
        assert result.exit_code == 1
        assert set(prevmd5) == set(_get_md5_template_files())
    """
    RUN: agogosml generate
    RESULT: Fail because manifest is invalid.
    """
    with runner.isolated_filesystem():
        _create_invalid_manifest_azure()
        _create_dummy_template_files()
        prevmd5 = _get_md5_template_files()
        result = runner.invoke(generate.generate)
        assert result.exit_code == 1
        assert set(prevmd5) == set(_get_md5_template_files())
    """
    RUN: agogosml generate -f
    RESULT: Overwrite existing files
    """
    with runner.isolated_filesystem():
        _create_test_manifest_azure()
        _create_dummy_template_files()
        prevmd5 = _get_md5_template_files()
        result = runner.invoke(generate.generate, ['--force'])
        assert result.exit_code == 0
        assert set(prevmd5) != set(_get_md5_template_files())
        _assert_template_files_exist()
    """
    RUN: agogosml generate
    RESULT: Fail since files already exist and should NOT overwite
    """
    with runner.isolated_filesystem():
        _create_test_manifest_azure()
        _create_dummy_template_files()
        prevmd5 = _get_md5_template_files()
        result = runner.invoke(generate.generate)
        assert result.exit_code == 1
        assert set(prevmd5) == set(_get_md5_template_files())
        _assert_template_files_exist()


def test_generate_folder():
    """Test of generate command with folder specified"""
    runner = CliRunner()
    """
    RUN: agogosml generate <folder>
    RESULT: Produces the correct files in the specified directory
    """
    with runner.isolated_filesystem():
        _create_test_manifest_azure()
        result = runner.invoke(generate.generate, ['folder'])
        assert result.exit_code == 0
        _assert_template_files_exist('folder')
    """
    RUN: agogosml generate <folder>
    RESULT: Produces the correct files in the specified directory
    where the manifest file is in the target directory.
    """
    with runner.isolated_filesystem():
        _create_test_manifest_azure('folder')
        result = runner.invoke(generate.generate, ['folder'])
        assert result.exit_code == 0
        _assert_template_files_exist('folder/')
    """
    RUN: agogosml generate -f <folder>
    RESULT: Overwrite existing files in the specified directory
    """
    with runner.isolated_filesystem():
        _create_test_manifest_azure()
        _create_dummy_template_files(folder='folder')
        prevmd5 = _get_md5_template_files(folder='folder')
        result = runner.invoke(generate.generate, ['--force', 'folder'])
        assert result.exit_code == 0
        assert set(prevmd5) != set(_get_md5_template_files(folder='folder'))
        _assert_template_files_exist('folder')
    """
    RUN: agogosml generate <folder>
    RESULT: Fail since files already exist and should NOT overwite
    """
    with runner.isolated_filesystem():
        _create_test_manifest_azure()
        _create_dummy_template_files(folder='folder')
        prevmd5 = _get_md5_template_files(folder='folder')
        result = runner.invoke(generate.generate, ['folder'])
        assert result.exit_code == 1
        assert set(prevmd5) == set(_get_md5_template_files(folder='folder'))
        _assert_template_files_exist('folder')


def test_generate_invalid_schema():
    """
    RUN: agogosml generate (with invalid manifest file)
    RESULT: Produces the ff in the current working directory:
        - .env
        - Pipfile
        - azure-ci-app-pipeline.json
        - ci-input-app-pipeline.json
        - ci-output-app-pipeline.json
        - azure-ci-e2e-tests-pipeline.json
    """
    runner = CliRunner()
    with runner.isolated_filesystem():
        manifest_str = """
        {
            "dummy": "abc"
        }
        """
        manifest = json.loads(manifest_str)
        with open('manifest.json', 'w') as file:
            json.dump(manifest, file, indent=4)

        result = runner.invoke(generate.generate)
        assert result.exit_code == 1


def _assert_template_files_exist(folder='.'):
    """Assert that an output template exists"""
    folder = Path(folder)
    for proj_file in EXPECTED_OUTPUT_PROJ_FILES:
        assert (folder / proj_file).exists()


def _create_test_manifest_azure(folder='.'):
    """Create valid manifest"""
    manifest_str = """
    {
        "name": "testproject",
        "cloud": {
            "vendor": "azure",
            "subscriptionId": "123-123-123-123",
            "otherProperties": {
                "azureContainerRegistry": "acr.azurecr.io",
                "azureResourceGroup": "agogosml-rg",
                "kubernetesCluster": "agogosml-k"
            }
        },
        "repository": {
            "type": "GitHub",
            "url": "https://github.com/Microsoft/agogosml.git"
        }
    }
    """
    manifest = json.loads(manifest_str)
    folder = Path(folder)
    folder.mkdir(parents=True, exist_ok=True)
    outfile = folder / 'manifest.json'
    with outfile.open('w') as file:
        json.dump(manifest, file, indent=4)


def _create_invalid_manifest_azure(folder='.'):
    """Create invalid manifest"""
    manifest_str = """
    {
        "name": "testproject",
        "cloud": {
            "vendor": "azure",
            "subscriptionId": "123-123-123-123",
            "otherProperties": {
                "azureContainerRegistry": "https://acr.acr.io"
            }
        },
        "repository": {
            "type": "GitHub",
            "url": "https://github.com/Microsoft/agogosml.git"
        }
    }
    """
    manifest = json.loads(manifest_str)
    folder = Path(folder)
    folder.mkdir(parents=True, exist_ok=True)
    outfile = folder / 'manifest.json'
    with outfile.open('w') as file:
        json.dump(manifest, file, indent=4)


def _create_dummy_template_files(files=EXPECTED_OUTPUT_PROJ_FILES, folder='.'):
    """Create dummy template files."""
    folder = Path(folder)
    folder.mkdir(parents=True, exist_ok=True)

    (folder / 'testproject' / 'agogosml').mkdir(parents=True, exist_ok=True)
    (folder / 'testproject' / 'input_reader').mkdir(parents=True, exist_ok=True)
    (folder / 'testproject' / 'output_writer').mkdir(parents=True, exist_ok=True)
    (folder / 'testproject' / 'testproject').mkdir(parents=True, exist_ok=True)

    for proj_file in files:
        outfile = folder / proj_file

        with outfile.open('w') as file:
            json.dump("test content", file, indent=4)


def _get_md5_template_files(files=EXPECTED_OUTPUT_PROJ_FILES, folder='.'):
    """Get the md5 hashes of the project files. Used to know if files were overwritten"""
    folder = Path(folder)
    allmd5 = []
    for proj_file in files:
        outfile = folder / proj_file
        allmd5.append(test_utils.md5(outfile))
    return allmd5
