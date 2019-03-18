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

from requests import post

import settings
from logic import transform

LOG = getLogger(__name__)


def main(data: dict):
    """Transform the input and forward the transformed payload via HTTP(S)."""
    data = transform(data)

    if not settings.OUTPUT_URL:
        LOG.warning('Not OUTPUT_URL specified, not forwarding data.')
        return data, 500

    response = post(settings.OUTPUT_URL, json=data)
    if not response.ok:
        LOG.error('Error %d with post to url %s and body %s.',
                  response.status_code, settings.OUTPUT_URL, data)
        return data, response.status_code

    LOG.info('Response %d received from output writer.', response.status_code)
    return data, 200


def build_app(wsgi=False):
    """Create the web server."""
    from connexion import App

    with open(settings.DATA_SCHEMA, encoding='utf-8') as fobj:
        data_schema = '\n'.join('  {}'.format(line.rstrip('\r\n'))
                                for line in fobj)

    LOG.setLevel(settings.LOG_LEVEL)

    app = App(__name__)
    app.add_api('api.spec.yaml', arguments={'DATA_SCHEMA': data_schema})

    return app.app if wsgi else app


def cli():
    """Command line interface for the web server."""
    from argparse import ArgumentParser

    from yaml import YAMLError

    parser = ArgumentParser(description=__doc__)
    parser.parse_args()

    try:
        app = build_app()
    except YAMLError as ex:
        parser.error('Unable to parse {} as a Swagger spec.\n\n{}'
                     .format(settings.DATA_SCHEMA, ex))
    else:
        app.run(port=int(settings.PORT), host=settings.HOST)


if __name__ == "__main__":
    cli()
