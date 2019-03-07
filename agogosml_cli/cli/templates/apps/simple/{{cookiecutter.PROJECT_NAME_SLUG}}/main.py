"""
Entrypoint for customer application.

Listens for HTTP(S) requests from the input reader, transforms the message
and sends the transformed message to the output writer.

You can view a specification for the API at /swagger.json as well as a testing
console at /ui/.

All business logic for {{cookiecutter.PROJECT_NAME_SLUG}} should be included
in `logic.py` and it is unlikely that changes to this `main.py` file will be
required.
"""
from logging import getLogger
from os import getenv

from logic import transform

from requests import post


LOG = getLogger(__name__)


class Config:
    """
    Class to hold all application configuration.

    All environment variable access hould happen in this class only.
    """

    PORT = getenv('PORT', '8888')
    HOST = getenv('HOST', '127.0.0.1')
    DATA_SCHEMA = getenv('SCHEMA_FILEPATH', 'data.spec.yaml')
    OUTPUT_URL = getenv('OUTPUT_URL', '')
    LOG_LEVEL = getenv('LOG_LEVEL', 'INFO').upper()


def main(data: dict):
    """Transform the input and forward the transformed payload via HTTP(S)."""
    data = transform(data)

    if not Config.OUTPUT_URL:
        LOG.warning('Not OUTPUT_URL specified, not forwarding data.')
        return data, 500

    response = post(Config.OUTPUT_URL, json=data)
    if not response.ok:
        LOG.error('Error %d with post to url %s and body %s.',
                  response.status_code, Config.OUTPUT_URL, data)
        return data, response.status_code

    LOG.info('Response %d received from output writer.', response.status_code)
    return data, 200


def build_app(wsgi=False):
    """Create the web server."""
    from connexion import App

    with open(Config.DATA_SCHEMA, encoding='utf-8') as fobj:
        data_schema = '\n'.join('  {}'.format(line.rstrip('\r\n'))
                                for line in fobj)

    LOG.setLevel(Config.LOG_LEVEL)

    app = App(__name__)
    app.add_api('api.spec.yaml', arguments={'DATA_SCHEMA': data_schema})

    return app.app if wsgi else app


def cli():
    """Command line interface for the web server."""
    from argparse import ArgumentParser

    from yaml import YAMLError

    parser = ArgumentParser(description=__doc__)

    for key, value in Config.__dict__.items():
        if not key.startswith('_'):
            parser.add_argument('--{}'.format(key.lower()), default=value)

    args = parser.parse_args()

    for key, value in args.__dict__.items():
        setattr(Config, key.upper(), value)

    try:
        app = build_app()
    except YAMLError as ex:
        parser.error('Unable to parse {} as a Swagger spec.\n\n{}'
                     .format(Config.DATA_SCHEMA, ex))
    else:
        app.run(port=int(Config.PORT), host=Config.HOST)


if __name__ == "__main__":
    cli()
